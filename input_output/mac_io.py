import pygetwindow as gw
import pyautogui

def read_title():
    return gw.getFocusedWindow().title

def kill_window():
    pyautogui.hotkey('command', 'w')
    #gw.getFocusedWindow().close() - probably kills whole browser
