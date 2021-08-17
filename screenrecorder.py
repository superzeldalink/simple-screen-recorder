from os import sys
import PySimpleGUI as sg
import subprocess
import os.path
import ctypes


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(
        os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def getMaxRes():
    default = [1080, 720, 480, 360]
    maxH = sg.Window.get_screen_size()[1]
    res = ['Default']
    for i in default:
        if i <= maxH:
            res.append(i)
    return res


def getRes():
    value = values['res']
    if value == 'Default':
        return '-1'

    return str(value)


def getQuality():
    value = values['quality']
    return str(round(-0.25*value+50))


def toggleButton():
    global recording
    recording = not recording
    window['Record'].update(disabled=recording)
    window['Close'].update(disabled=recording)
    window['Convert to MP4'].update(disabled=recording)
    window['Downscale'].update(disabled=recording)
    window['Browse'].update(disabled=recording)
    window['Stop'].update(disabled=not recording)


# Variables and stuffs
ffmpegPath = resource_path('ffmpeg.exe')
location = os.path.join(os.getcwd(), 'video.mkv')
recording = False


sg.theme('SystemDefault')
# All the stuff inside your window.
layout = [[sg.Text('Simple Screen Recorder', font=("Helvetica", 13))],
          [sg.Text('Please click \'Help\' button if you\'re first using this program.')],
          [sg.Text('File location: '), sg.Text(
              location + ' (or .mp4)', key='filelocation'), sg.Button('Browse'), sg.Button('View')],
          [sg.Text('Resolution: '), sg.Combo(
              getMaxRes(), default_value='Default', key='res'), sg.Text('Quality: '), sg.Slider(
              (1, 100), resolution=10, orientation='horizontal', default_value='60', key='quality')],
          [sg.Button('Convert to MP4'), sg.Button('Downscale'), sg.Checkbox('Remove audio', key='removeaudio')],
          [sg.Button('Record'), sg.Button('Stop', disabled=True), sg.Button('Help'), sg.Button('Close')]]

# Create the Window
window = sg.Window('Simple Screen Recorder', layout, finalize=True)
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()

    if event == 'Browse':
        new_location = sg.popup_get_file(
            'Browse', save_as=True, file_types=(('MKV', '*.mkv'),), default_extension="mkv", default_path=location)
        if new_location != None:
            location = new_location
            window['filelocation'].update(location)

    if event == 'View':
        os.startfile(os.path.split(location)[0])

    if event == 'Convert to MP4 from MKV':
        file = sg.popup_get_file('Open an MKV file', file_types=(
            ('MKV', '*.mkv'),), default_extension="mkv")

        if file != None:
            if os.path.isfile(file) == False:
                sg.popup_ok('File does not exist.')
            else:
                convert = subprocess.Popen(
                    ffmpegPath + ' -i \"'+file+'\" -codec copy -y \".'+str.split(file, '.mkv')[0]+'.mp4\"', shell=True, stdin=subprocess.PIPE)
                while convert.poll() is None:
                    pass
                os.remove(file)
                sg.popup_ok('Done')
                os.startfile(os.path.split(file)[0])

    if event == 'Downscale':
        file = sg.popup_get_file('Open a video file', file_types=(
            ('Supported video files', '*.mp4 *.mkv *.mov'),),)

        if file != None:
            if os.path.isfile(file) == False:
                sg.popup_ok('File does not exist.')
            else:
                if file.find('.mkv') != -1:
                    new_file = file.replace('.mkv', '_downscaled.mp4')
                elif file.find('.MKV') != -1:
                    new_file = file.replace('.MKV', '_downscaled.mp4')
                elif file.find('.MP4') != -1:
                    new_file = file.replace('.MP4', '_downscaled.mp4')
                elif file.find('.mp4') != -1:
                    new_file = file.replace('.mp4', '_downscaled.mp4')
                elif file.find('.mov') != -1:
                    new_file = file.replace('.mov', '_downscaled.mp4')
                elif file.find('.MOV') != -1:
                    new_file = file.replace('.MOV', '_downscaled.mp4')

                process = ffmpegPath + ' -i \"' + file + '\" -crf ' + getQuality() + ' -vcodec libx264 ' + ('-an ' if values['removeaudio'] == True else '') + '-preset ultrafast -vf \"mpdecimate, scale=-1:' + \
                    getRes() + '\" -y \"' + new_file + '\"'
                convert = subprocess.Popen(
                    process, shell=True, stdin=subprocess.PIPE)
                while convert.poll() is None:
                    pass
                sg.popup_ok('Done')
                os.startfile(os.path.split(new_file)[0])

    if event == 'Record':
        process = ffmpegPath + ' -f gdigrab -i desktop -crf '+getQuality()+' -pix_fmt yuv420p -vcodec libx264 -preset ultrafast -vf \"mpdecimate, scale=-1:' + getRes() + '\" -y \"' + \
            location + '\"'
        print(process)
        if os.path.isfile(location) or os.path.isfile(location.replace('mkv', 'mp4')):
            overwrite = sg.popup_yes_no('File exists. Overwrite?')
            if overwrite == 'Yes':
                toggleButton()
                ffmpeger = subprocess.Popen(
                    process, shell=True, stdin=subprocess.PIPE)
            else:
                print('no')

        else:
            toggleButton()
            ffmpeger = subprocess.Popen(
                process, shell=True, stdin=subprocess.PIPE)

    def stopRec(toggle=True):
        global recording
        if toggle == True:
            toggleButton()
        ffmpeger.stdin.write('q'.encode("GBK"))
        ffmpeger.communicate()
        recording = False
        convert = subprocess.Popen(
            ffmpegPath + ' -i \"'+location+'\" -codec copy -y \"'+location.replace('.mkv', '.mp4')+'\"', shell=True, stdin=subprocess.PIPE)
        while convert.poll() is None:
            pass
        os.remove(location)

        sg.popup_ok('Done')
        os.startfile(os.path.split(location)[0])

    if event == 'Stop':
        stopRec()

    if event == 'Help':
        sg.popup_ok(
            'Created by Link from HCMUT \n - The program saves video in MKV extension to prevent unexpected interruption. After the recording stopped, the program will automatically convert into MP4 and delete the MKV file. \n - If the program exit unexpectedly, you can click on \'Convert to MP4\' to convert MKV into MP4.\n - \'Downscale\' process seems stucked but can be seen in console log, please be patient when using it.', title='Help')

    if event == sg.WIN_CLOSED or event == 'Close':  # if user closes window or clicks cancel
        if recording:
            stopRec(toggle=False)
        break


window.close()
