import time
#import pygetwindow as gw
from openai import OpenAI
from mistralai import Mistral
from anthropic import Anthropic
import os
import subprocess

clientopenai = OpenAI()
clientanthropic = Anthropic()


# Gets title (improved performance if it's obvious no procrastinating)
# Could be moved to a separate file
def read_title():
        # Get the active window ID using xdotool
    try:
        active_window_id = subprocess.check_output(['xdotool', 'getactivewindow']).strip()
        
        # Get the window name using xprop
        if active_window_id:
            return subprocess.check_output(['xprop', '-id', active_window_id, 'WM_NAME']).strip().decode('utf-8').split(' = ', 1)[1].strip('"')
        else:
            return False
        # Decode the byte string and remove the 'WM_NAME' part
        



    except subprocess.CalledProcessError:
        return None

# Gets all content
def read_content():

    # Ask for content using ActivityWatch?
        # Recall: Export Bucket, or using Rest API, or using
    return "youtube.com, Ethoslab"


def is_productive(content, service):
    
    # response = clientopenai.chat.completions.create(
    #     model = "gpt-4o-mini",
    #     messages=[
    #     {"role": "system", "content": "I am a machine learning engineer. Please determine if a given activity is productive or not by looking at currently open window titles. Please reply only with 'Productive', 'Not productive' or 'Unsure'. Thanks :-)"},
    # ]
    # )

    # print(response.choices[0].message())

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
    all_content = set()
    while True:
        content = read_title()
        if content and not content in all_content:
            all_content.add(content)
            if not is_productive(content, "Claude"):
                kill_window()

        time.sleep(5)
