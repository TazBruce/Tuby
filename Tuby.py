from pytube import YouTube
import PySimpleGUI as sg


def progress_check(stream = None, chunk = None, file_handle = None, remaining = None):
    #Gets the percentage of the file that has been downloaded.
    percent = (100*(file_size-remaining))/file_size
    print("{:00.0f}% downloaded".format(percent))


sg.ChangeLookAndFeel('DarkRed1')
# sg.SetGlobalIcon('logo.ico')

layout = [[sg.T("Tuby")],
          [sg.T("URL")],
          [sg.I(key="_URL_")],
          [sg.T("Destination")],
          [sg.I(" ", key="_FOLDER_"), sg.FolderBrowse()],
          [sg.B("Download")]
          ]
window = sg.Window('Tuby', layout, default_element_size=(40, 1), resizable=True, font="Helvetica").finalize()
while True:
    event, values = window.Read()
    print(values)
    if event in (None, 'Exit'):
        break
    elif event == "Download":
        YouTube(values["_URL_"]).streams.first().download(values["_FOLDER_"])
        YouTube.register_on_progress_callback(show_progress_bar)

window.close()
