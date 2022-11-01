import os.path
import sys
import tkinter
import tkinter.messagebox
from shutil import copyfile
from importlib import import_module
import pickle
from os.path import isfile
import nathlib as nlib
import glob

version_name = "snapshot_016"
version_number = 1

nlib.start_logs("latest.log")
nlib.log("Starting file manager ...", "info", "file_manager")

lang_files_to_load = glob.glob("lang/*.lang")

lang_number = len(lang_files_to_load)


def get_system_lang():
    try:
        if sys.platform == "win32":
            ret = 'en_US'
            import ctypes
            import locale
            ret = str(locale.windows_locale[ctypes.windll.kernel32.GetUserDefaultUILanguage()])
        else:
            ret = "en_US"
            ret = str(os.getenv('LANG'))
    except Exception as e:
        print(e)
        ret = "en_US"
    ret = ret[:2]  # [:2] = get 2 first character en_US -> en
    lng = []
    for ele in lang_files_to_load:
        lng.append(ele.replace(".lang", "").replace("lang", ""))
    fn = False
    for _el in lng:
        if nlib.check(ret, _el):
            fn = True
    if fn:
        try:
            with open("lang/" + ret + ".lang", 'r', encoding='utf-8') as tx:
                final = tx.readlines()[0][:-1]
                tx.close()
        except Exception as e:
            print(e)
            final = "English"
    else:
        final = "English"
    return final


def new_settings():
    with open('settings.ini', 'wb') as settings_file:
        setting_list = [get_system_lang(), False, True, False, 0]  # 0 is swatter, 1 pro, 2 ruler
        pickle.dump(setting_list, settings_file)
        settings_file.close()
    return setting_list  # will create new settings, return it, and save it.


def overwrite_better_score(score, name, bziocoins, buy=0, item_list=None):
    if item_list is None:
        item_list = []
    nlib.save([score, name, bziocoins, buy, item_list, version_name], 'save.dat')


def update_save_data():
    data = nlib.load("save.dat")
    score = 0
    try:
        score = data[0]
    except:
        pass
    name = "nobody"
    try:
        name = data[1]
    except:
        pass
    bziocoins = 0
    try:
        bziocoins = data[2]
    except:
        pass
    buy = 0
    try:
        buy = data[3]
    except:
        pass
    item_list = []
    try:
        item_list = data[4]
    except:
        pass
    nlib.save([score, name, bziocoins, buy, item_list, version_name], "save.dat")


def get_better_score():
    try:
        if nlib.load("save.dat")[-1] != version_name:
            tk = tkinter.Tk()
            tk.attributes("-topmost", True)
            tk.withdraw()
            if tkinter.messagebox.askyesno("Update save data", "Your game is running version %s\n"
                                                               "However, it seems your save data is from %s\n"
                                                               "Do you want to try converting your save data ?\n"
                                                               "A backup will be made, but\n"
                                                               "Previous versions may not be able to load your save\n"
                                                               "Proceed ?" % (version_name,
                                                                              str(nlib.load("save.dat")[-1]))):
                copyfile("save.dat", "backup_%s.dat" % (str(nlib.load("save.dat")[-1])))
                update_save_data()
            else:
                quit()
        return nlib.load('save.dat')
    except Exception as e:
        nlib.log("Failed to read save data : %s" % str(e), "error", "file_manager")
        return [0, "nobody", 0, 0, [], version_name]  # Best score, best player name, b coins, 0: Basic Swatter, 1: Swatter Pro 2:
        # B Ruler, and list containing inv


if isfile("settings.ini"):  # load the save
    try:
        settings_list = nlib.load("settings.ini")
        nlib.log("Loaded default settings.", "info", "file_manager")
        _tmp = settings_list[3]
        del _tmp
    except:
        settings_list = new_settings()
        nlib.log("Failed to load settings, recreating them.", "error", "file_manager")
else:
    settings_list = new_settings()
    nlib.log("Default settings file was not found, creating a blank one !", "error", "file_manager")

# load default lang

lang_file_names = {}
for x in range(0, lang_number):
    with open(lang_files_to_load[x], "r", encoding="utf-8") as lang_file:
        name = lang_file.readlines()[0][:-1]  # [:-1] : remove the '\n' character at end of each line [0] = get 1st line
        lang_file.close()
    lang_file_names.update({name: lang_files_to_load[x]})

lang_list = list(lang_file_names.keys())

if not settings_list[0] in lang_file_names:
    # The lang set in options is not in lang/ directory and cannot be loaded
    settings_list[0] = "English"
    nlib.save(settings_list, "settings.ini")

# let's load the lang file !
with open(lang_file_names[settings_list[0]], "r", encoding="utf-8") as lang_txt_file:
    default_lang = []
    lines = lang_txt_file.readlines()  # can only be called once, or it returns empty list
    for x in range(0, len(lines) - 1):
        line_to_append = lines[x + 1].replace("\\n", "\n").replace("\\u20BF", "\u20BF")
        if lines[x + 1][-1] == "\n":  # [-1] = get last character of string
            line_to_append = line_to_append[:-1]  # remove last character
        default_lang.append(line_to_append)

# Note : default_lang is directly imported in main.py when FileManager import is called

nlib.log("All files are loaded.", "info", "file_manager")
