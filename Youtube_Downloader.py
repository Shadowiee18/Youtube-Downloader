import tkinter as tk
from pytube import Playlist, YouTube, exceptions
import os
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat
from tkinter import messagebox
from tkinter import filedialog


def download_mp3(video, save_path):
    file_path = os.path.join(save_path, video.title + '.mp3')
    if os.path.exists(file_path):
        print(f'{video.title} already exists.')
    else:
        audio_stream = video.streams.filter(only_audio=True).first()
        audio_stream.download(save_path, filename=video.title + '.mp3')
        print(video.watch_url, 'downloaded.')


def download_mp4(video, save_path):
    file_path = os.path.join(save_path, video.title + '.mp4')
    if os.path.exists(file_path):
        print(f'{video.title} already exists.')
    else:
        highest_res = video.streams.get_highest_resolution()
        highest_res.download(save_path)
        print(video.watch_url, 'downloaded.')


def save_click():
    path_entry.delete(0, tk.END)
    path_entry.insert(0, filedialog.askdirectory(initialdir="D:\\Music"))


def button_click():
    if os.path.isdir(path_entry.get()):
        save_path = path_entry.get()
        if rbVar.get() == 0:
            try:
                url = url_entry.get()
                playlist = Playlist(url)
                if mpVar.get() == 0:
                    with ThreadPoolExecutor(max_workers=20) as executor:
                        executor.map(download_mp3, playlist.videos, repeat(save_path))
                    messagebox.askokcancel(title='Finish', message='Finished Downloading.')
                elif mpVar.get() == 1:
                    with ThreadPoolExecutor(max_workers=20) as executor:
                        executor.map(download_mp4, playlist.videos, repeat(save_path))
                    messagebox.askokcancel(title='Finish', message='Finished Downloading.')

            except KeyError:
                messagebox.askretrycancel(title='Error', message='Invalid URL')
        elif rbVar.get() == 1:
            try:
                url = url_entry.get()
                if mpVar.get() == 0:
                    download_mp3(YouTube(url), save_path)
                elif mpVar.get() == 1:
                    download_mp4(YouTube(url), save_path)

            except KeyError:
                messagebox.askretrycancel(title='Error', message='Invalid URL')

            except exceptions.RegexMatchError:
                messagebox.askretrycancel(title='Error', message='Invalid URL')
    else:
        messagebox.showerror(title='Error', message='Folder not found.')


if __name__ == '__main__':
    window = tk.Tk()
    multiple_choices = ['Playlist', 'Song']
    mp_choices = ['MP3', 'MP4']
    mpVar = tk.IntVar()
    rbVar = tk.IntVar()
    window.title('MP3 downloader')
    window.geometry('800x800')
    icon = tk.PhotoImage(file='images.png')
    photo = tk.PhotoImage(file='among_us_player_red_icon_156942.png')
    window.iconphoto(True, icon)
    label1 = tk.Label(window,
                      text='MP3 downloader',
                      font=('Arial', 30, 'bold'),
                      image=photo,
                      compound=tk.BOTTOM
                      )
    label2 = tk.Label(window,
                      text='Enter an URL:',
                      font=('Arial', 20, 'bold'),
                      relief=tk.RAISED
                      )
    label3 = tk.Label(window,
                      text='Enter a save path:',
                      font=('Arial', 20, 'bold'),
                      relief=tk.RAISED
                      )
    label1.pack(side=tk.TOP)
    label2.place(x=250, y=200)
    label3.place(x=250, y=300)
    convert_button = tk.Button(window,
                               text='Convert to MP3',
                               font=('Arial', 35, 'bold'),
                               activebackground='white',
                               activeforeground='black',
                               command=button_click
                               )
    convert_button.place(x=200, y=450)
    save_button = tk.Button(window,
                            text='V',
                            font=('Arial', 14, 'bold'),
                            command=save_click,
                            background='white',
                            foreground='black'
                            )
    save_button.place(x=553, y=340)

    url_entry = tk.Entry(window,
                         font=('Arial', 20, 'bold'),
                         relief=tk.RAISED
                         )
    path_entry = tk.Entry(window,
                          font=('Arial', 20, 'bold'),
                          relief=tk.RAISED
                          )
    path_entry.place(x=250, y=340)
    path_entry.insert(0, 'D:\\Music')
    url_entry.place(x=250, y=240)

    for i in range(len(multiple_choices)):
        radio_buttons = tk.Radiobutton(window,
                                       text=multiple_choices[i],
                                       font=('Arial', 15, 'bold'),
                                       variable=rbVar,
                                       value=i
                                       )
        radio_buttons.pack(side=tk.LEFT, anchor='nw')
    for i in range(len(mp_choices)):
        radio_buttons = tk.Radiobutton(window,
                                       text=mp_choices[i],
                                       font=('Arial', 15, 'bold'),
                                       variable=mpVar,
                                       value=i
                                       )
        radio_buttons.pack(side=tk.RIGHT, anchor='nw')
    window.mainloop()
