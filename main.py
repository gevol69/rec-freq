import tkinter as tk
from tkinter.filedialog import askdirectory
from PIL import ImageTk
import wave
import sys, os
from recognition import find_formant
import time
import csv
import pyaudio


class Main(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.init_main()

    def init_main(self):
        self.centerWindow()


    def centerWindow(self):
        w = 250
        h = 640
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - w)/2
        y = (sh - h)/2
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))


def write_csv(data, name):
    os.chdir(default_dir + '\\Results\\' + name)
    with open(name + 'freq.csv', 'a', newline='') as file:
        order = [   
                    'number',
                    'name_file_wav', 
                    'numb_formant', 
                    'freq_1_formant', 
                    'amplitude_1_formant',
                    'min_1_formant',
                    'max_1_formant',
                    'freq_2_formant', 
                    'amplitude_2_formant',
                    'min_2_formant',
                    'max_2_formant',
                    'freq_3_formant', 
                    'amplitude_3_formant',
                    'min_3_formant',
                    'max_3_formant',
                    'freq_4_formant', 
                    'amplitude_4_formant',
                    'min_4_formant',
                    'max_4_formant',
                    'freq_5_formant', 
                    'amplitude_5_formant',
                    'min_5_formant',
                    'max_5_formant',
                    'freq_6_formant', 
                    'amplitude_6_formant',
                    'min_6_formant',
                    'max_6_formant',
                    'freq_7_formant', 
                    'amplitude_7_formant',
                    'min_7_formant',
                    'max_7_formant',
                    'freq_need_formant'
                ]
        writer = csv.DictWriter(file, fieldnames=order)
        writer.writerow(data)

def click_button():
    recordButton.configure(text='Идет запись', image=image_process, compound='left', font='14')

def record_audio():
    global number_file
    letter = letter_text.get() 
    number_file += 1
    recordButton.configure(text='Идет запись', image=image_process, compound='left', font='14')
    recordButton.configure(state='disabled')
    root.update()


    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 4
    WAVE_OUTPUT_FILENAME = letter + str(number_file) + ".wav"


    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)


    frames = []

    count = 0
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
        if i % 46 == 0:
            count += 1
        recordButton.configure(text='Идет запись' + ' 00:0' + str(count), image=image_process, compound='left', font='14')
        root.update()

    #print(RATE / CHUNK * RECORD_SECONDS)


    recordButton.configure(text='Запись звука', image=image_record, compound='left', font='14')
    root.update()

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    listbox_letters.insert(0, WAVE_OUTPUT_FILENAME)
    recordButton.configure(state='active')



def create_dir_user():
    try:
        global default_dir
        os.chdir(default_dir)
        name_user = name_text.get()
        global new_path_user
        new_path_user = default_dir + '\\Results\\'  + name_user
        os.mkdir(new_path_user)
        os.chdir(new_path_user)
        #create_dir_name.configure(state='disabled')
        #create_dir_lett.configure(state='active')
        recordButton.configure(state='active')
        open_folder.configure(state='active')
    except:
        print('Пустое поле')


def create_dir_letter():
    try:
        global number_file
        number_file = 0
        os.chdir(new_path_user)
        letter = letter_text.get()
        new_path_letter = os.getcwd() + '\\' + letter
        os.mkdir(new_path_letter)
        os.chdir(new_path_letter)
        listbox_letters.delete(0, 'end')
        build_graph.configure(state='disabled')
    except:
        print('Пустое поле')


def choose(event):
    try:
        build_graph.configure(state='active')
        widget = event.widget
        global selection
        selection = widget.curselection()
        global value
        value = widget.get(selection[0])
    except:
        print('Нечего выделять!')
 

def building_graph():
    flag_unload = False
    global dir_folder_file
    try:
        file_path = os.getcwd() + '\\' + value
        find_formant(file_path, flag_unload)
    except:
        file_path = dir_folder_file + '\\' + value
        find_formant(file_path, flag_unload)

  


def creating_new_user():
    global number_file
    number_file = 0
    name_text.delete(0, 'end')
    letter_text.delete(0, 'end')
   # create_dir_name.configure(state='active')
    listbox_letters.delete(0, 'end')
    #create_dir_lett.configure(state='disabled')
    build_graph.configure(state='disabled')

def opening_folder():
    count = 0
    listbox_letters.delete(0, 'end')
    letter_text.delete(0, 'end')
    name_text.delete(0, 'end')
    dir_path = askdirectory()
    global dir_folder_file 
    for root, dirs, files in os.walk(dir_path):  
        dir_folder_file = root
        for filename in files:
            listbox_letters.insert(0, filename)
            count += 1
    os.chdir(dir_folder_file)
    build_graph.configure(state='active')
    recordButton.configure(state='active')
    letter_text.insert(0, dir_folder_file[-1:])
    name_text.insert(0, dir_folder_file[dir_folder_file[:-2].rfind('/'):])
    global number_file
    number_file = count
   
    

def deleting_file():
    global dir_folder_file
    try:
        file_path = os.getcwd() + '\\' + value
        os.remove(file_path)
    except:
        file_path = dir_folder_file + '\\' + value
        os.remove(file_path)
    listbox_letters.delete(selection[0])

def unload():
    os.chdir(default_dir)
    flag_unload = True
    name_Exp = ['Exp1', 'Exp2']
    for name in name_Exp:
        os.chdir(default_dir)
        way_file = os.getcwd() + '\\Results\\' + name + '\\{}\\{}\\{}.wav'
        letters = ['a', 'e', 'o']
        numbers = ['1 - f', '2 - f', '3 - m', '4 - f', '5 - m', '6 - m', '7 - f']
        path = default_dir + '\\Results\\' + '\\Graphs\\' + '\\' + name + '\\'
        for number in numbers:
            new_path_number = path + '\\' + number
            os.mkdir(new_path_number)
            os.chdir(new_path_number)
            for letter in letters:
                new_path_letter = new_path_number + '\\' + letter
                os.mkdir(new_path_letter)
                os.chdir(new_path_letter)
                for i in range(1, 11):
                    name_file_wav = letter + str(i)
                    file = way_file.format(number, letter, name_file_wav)
                    print_find_formant = find_formant(file, flag_unload)
                    min_freqs = print_find_formant[0]
                    max_freqs = print_find_formant[1]
                    freq_need_formant = print_find_formant[2]
                    values_need = print_find_formant[3]
                    print(number, ':', name_file_wav, freq_need_formant, values_need.keys(), values_need.values())
                    freqs = list(values_need.keys())
                    amplitudes = list(values_need.values())
                    data = {
                            'number' : number,
                            'name_file_wav' : name_file_wav, 
                            'freq_1_formant' : freqs[0],
                            'amplitude_1_formant' : amplitudes[0],
                            'min_1_formant' : min_freqs[0], 
                            'max_1_formant': max_freqs[0], 
                            'freq_2_formant' : freqs[1], 
                            'amplitude_2_formant' : amplitudes[1],
                            'min_2_formant': min_freqs[1], 
                            'max_2_formant': max_freqs[1],
                            'freq_3_formant' : freqs[2], 
                            'amplitude_3_formant' : amplitudes[2],
                            'min_3_formant': min_freqs[2], 
                            'max_3_formant': max_freqs[2],
                            'freq_4_formant' : freqs[3],
                            'amplitude_4_formant' : amplitudes[3],
                            'min_4_formant': min_freqs[3], 
                            'max_4_formant': max_freqs[3],
                            'freq_5_formant' : freqs[4], 
                            'amplitude_5_formant' : amplitudes[4],
                            'min_5_formant': min_freqs[4], 
                            'max_5_formant': max_freqs[4],
                            'freq_6_formant' : freqs[5], 
                            'amplitude_6_formant' : amplitudes[5],
                            'min_6_formant': min_freqs[5], 
                            'max_6_formant': max_freqs[5],
                            'freq_7_formant' : freqs[6], 
                            'amplitude_7_formant' : amplitudes[6],
                            'min_7_formant': min_freqs[6], 
                            'max_7_formant': max_freqs[6],
                            'freq_need_formant': freq_need_formant
                        }
                    write_csv(data, name)
                    os.chdir(new_path_letter)


if __name__ == "__main__":
    import warnings 
    warnings.filterwarnings("ignore", category=UserWarning)
    flag_unload = False
    global default_dir
    default_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
    global number_file
    number_file = 0
    root = tk.Tk()
    app = Main(root)
    app.pack()
    root.title("Форманта")
    root.resizable(False, False)
    image_record = ImageTk.PhotoImage(file=default_dir + '\\Images\\' + 'record.png')
    image_process = ImageTk.PhotoImage(file=default_dir + '\\Images\\' + "process.png")
    image_graph = ImageTk.PhotoImage(file=default_dir + '\\Images\\' + "graph.jpg")
    image_new_user = ImageTk.PhotoImage(file=default_dir + '\\Images\\' + "new_user.png")
    name_label = tk.Label(root, text='Пользователь', font='Arial 12')
    name_label.pack(side='top', fill='x')
    name_text = tk.Entry(root, font='Arial 12')
    name_text.pack(side='top', fill='x')
    letter_label = tk.Label(root, text='Буква', font='Arial 12')
    letter_label.pack(side='top', fill='x')
    letter_text = tk.Entry(root, font='Arial 12')
    letter_text.pack(side='top', fill='x')
    letters_label = tk.Label(root, text='Записанные буквы', font='Arial 12')
    letters_label.pack(side='top', fill='x')
    open_folder = tk.Button(root)
    open_folder.configure(text='Открыть папку', font='Arial 10', command=opening_folder)
    open_folder.pack(side='top', fill='x')
    listbox_letters = tk.Listbox(root, height=10, font='Arial 14')
    listbox_letters.pack(side='top', fill='x')
    listbox_letters.bind("<<ListboxSelect>>", choose)
    delete_file = tk.Button(root)
    delete_file.configure(text='Удалить файл', font='Arial 10', command=deleting_file)
    delete_file.pack(side='top', fill='x')
    build_graph = tk.Button(root)
    build_graph.configure(text='Построить графики', image=image_graph, compound='left', font='14', command=building_graph)
    build_graph.pack(side='top', fill='x')
    build_graph.configure(state='disabled')
    recordButton = tk.Button(root)
    recordButton.configure(text='Запись звука', image=image_record, compound='left', font='14', command=record_audio)
    recordButton.pack(side='top', fill='x')
    recordButton.configure(state='disabled')
    create_new_user = tk.Button(root)
    create_new_user.configure(text='Новый пользователь', image=image_new_user, compound='left', font='14', command=creating_new_user)
    create_new_user.pack(side='top', fill='x')
    unload_button = tk.Button(root)
    unload_button.configure(text='Выгрузить', compound='left', font='14', command=unload)
    unload_button.pack(side='top', fill='x')
    root.mainloop()