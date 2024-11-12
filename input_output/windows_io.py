import pygetwindow as gw
import pyautogui

def read_title():
    return gw.getFocusedWindow().title

def kill_window():
    pyautogui.hotkey('ctrl', 'w')
    #gw.getFocusedWindow().close()
    
