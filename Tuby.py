from pytube import YouTube
import PySimpleGUI as sg

file_size = 0


def progress_check(stream=None, chunk=None, file_handle=None, remaining=None):
    percent = (100*(file_size-remaining))/file_size
    sg.one_line_progress_meter('Progress Bar', current_value=percent, max_value=100, key="_BAR_",
                               orientation="horizontal")


sg.ChangeLookAndFeel('DarkRed1')
# sg.SetGlobalIcon('logo.ico')

layout = [[sg.T("Tuby")],
          [sg.T("URL")],
          [sg.I(key="_URL_")],
          [sg.T("Destination")],
          [sg.I(" ", key="_FOLDER_"), sg.FolderBrowse()],
          [sg.B("Download")],
          ]
window = sg.Window('Tuby', layout, default_element_size=(50, 1), resizable=False, font="Helvetica").finalize()
while True:
    event, values = window.Read()
    print(values)
    if event in (None, 'Exit'):
        break
    elif event == "Download":
        sg.popup("Starting Download...", auto_close=True, auto_close_duration=3)
        video = YouTube(values["_URL_"], on_progress_callback=progress_check)
        video_type = video.streams.filter(progressive=True, file_extension="mp4").first()
        title = video.title
        file_size = video_type.filesize
        video_type.download(values["_FOLDER_"])


window.close()
