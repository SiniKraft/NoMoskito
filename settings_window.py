import tkinter as tk
import tkinter.ttk as ttk
import nathlib as nlib
import webbrowser


def open_settings(global_var, default_lang, settings_list, version_name, lang_list, version_number):
    global_var.set_value("is_update_checked", False)

    def check_update_main():
        update_result = nlib.get_json_from_url("https://raw.githubusercontent.com/SiniKraft/"
                                               "Space-Escape/master/update.json")

        def download():
            webbrowser.open(update_result["version"]["latest"]["download"])

        if update_result["version"]["latest"]["number"] > version_number:
            txt_to_config = default_lang[5].format(version_name,
                                                   update_result["version"]["latest"]["name"])
            btn_update2 = ttk.Button(settings_window, text=default_lang[6], command=download)
            btn_update2.place(x=40, y=165)
        else:
            txt_to_config = default_lang[9].format(version_name)
        update_txt.config(text=txt_to_config)

    def save_window_settings():
        global_var.set_value("is_settings_to_save", True)
        settings_window.destroy()

    global_var.set_value("is_settings_to_save", False)
    settings_window = tk.Tk()
    settings_window.title(default_lang[1])
    # move window center
    winWidth = settings_window.winfo_reqwidth()
    winwHeight = settings_window.winfo_reqheight()
    posRight = int(settings_window.winfo_screenwidth() / 2 - winWidth / 2)
    posDown = int(settings_window.winfo_screenheight() / 2 - winwHeight / 2)
    settings_window.geometry("+{}+{}".format(posRight, posDown))
    settings_window.configure(width=500, height=400)
    settings_window.resizable(0, 0)
    icon = tk.PhotoImage(file="resources/resource_2.png")
    settings_window.iconphoto(False, icon)
    variable = tk.StringVar(settings_window)
    variable.set(settings_list[0])
    img = tk.PhotoImage(file="resources/resource_7.png")
    panel = tk.Label(settings_window, image=img)
    text = ttk.Label(settings_window, text=default_lang[3])
    text.place(x=170, y=50)
    update_txt = ttk.Label(settings_window, text=default_lang[7].format(version_name))
    update_txt.place(x=170, y=125)
    btn_update = ttk.Button(settings_window, text=default_lang[8], command=check_update_main)
    btn_update.place(x=40, y=125)
    w = ttk.OptionMenu(settings_window, variable, settings_list[0], *lang_list)
    w.place(x=250, y=50)
    btn = ttk.Button(settings_window, text=default_lang[4], command=save_window_settings)
    btn.place(x=215, y=365)
    panel.pack()
    settings_window.mainloop()
    if global_var.get_value("is_settings_to_save"):
        settings_list[0] = variable.get()
        nlib.save(settings_list, "settings.ini")
