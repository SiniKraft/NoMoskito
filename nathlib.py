##########################################################
# This is the nathlib, a lib used by most of my programs #
# You are free to use it                                 #
##########################################################
# Instructions : Import nathlib like this :              #
# 'import nathlib as nlib', will work if nathlib.py is   #
# where your script is.                                  #
# To use nathlib in your scripts, do as the following :  #
# 'nlib.func(args)' where func is the function you want  #
# to use and args the arguments you need to put into.    #
##########################################################
# Thank you, don't forget to see 'github.com/SiniKraft' !#
##########################################################
# This work is licensed under the                        #
# Creative Commons Attribution 4.0 International License.#
# To view a copy of this license, visit                  #
# http://creativecommons.org/licenses/by/4.0/ or send a  #
# letter to Creative Commons, PO Box 1866, Mountain View #
# CA 94042, USA.                                         #
##########################################################

import pickle
import logging
import datetime
import json
import urllib.request
import sys

# nathlib version :
NATHLIB_VERSION = "1.0.011"


def setup_exception_handler():
    from tkinter import messagebox, Tk

    def showerror(type, content, tb):
        root = Tk()
        root.withdraw()
        messagebox.showerror("An error occurred", "{}: {}".format(repr(content).split("(")[0], content))
        root.destroy()

    sys.excepthook = showerror


def write_file(to_write, directory, add_backspace=False, overwrite=False):
    if not overwrite:
        with open(directory, "a") as file:
            if add_backspace:
                file.write("\n")
            file.write(to_write)
            file.close()
    else:
        with open(directory, "w+") as file:
            if add_backspace:
                file.write("\n")
            file.write(to_write)
            file.close()


def import_m(module):
    """Will simply import a module into a var
    Usage : pygame = import_m("pygame")"""
    return __import__(module)


def save(data_to_save, target):
    """Will save a python object in binary format
    Usage : save(my_var, "my_var.dat")"""
    with open(target, 'wb') as file:
        pickle.dump(data_to_save, file)
        file.close()


def collision(sprite1, sprite2):
    """Used to check between 2 pygame sprites rects if they collides
    Usage : if collision(sprite1.rect, sprite2.rect): [...]"""
    if sprite2.right < sprite1.left:
        return False
    if sprite2.bottom < sprite1.top:
        return False
    if sprite2.left > sprite1.right:
        return False
    if sprite2.top > sprite1.bottom:
        return False
    return True


def load(directory):
    """Will load a binary file into python object
    Usage : my_loaded_var = load("my_saved_var.dat")"""
    with open(directory, 'rb') as loaded_file:
        file = pickle.load(loaded_file)
        loaded_file.close()
    return file  # will load file in the directory specified and return it.


def start_logs(filename):
    """Start a basic logging configuration
    Usage : start_logs("latest.log")"""
    logging.basicConfig(filename=filename, format='[%(asctime)s][%(levelname)s/%(name)s]: %(message)s',
                        level=logging.DEBUG, datefmt='%H:%M:%S')


def get_date(date_type):
    """Will return desired date, useful !
    Warning : will return nothing if the argument isn't correct !
    usage : my_value = get_date("date_time_str")"""
    now = datetime.date.today()
    time_tmp = datetime.datetime.now()
    if date_type == "day":
        return now.day
    elif date_type == "year":
        return now.year
    elif date_type == "month":
        return now.month
    elif date_type == "date_str":
        return str(now.day) + "/" + str(now.month) + "/" + str(now.year)
    elif date_type == "date_list":
        return [now.day, now.month, now.year]
    elif date_type == "date":
        return now
    elif date_type == "hour":
        return time_tmp.hour
    elif date_type == "minute":
        return time_tmp.minute
    elif date_type == "second":
        return time_tmp.second
    elif date_type == "time":
        return str(time_tmp.hour) + ":" + str(time_tmp.minute) + ":" + str(time_tmp.second)
    elif date_type == "time_list":
        return [time_tmp.hour, time_tmp.minute, time_tmp.second]
    elif date_type == "date_time_str":
        return str(now.day) + "/" + str(now.month) + "/" + str(now.year) + " " + str(time_tmp.hour) + ":" + \
               str(time_tmp.minute) + ":" + str(time_tmp.second)
    return None


def log(message, level, name="main"):
    """Will print a log and save it into a file
    Usage : log("This is an error", "error")"""
    if level == "debug":
        logging.debug(message)
    elif level == "info":
        logging.info(message)
    elif level == "warn":
        logging.warn(message)
    elif level == "error":
        logging.error(message)
    elif level == "critical":
        logging.critical(message)
    print("[%s][%s/%s]: %s" % (get_date("time"), level.upper(), name, message))


def check(value, filter_in):
    """Will check if string contains only characters of filter_in string
    Usage : my_check = check("abc", "abcdefghij")
    can also be used in if condition"""
    for letter in value:
        if letter not in filter_in:
            return False
    return True


def get_json_from_url(url_in):
    """Will load a json from url and convert it as python dictionary
    Usage : my_dict = get_json_from_url("https://my_json")"""
    with urllib.request.urlopen(url_in) as url:
        return json.loads(url.read().decode())


def save_json(dict_in, directory):
    """Will write txt file containing the json loaded from a python dictionary
    Usage : save_json(my_dict, "my_json.json")"""
    write_json = json.dumps(dict_in, indent=4)
    with open(directory, "w+") as file:
        file.write(write_json)
        file.close()  # create json


def load_json(directory):
    """Will load json from a file
    Usage : my_new_dict = load_json(my_json.json)"""
    with open(directory, "r") as file:
        data = json.load(file)
        file.close()
    return data
