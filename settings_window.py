import tkinter as tk
import tkinter.ttk as ttk
import nathlib as nlib
import webbrowser
import os.path
from tkinter import messagebox
from PIL import Image, ImageTk
import zipfile
import io


def open_settings(global_var, default_lang, settings_list, version_name, lang_list, version_number):
    global_var.set_value("is_update_checked", False)

    def check_update_main():
        try:
            update_result = nlib.get_json_from_url("https://raw.githubusercontent.com/SiniKraft/"
                                                   "NoMoskito/master/update.json")
        except Exception as e:
            nlib.log("Failed to check for updates ! %s" % repr(e).split("(")[0] + ": " + str(e),
                     "error", "settings_window")
            messagebox.showerror(default_lang[58], default_lang[59].format(repr(e))
                                 .split("(")[0] + ": " + str(e))
            return

        def download():
            webbrowser.open(update_result["version"]["latest"]["download"])

        if update_result["version"]["latest"]["number"] > version_number:
            txt_to_config = default_lang[5].format(version_name,
                                                   update_result["version"]["latest"]["name"])
            btn_update2 = ttk.Button(settings_window, text=default_lang[6], command=download)
            btn_update2.place(x=320, y=165)
        else:
            txt_to_config = default_lang[9].format(version_name)
        update_txt.config(text=txt_to_config)

    def save_window_settings():
        global_var.set_value("is_settings_to_save", True)
        settings_window.destroy()

    def reset():
        if messagebox.askyesnocancel(default_lang[60], default_lang[61]):
            nlib.save([0, "nobody", 0, 0, []], 'save.dat')

    global_var.set_value("is_settings_to_save", False)
    settings_window = tk.Tk()
    settings_window.title(default_lang[1])
    # move window center
    fullscreen_mode = settings_list[3]
    winWidth = settings_window.winfo_reqwidth()
    winwHeight = settings_window.winfo_reqheight()
    posRight = int(settings_window.winfo_screenwidth() / 2 - winWidth / 2)
    posDown = int(settings_window.winfo_screenheight() / 2 - winwHeight / 2)
    settings_window.geometry("+{}+{}".format(posRight, posDown))
    settings_window.configure(width=500, height=400)
    settings_window.resizable(0, 0)
    if os.path.isfile("resources.pak"):
        z = zipfile.ZipFile("resources.pak", "r")
        data = z.read("resource_2.png")  # Read in the first image data
        dataEnc = io.BytesIO(data)  # Encode the raw data to be used by Image.open()
        _img = Image.open(dataEnc)  # Open the image
        icon = ImageTk.PhotoImage(_img)  # Make tk compatible image
        data2 = z.read("resource_7.png")
        dataEnc2 = io.BytesIO(data2)
        _img2 = Image.open(dataEnc2)
        img = ImageTk.PhotoImage(_img2)
    else:
        icon = tk.PhotoImage(file="resources/resource_2.png")
        img = tk.PhotoImage(file="resources/resource_7.png")
    settings_window.iconphoto(False, icon)
    variable = tk.StringVar(settings_window)
    variable.set(settings_list[0])
    panel = tk.Label(settings_window, image=img)
    text = ttk.Label(settings_window, text=default_lang[3])
    text.place(x=170, y=50)
    update_txt = ttk.Label(settings_window, text=default_lang[7].format(version_name))
    update_txt.place(x=170, y=125)
    warn_txt = ttk.Label(settings_window, text=default_lang[62])
    warn_txt.place(x=40, y=320)
    btn_update = ttk.Button(settings_window, text=default_lang[8], command=check_update_main)
    btn_update.place(x=40, y=125)
    w = ttk.OptionMenu(settings_window, variable, settings_list[0], *lang_list)
    w.place(x=250, y=50)
    btn = ttk.Button(settings_window, text=default_lang[4], command=save_window_settings)
    btn.place(x=215, y=365)
    btn_del_save = ttk.Button(settings_window, text=default_lang[60], command=reset)
    btn_del_save.place(x=40, y=237)
    var_1 = tk.IntVar()
    if settings_list[2]:
        var_1.set(1)
    else:
        var_1.set(0)
    var_2 = tk.BooleanVar()
    var_2.set(settings_list[3])
    enable_audio_ck = ttk.Checkbutton(settings_window, text=default_lang[16], variable=var_1,
                                      onvalue=1, offvalue=0)
    enable_audio_ck.place(x=40, y=162)
    enable_fullscreen = ttk.Checkbutton(settings_window, text=default_lang[63], variable=var_2,
                                        onvalue=True, offvalue=False)
    enable_fullscreen.place(x=40, y=200)
    panel.pack()
    settings_window.lift()
    settings_window.attributes('-topmost', True)  # note - before topmost
    settings_window.mainloop()
    if global_var.get_value("is_settings_to_save"):
        settings_list[0] = variable.get()
        settings_list[2] = var_1.get()
        settings_list[3] = var_2.get()
        global_var.enable_sound = var_1.get()
        if fullscreen_mode != var_2.get():
            global_var.change_fullscreen = True
        nlib.save(settings_list, "settings.ini")
