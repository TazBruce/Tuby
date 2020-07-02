import PySimpleGUI as sg
from pytube import YouTube

file_size = 0


def progress_check(stream, chunk, remaining):
    percent = (100 * (file_size - remaining)) / file_size
    window["_BAR_"].UpdateBar(percent)


# sg.ChangeLookAndFeel('DarkRed1')
# sg.SetGlobalIcon('logo.ico')

layout = [[sg.T("Tuby")],
          [sg.T("URL")],
          [sg.I(key="_URL_", size=(42, 18))],
          [sg.T("Destination")],
          [sg.I(" ", key="_FOLDER_", size=(42, 18)), sg.FolderBrowse()],
          [sg.B("Download")],
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
        title = video.title
        print(title)
        file_size = video_type.filesize
        video_type.download(values["_FOLDER_"], filename=title)
        window["_BAR_"].UpdateBar(0)
        sg.popup("Complete!", auto_close=False)

window.close()
