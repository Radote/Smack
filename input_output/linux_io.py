import subprocess
import logging

logging.basicConfig(level=logging.INFO)
logging.basicConfig(filename='smack.log', level=logging.info)


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
    except IndexError:
        logging.info("Error in read_title: Split operation failed, possibly invalid format in WM_NAME")
        return "Safeword"

def kill_window():
    subprocess.run(['xdotool', 'key', 'ctrl+w'])
