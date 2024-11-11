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
from appdirs import AppDirs


dirs = AppDirs("Smack", "Smack project")
user_config_path = dirs.user_config_dir
os.makedirs(user_config_path, exist_ok=True)
path = os.path.join(*os.path.split(__file__)[:-1])
self_description = ""
os.chdir(path)

root = tk.Tk()
root.withdraw()
logging.basicConfig(level=logging.INFO)
logging.basicConfig(filename='smack.log', level=logging.info)

env_path = os.path.join(user_config_path, ".env")
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    str = "\"" + simpledialog.askstring("First-time set-up", "Please enter your API key (without quotes)") + "\""
    with open(os.path.join(user_config_path, ".env"), "w") as env_file:
        env_file.write("ANTHROPIC_API_KEY=" + str)
    load_dotenv(env_path)

anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
clientanthropic = Anthropic(api_key=anthropic_api_key)

self_descript_path = os.path.join(user_config_path, "self-description.txt")
if os.path.exists(self_descript_path):
    with open(self_descript_path, "r") as f:
        self_description = f.read()
else:
    self_description = simpledialog.askstring("Self-description", "Please describe yourself (to personalise blocking)")
    with open(self_descript_path, "w") as f:
        f.write(self_description)





# Gets title (improved performance if it's obvious no procrastinating)
def read_title():
    try:
        active_window_id = subprocess.check_output(['xdotool', 'getactivewindow']).strip()
        if active_window_id:
            return subprocess.check_output(['xprop', '-id', active_window_id, 'WM_NAME'], stderr=subprocess.DEVNULL).strip().decode('utf-8').split(' = ', 1)[1].strip('"')
        else:
            return "Safeword"

    except subprocess.CalledProcessError:
        logging.info("Error in read_title: xdotool command failed (probably no active window/Firefox)")
        return "Safeword"


def query_model(content, service, plans):

    response = clientanthropic.messages.create(
        max_tokens = 3,
        model="claude-3-5-sonnet-20241022",
        temperature = 0,
        system = f"{self_description}, and today my plans are: {plans}. Please determine if a given activity is productive or not by looking at currently open window titles. Please reply only with 'Productive', 'Not productive' or 'Unsure'.",
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
    


# Specifically for when there's many variations
# TODO: Fix this implementation
# Return False when it is not in wildcardlist, or is actually false (unproductive)
def query_wildcardlist(word):
    safe_word = {"VLC": True}
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
                logging.info("Creating new dictionary")
                return {"Safeword": True}
    else:
        logging.info("Creating new dictionary")
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

    file_path = os.path.join(user_config_path, "whiteblacklist.json")

    whiteblacklist = load_dictionary(file_path)
    save_thread = threading.Thread(target=periodic_save, args=(whiteblacklist, file_path))
    save_thread.start()

    while True:
        content = read_title()
        if content and not content in whiteblacklist and not query_wildcardlist(content):
            logging.info("Querying Claude")
            whiteblacklist[content] = query_model(content, "Claude", plans)
        if  not query_wildcardlist(content) and not whiteblacklist[content]:
            logging.info("Killing")
            kill_window()
        time.sleep(1)
