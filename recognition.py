from __future__ import print_function
import scipy.io.wavfile as wavfile
import scipy
import scipy.fftpack
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from scipy import signal
from scipy.signal import medfilt

import scipy.signal

from detect_peaks import detect_peaks #обнаружение пиков

#fs_rate - частотная выборка
#signal - объект для хранения wav файла
#l_audio - количество каналов 
#N - полная дискретизация


def find_formant(file, flag_unload):
    fs_rate, sig = wavfile.read(file) #считывание wav файла
    #print ("Частота дискретизации", fs_rate)
    l_audio = len(sig.shape)
    #print ("Количество каналов", l_audio)
    if l_audio == 2:
        sig = sig.sum(axis=1) / 2
    N = sig.shape[0]
    #print ("Полная дискретизация (выборка) N", N)
    secs = N / float(fs_rate)
    #print ("Секунд", secs)
    Ts = 1.0/fs_rate # время между выборками
    #print ("Время между выборками Ts", Ts)
    t = scipy.arange(0, secs, Ts) # вектор времени в scipy arange field / numpy.ndarray



    FFT = abs(scipy.fft(sig))
    FFT_side = FFT[range(N//2)] # односторонний диапазон FFT
    freqs = scipy.fftpack.fftfreq(sig.size, t[1]-t[0])
    fft_freqs = np.array(freqs)
    freqs_side = freqs[range(N//2)] # однополосный частотный диапазон

    fft_freqs_side = np.array(freqs_side[0:7500])
    fft_amplitude_side = np.array(FFT_side[0:7500])

    
    fft_amplitude_side_smooth = medfilt(fft_amplitude_side)


    plt.figure(figsize=(14, 6), dpi= 100, facecolor='w', edgecolor='k')
    plt.xlabel('Частота (Hz)')
    plt.ylabel('Амплитуда') 
    plt.plot(fft_freqs_side, abs(fft_amplitude_side_smooth), "g")

    gender = file[:file.rfind('\\')][-3]

    letter = file[:file.rfind('\\')][-1]

    #поиск пиков
    mph = 10000
    if gender == 'f':
        mpd = 550
    else:
        mpd = 300
       

    peakind = detect_peaks(fft_amplitude_side_smooth, mph=mph, mpd=mpd)

    fft_freqs_side_peakind = np.array(fft_freqs_side[peakind])
    max_freq = max(fft_freqs_side_peakind)
    fft_amplitude_side_smooth_peakind = np.array(fft_amplitude_side_smooth[peakind])
    max_amplitude = max(fft_amplitude_side_smooth_peakind)

    



    if gender == 'f':
        fft_freqs_side_peakind = np.array(fft_freqs_side_peakind[0:7])
        fft_amplitude_side_smooth_peakind = np.array(fft_amplitude_side_smooth_peakind[0:7])
        formant_one = fft_freqs_side_peakind[0]
    else:
        fft_freqs_side_peakind = fft_freqs_side_peakind[1:]
        fft_amplitude_side_smooth_peakind = fft_amplitude_side_smooth_peakind[1:]
        fft_freqs_side_peakind = np.array(fft_freqs_side_peakind[0:7])
        fft_amplitude_side_smooth_peakind = np.array(fft_amplitude_side_smooth_peakind[0:7])
        

 
    formant_last = fft_freqs_side_peakind[-1]
    amplitude_formant_last = fft_amplitude_side_smooth_peakind[-1]


    name_wav_file = file[file.rfind('\\')+1:]
    values_need = dict(zip(fft_freqs_side_peakind, fft_amplitude_side_smooth_peakind))
    for key, value in values_need.items():
        if value == max(fft_amplitude_side_smooth_peakind):
            freq_need_formant = key
    
    plt.title(name_wav_file + '\n' + 'Частота форманты с наибольшей амплитудой: {}'.format(freq_need_formant), fontsize=14, y=1.05)
    plt.plot(fft_freqs_side_peakind, abs(fft_amplitude_side_smooth_peakind), color='red', marker='o', linestyle='')

    # if gender == 'f':
    #     plt.plot(fft_freqs_side_peakind, abs(fft_amplitude_side_smooth_peakind), color='red', marker='o', linestyle='')
    # else:
    #     plt.plot(fft_freqs_side_peakind[1:], abs(fft_amplitude_side_smooth_peakind[1:]), color='red', marker='o', linestyle='')
    
    
    freqs = []
    amplitudes = []
    for value in fft_freqs_side_peakind:
        freqs.append(float('{:.3f}'.format(value)))
    for value in fft_amplitude_side_smooth_peakind:
        amplitudes.append(float('{:.3f}'.format(value)))
    values = dict(zip(freqs, amplitudes))


    res = ''
    numb = 0
    for key, val in values.items():
        numb += 1
        res += '{} форм. {} : {}'.format(numb, key, val) + '\n'
    
    result = '              Частота : Амплитуда\n' + res

    plt.text(max_freq - mpd, max_amplitude, result, va='top', fontsize=12)
    
    mph = 200000
    mpd = 65
    min_freqs = []
    min_amplitudes = []
    max_freqs = []
    max_amplitudes = []
    peakind_min = detect_peaks(fft_amplitude_side_smooth, mph=mph, mpd=mpd, valley = True)
    fft_freqs_side_peakind_min = np.array(fft_freqs_side[peakind_min])
    fft_amplitude_side_smooth_peakind_min = np.array(fft_amplitude_side_smooth[peakind_min])
    for formant in fft_freqs_side_peakind:
        N_min = formant - mpd
        N_max = formant + mpd
        min_range = min(fft_freqs_side_peakind_min, key=lambda x: abs(N_min-x))
        index_min_range = list(fft_freqs_side_peakind_min).index(min_range)
        max_range = min(fft_freqs_side_peakind_min, key=lambda x: abs(N_max-x))
        index_max_range = list(fft_freqs_side_peakind_min).index(max_range)
        minimum = fft_freqs_side_peakind_min[index_min_range]
        maximum = fft_freqs_side_peakind_min[index_max_range]
        index_min = list(fft_freqs_side_peakind_min).index(minimum)
        index_max = list(fft_freqs_side_peakind_min).index(maximum)
        min_freqs.append(fft_freqs_side_peakind_min[index_min])
        min_amplitudes.append(fft_amplitude_side_smooth_peakind_min[index_min])
        max_freqs.append(fft_freqs_side_peakind_min[index_max])
        max_amplitudes.append(fft_amplitude_side_smooth_peakind_min[index_max])

    plt.plot(min_freqs, min_amplitudes, color='blue', marker='o', linestyle='')
    plt.plot(max_freqs, max_amplitudes, color='blue', marker='o', linestyle='')
    
    
    
    
    
    if not flag_unload:
        plt.show()
    else:
        #Сохранение картинки
        plt.savefig(name_wav_file + '.png')
        plt.close()

    return(min_freqs, max_freqs, freq_need_formant, values_need)

