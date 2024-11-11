import time
from anthropic import Anthropic
import subprocess
import logging
import os
import tkinter as tk
from tkinter import simpledialog
import json
import threading
from dotenv import load_dotenv
import sys


root = tk.Tk()
root.withdraw()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logging.basicConfig(filename='smack.log', level=logging.info)

load_dotenv(".env")

anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
clientanthropic = Anthropic(api_key=anthropic_api_key)



# Gets title (improved performance if it's obvious no procrastinating)
def read_title():
    try:
        active_window_id = subprocess.check_output(['xdotool', 'getactivewindow']).strip()
        if active_window_id:
            return subprocess.check_output(['xprop', '-id', active_window_id, 'WM_NAME']).strip().decode('utf-8').split(' = ', 1)[1].strip('"')
        else:
            return "Safeword"

    except subprocess.CalledProcessError:
        logging.info("Error in read_title: xdotool command failed (probably no active window/Firefox)")
        return "Safeword"
        

def is_productive(content, service, plans):
    
    response = clientanthropic.messages.create(
        max_tokens = 3,
        model="claude-3-5-sonnet-20241022",
        temperature = 0,
        system = f"I am a machine learning engineer, and today my plans are: {plans}. Please determine if a given activity is productive or not by looking at currently open window titles. Please reply only with 'Productive', 'Not productive' or 'Unsure'.",
        messages=[
        {
            "role": "user", "content": content
        }
    ]
    )

    response = response.content[0].text

    logging.info(response)
    if response == "Productive" or response == "Unsure":
        return True
    elif response == "Not Productive" or response == "Not productive":
        return False
    return True

# Kills current window, maybe display a little icon too?
def kill_window():
    subprocess.run(['xdotool', 'key', 'ctrl+w'])
    pass

# Specifically for when there's many variations
# TODO: Fix this implementation
def safe_words(word):
    safe_word = {"VLC"}
    if "VLC" in word:
        return True
    else:
        return False


def gui():
    # Needs to input and output with other parts.
        # Should initialize is_procrastinating, by prompt engineering the NN. Maybe save prompts when exiting?
        # read_title and read_content for now needn't interact with it.
        # kill_window sort of, but can just call an update in the if statement. Then prompt in bottom right?
    # For now, I know how to do this with tkinter. 
    pass


def load_dictionary(file_path):
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, "r") as file:
            data = json.load(file)  
            if isinstance(data, dict):
                return data
            else:
                return {"Safeword": True}
    else:
        return {"Safeword": True}
    
def save_dictionary(dictionary, file_path):
    if dict:
        with open(file_path, "w") as file:
            json.dump(dictionary, file)

def periodic_save(dictionary, file_path):
    while True:
        logging.info("Saving dictionary")
        save_dictionary(dictionary, file_path)
        time.sleep(20)
    

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    plans = simpledialog.askstring("Daily Plans", "What are your plans for today?")
    logging.info(plans)

    file_path = "whiteblacklist.json"

    whiteblacklist = load_dictionary(file_path)
    save_thread = threading.Thread(target=periodic_save, args=(whiteblacklist, file_path))
    save_thread.start()

    while True:
        content = read_title()
        logger.info(content)
        if content and not content in whiteblacklist and not safe_words(content):
            logging.info("Querying Claude")
            whiteblacklist[content] = is_productive(content, "Claude", plans)
        if  not safe_words(content) and not whiteblacklist[content]:
            logging.info("Killing")
            kill_window()    
        time.sleep(1)

