from shutil import copyfile
from importlib import import_module
import pickle
from os.path import isfile
import logging
import nathlib as nlib

nlib.start_logs("latest.log")
nlib.log("Starting file manager ...", "info")

lang_files_to_load = ['en_US', 'fr_FR']

lang_files_names = {"Français": "fr_FR", "English": "en_US"}

lang_list = ['English', 'Français']

lang_number = len(lang_files_to_load)  # Count the number of files entries


# settings loader

def new_settings():
    with open('settings.ini', 'wb') as settings_file:
        setting_list = ["English", False, False]
        pickle.dump(setting_list, settings_file)
        settings_file.close()
    return setting_list  # will create new settings, return it, and save it.


def overwrite_better_score(score, name):
    nlib.save([score, name], 'save.dat')


def get_better_score():
    try:
        return nlib.load('save.dat')
    except Exception as e:
        nlib.log("Failed to read best score file : %s" % str(e), "error")
        return [0, "nobody"]


if isfile("settings.ini"):  # load the save
    try:
        settings_list = nlib.load("settings.ini")
        nlib.log("Loaded default settings.", "info")
        _tmp = settings_list[2]
        del _tmp
    except:
        settings_list = new_settings()
        nlib.log("Failed to load settings, recreating them.", "error")
else:
    settings_list = new_settings()
    nlib.log("Default settings file was not found, creating a blank one !", "error")

for x in range(0, lang_number):
    try:
        copyfile('resources/lang/' + lang_files_to_load[x] + ".txt",
                 "scripts/util/tmp/lang_" + lang_files_to_load[x] + ".py")  # will copy resource/lang file into tmp/lang
    except FileNotFoundError:
        nlib.log("File '" + lang_files_to_load[x] + "' not found in resources folder !", "error")

        copyfile('scripts/util/default/lang/' + lang_files_to_load[x] + '.py',
                 "resources/lang/" + lang_files_to_load[x] + ".txt")

for x in range(0, lang_number):
    try:
        import_module("scripts.util.tmp.lang_" + lang_files_to_load[x])  # load modified lang file
    except:
        copyfile('scripts/util/default/lang/' + lang_files_to_load[x] + '.py',
                 "resources/lang/" + lang_files_to_load[x] + ".txt")
        copyfile('resources/lang/' + lang_files_to_load[x] + '.txt',
                 "scripts/util/tmp/lang_" + lang_files_to_load[x] + ".py")
        nlib.log("Failed to launch lang resource '" + lang_files_to_load[x] + "', using default !", "error")
        import_module("scripts.util.tmp.lang_" + lang_files_to_load[x])
        # will replace modified files with the defaults because errors were found on them.

    finally:
        try:
            scripts = __import__("scripts.util.tmp.lang_" + lang_files_to_load[x])
            exec(lang_files_to_load[x] + " = " + 'scripts.util.tmp.lang_' + lang_files_to_load[x] + '.' +
                 lang_files_to_load[x]
                 + '_lang')
            # load list components as single vars containing info
            exec("nlib.log('Successfully loaded resource " + "\\'" + lang_files_to_load[x] + ".txt" + "\\'" + "." +
                 "', 'info')")
        except:
            nlib.log("Can\'t load resource \'" + lang_files_to_load[x] + "\' !", "error")

nlib.log("All files are loaded.", "info")
