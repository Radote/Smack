import time
#import pygetwindow as gw
from openai import OpenAI
from mistralai import Mistral
from anthropic import Anthropic
import os
import subprocess
import re
import json
from Xlib import X, display
import logging

clientopenai = OpenAI()
clientanthropic = Anthropic()
logger = logging.getLogger(__name__)
logging.basicConfig(filename='smack.log', level=logging.INFO)


# Gets title (improved performance if it's obvious no procrastinating)
def read_title():
        
    try:
        active_window_id = subprocess.check_output(['xdotool', 'getactivewindow']).strip()
        if active_window_id:
            return subprocess.check_output(['xprop', '-id', active_window_id, 'WM_NAME']).strip().decode('utf-8').split(' = ', 1)[1].strip('"')
        else:
            return True

    except subprocess.CalledProcessError:
        logging.info("Error in read_title: xdotool command failed (probably no active window/Firefox)")
        return True
        
        # Decode the byte string and remove the 'WM_NAME' part

  
       
    # d = display.Display()
    # root = d.screen().root
    # active_window_id = root.get_full_property(d.intern_atom('_NET_ACTIVE_WINDOW'), X.AnyPropertyType).value[0]

    # if active_window_id:
    #     active_window = d.create_resource_object('window', active_window_id)
    #     window_name = active_window.get_wm_name()
    #     return window_name
    # return None


def is_productive(content, service):
    
    response = clientanthropic.messages.create(
        max_tokens = 5,
        model="claude-3-5-sonnet-20241022",
        temperature = 0,
        system = "I am a machine learning engineer. Please determine if a given activity is productive or not by looking at currently open window titles. Please reply only with 'Productive', 'Not productive' or 'Unsure'.",
        messages=[
        {
            "role": "user", "content": content
        }
    ]
    )

    response = response.content[0].text

    print(response)
    if response == "Productive" or response == "Unsure":
        return True
    elif response == "Not Productive" or response == "Not productive":
        return False


    return False

# Kills current window, maybe display a little icon too?
def kill_window():
    subprocess.run(['xdotool', 'key', 'ctrl+w'])
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
    all_content = {"True": True}
    while True:
        content = read_title()
        logger.info(content)
        if content is True:
            pass
        elif content and not content in all_content:
            all_content[content] = is_productive(content, "Claude")
            if not all_content[content]:
                kill_window()
        elif content and content in all_content:
            if not all_content[content]:
                kill_window()


        time.sleep(5)
