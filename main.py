import time
#import pygetwindow as gw
from openai import OpenAI
#import google.generativeai as genai
from mistralai import Mistral
import os
import subprocess

client = OpenAI()

# Gets title (improved performance if it's obvious no procrastinating)
# Could be moved to a separate file
def read_title():
        # Get the active window ID using xdotool
    try:
        active_window_id = subprocess.check_output(['xdotool', 'getactivewindow']).strip()
        
        # Get the window name using xprop
        window_name = subprocess.check_output(['xprop', '-id', active_window_id, 'WM_NAME']).strip()
        
        # Decode the byte string and remove the 'WM_NAME' part
        window_name = window_name.decode('utf-8').split(' = ', 1)[1].strip('"')
        
        return window_name

    except subprocess.CalledProcessError:
        return None

# Gets all content
def read_content():

    # Ask for content using ActivityWatch?
        # Recall: Export Bucket, or using Rest API, or using
    return "youtube.com, Ethoslab"


def is_productive(content, service):
    
    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages=[
        {"role": "system", "content": "I am a machine learning engineer. Please determine if a given activity is productive or not by looking at currently open window titles. Please reply only with 'Productive' or 'Not productive'. Thanks :-)"},
    ]
    )

    print(response.choices[0].message())



    return False

# Kills current window, maybe display a little icon too?
def kill_window():
    #current_window = gw.getActiveWindow()
    #current_window.minimize()
    # This will minimize all of firefox.
    pass


def gui():
    # Needs to input and output with other parts.
        # Should initialize is_procrastinating, by prompt engineering the NN. Maybe save prompts when exiting?
        # read_title and read_content for now needn't interact with it.
        # kill_window sort of, but can just call an update in the if statement. Then prompt in bottom right?
    # For now, I know how to do this with
    pass


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    while True:
        content = read_title()
        print(content)
        # if not is_productive(content, "OpenAI"):
        #     kill_window()
        # if not is_productive(content, "mistral"):
        #     kill_window()
        time.sleep(1)
