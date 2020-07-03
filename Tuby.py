import os

import PySimpleGUI as sg
from moviepy.editor import *
from pytube import YouTube

file_size = 0


# Updates GUI progress bar depending on current progress of download
def progress_check(stream, chunk, remaining):
    percent = (100 * (file_size - remaining)) / file_size
    window["_BAR_"].UpdateBar(percent)


# Converts MP4 youtube file into MP3 File
def convert(video, audio):
    videoClip = VideoFileClip(video)
    audioClip = videoClip.audio
    audioClip.write_audiofile(audio)
    audioClip.close()
    videoClip.close()


# sg.ChangeLookAndFeel('DarkRed1')
# sg.SetGlobalIcon('logo.ico')

layout = [[sg.T("Tuby")],
          [sg.T("URL")],
          [sg.I(key="_URL_", size=(42, 18))],
          [sg.T("File Name")],
          [sg.I(key="_FILE_", size=(42, 18))],
          [sg.T("Destination")],
          [sg.FolderBrowse(), sg.I(" ", key="_FOLDER_", size=(34, 18))],
          [sg.Radio("MP3", group_id="FORMAT", default=True, key="_FORMAT_"), sg.Radio("MP4", group_id="FORMAT")],
          [sg.B("Download", size=(42, 1))],
          [sg.ProgressBar(max_value=100, orientation="horizontal", key="_BAR_", size=(36, 25))]
          ]
window = sg.Window('Tuby', layout, default_element_size=(50, 1), resizable=False, font="Helvetica").finalize()
while True:
    event, values = window.Read()
    print(values)
    if event in (None, 'Exit'):
        break
    elif event == "Download":
        sg.popup("Starting Download...", auto_close=True, auto_close_duration=1)
        video = YouTube(values["_URL_"], on_progress_callback=progress_check)
        video_type = video.streams.filter(progressive=True, file_extension="mp4").first()
        title = values["_FILE_"]
        file_size = video_type.filesize
        video_type.download(values["_FOLDER_"], filename=title)
        if values["_FORMAT_"]:
            mp4 = values["_FOLDER_"] + "/" + title + ".mp4"
            mp3 = values["_FOLDER_"] + "/" + title + ".mp3"
            convert(mp4, mp3)
            os.remove(mp4)

        window["_BAR_"].UpdateBar(0)
        window["_FOLDER_"].Update(" ")
        window["_URL_"].Update(" ")
        sg.popup("Complete!", auto_close=False)

window.close()
