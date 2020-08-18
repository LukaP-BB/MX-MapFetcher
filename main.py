#!/usr/bin/python3.6
# -*-coding:utf-8 -*
# coding: utf8
import time
import requests as req      #http calls to the api
import re, json, time, sys, os  #utilities
import tkinter as tk        #the GUI
import tkinter.filedialog as tkfd
from enum_values import *   #loading dicts with api values as global variables
import functions as funk    #loads the function relative to database management
import rng_map as rng       #loads the functions for random map picking (with parameters)

general_bg_color = "#f3e9d2"
panel_color = "#c6dabf"
button_color = "#ffe1a8"
button_font = "Bahnschrift Condensed"
font_params = (button_font, 15)
slider_font = (button_font, 13)
dropdown_font = (button_font, 13)
menu_bg_color = "#bad2db"

def set_maps_dir(folder_path, but=None):
    filename = tkfd.askdirectory()
    folder_path.set(filename)
    if not os.path.exists("userdata") :
        os.mkdir("userdata")

    try :
        with open("userdata/settings.json", "r+") as setup_file :
            options = json.load(setup_file)
    except FileNotFoundError :
        options = {"dl_folder" : ""}

    if len(filename) > 0 :
        with open("userdata/settings.json", "w+") as setup_file :
            options["dl_folder"] = folder_path.get()
            json.dump(options, setup_file)
        if but != None :
            but.pack()

def quit_setup(frame):
    frame.destroy()

def startup_checks():
    try :
        with open("userdata/settings.json", "r") as userdata :
            options = json.load(userdata)
            print(f"Folder where maps will be downloaded : {options['dl_folder']}")
    except :
        setup = tk.Tk()
        folder_path = tk.StringVar(setup)
        setup.title("Setup") #setting title
        setup.iconbitmap("media/mx_full.ico")
        setup.config(background=panel_color)
        text = tk.Label(setup, text="First time launching the program ?\n Please setup your map folders were the maps will be downloaded",
                        font=font_params, bg=button_color, fg="black")
        text.pack(pady="10", padx="10")
        button = tk.Button(setup, text="Setup Your maps folder", font=font_params, bg=button_color, fg="black", command=lambda: set_maps_dir(folder_path, button_next))
        button.pack(padx="10", pady="10", expand="True")
        button_next = tk.Button(setup, text="Go to the main program", font=font_params, bg=button_color, fg="black", command=lambda: quit_setup(setup))
        button_next.pack(padx="10", pady="10", expand="True")
        button_next.pack_forget()
        setup.mainloop()


def clean_name(mapname):
    """cleans mapname formatting, takes a string, returns a string"""
    mapname = re.sub("\$[wnoitsgz\$]|\$...|[\<\>\:\"\/\|\?\*]", "", mapname)
    return mapname

def gib_name(file) :
    """takes a path to a gbx file and returns the name of the map"""
    if os.path.splitext(file)[1] != ".gbx" :
        return False
    with open(file, "rb") as gbx_file : #reads file content as bytes
        content = gbx_file.read()
    content = list(content)
    header = ""
    for a in range(2000) :
        #reads the first 2000 chars of the gbx header
        header += chr(content[a]) #chr returns a unicode char from it's code
    #extracts the track name from the header
    t_name = re.search('name="(.*)" author=', header).group(1)
    return clean_name(t_name)

def rename_file(old_f, new_f) :
    try :
        os.rename(old_f, new_f)
    except FileExistsError:
        try :
            n = int(re.search(".*\((\d+)\).gbx", new_f).group(1))
            n+=1
        except AttributeError as e :
            n = 1
        new = gib_name(old_f)
        new =os.path.join(os.path.dirname(new_f), f"{new}({n}).gbx")
        rename_file(old_f, new)


def dl_maps():
    web_site = Web_Site.get()
    web_site = "tm.mania-exchange.com"
    map_list = json.loads(Map_List.get())
    map_folder = Map_Folder.get()
    # print(map_list, map_folder)
    i = 0
    final_label.insert(tk.INSERT, "downloading maps")
    for map_id in map_list :
        i+=1
        dl = f"https://{web_site}/tracks/download/{map_id}"
        with open(f'{map_folder}/{map_id}.gbx', 'wb') as map_file:
                response = req.get(dl, stream=True)
                if not response.ok:
                    print (response)
                for block in response.iter_content(1024):
                    if not block:
                        break
                    map_file.write(block)

    for filename in os.listdir(map_folder) :
        old = os.path.join(map_folder,filename)
        mapname = gib_name(os.path.join(map_folder, filename))
        if mapname :
            new = os.path.join(map_folder, f"{mapname}.gbx")
            rename_file(old, new)

    final_label.insert(tk.INSERT, f"\n\nMaps downloaded to {map_folder}")
    dl_button.pack_forget()

def rng_find(db):
    op = int(lengthop[Operator.get()][10])
    if op == 0 :
        len1 = Length.get()
        len2 = Length.get()
    elif op == 1 or op == 3 :
        len2 = Length.get()
        len1 = "15 secs"
    elif op == 2 or op == 4 :
        len1 = Length.get()
        len2 = "Long"

    parameters = rng.define_parameters(
        car=Vehicles.get(),
        envi=Environment.get(),
        len1=len1,
        len2=len2,
        style=Style.get(),
        awards=AwardsCount.get(),
        )
    # print(parameters)
    string = rng.look4map(db,map_amount=MapCount.get(), parameters=parameters)
    final_label.delete("1.0", tk.END)
    final_label.insert(tk.INSERT, string[0])

    Map_List.set(json.dumps([result for result in string[1]]))
    dl_button.pack()

def search():
    # the link for the api call
    link = tk.StringVar()
    link.set("https://tm.mania-exchange.com/tracksearch2/search?api=on")
    final_link = (
        link.get()
        +length[Length.get()]
        +lengthop[Operator.get()]
        +vehicles[Vehicles.get()]
        +style[Style.get()]
        +environments[Environment.get()]
        +ordering[Ordering.get()]
        +f"&limit={MapCount.get()}"
        )
    # print(final_link)
    result = req.get(final_link)
    js = json.loads(result.text)
    found = False
    string = "//mx add "
    for result in js["results"] :
        found = True
        string += f"{result['TrackID']} "
    string+="\n\n"
    for result in js["results"] :
        string += f"{result['Name']} by {result['Username']} with {result['AwardCount']} awards\n"

    if found :
        final_str.set(string)
    else :
        final_str.set("No map found")
    final_label.delete("1.0", tk.END)
    final_label.insert(tk.INSERT, final_str.get())

    Map_List.set(json.dumps([result["TrackID"] for result in js["results"]]))
    dl_button.pack()

def create_dropdown(window, enum, name, label_name):
    #the action when something is selected in the dropdown
    def fonction_test(*args):
        enum[name.get()] # changes the StringVar and keeps it somewhere to be retreived
    #grouping the dropdown and a label
    frame = tk.Frame(window, bg=button_color, bd=1, relief="ridge", width=290, height=40)
    # frame.config( )
    frame.pack(side="bottom", anchor="w", expand=False, fill=None,)
    frame.pack_propagate(False)
    # label of the dropdown
    label_title = tk.Label(frame, text=label_name, font=font_params, bg=button_color, fg="black")
    label_title.pack(side="left")
    #creating the dropdown
    name.set(next(iter(enum))) #sets the default action to the first element of the dict
    popup = tk.OptionMenu(frame, name, *enum)
    popup.config(bg=button_color, font=dropdown_font)
    popup["menu"].config(bg=menu_bg_color)
    name.trace('w', fonction_test)
    popup.pack(side="right")

def make_top_menu() :
    Top_Menu = tk.Frame(root, bg=menu_bg_color,  bd=1, relief="ridge", width=1052, height=30)
    Top_Menu.pack(side="top", anchor="w")
    Top_Menu.pack_propagate(False)

    Setting = tk.StringVar()
    Setting.set("Settings")

    Button_Settings = tk.Menubutton(Top_Menu, text="Settings")
    Button_Settings.config(bg=button_color, font=dropdown_font)
    Button_Settings.pack(side="left")

    Button_Settings.menu = tk.Menu(Button_Settings, cursor="hand2", tearoff=0)
    Button_Settings["menu"] = Button_Settings.menu
    Button_Settings.menu.config(bg=menu_bg_color, font=dropdown_font)

    folder_path = tk.StringVar(root)
    Button_Settings.menu.add_command(label="Download Folder", command=lambda:set_maps_dir(folder_path))


if __name__ == '__main__' :
    print("Launching program...")
    funk.update_db()
    start_time = time.time()
    db = funk.load_database()
    print(f"Database loaded in {round(time.time()-start_time, 1)} seconds, with {len(db)} entries")
    startup_checks()

    # creating an instance for the main window
    root = tk.Tk()
    root.title("Map ID picker") #setting title
    root.iconbitmap("media/mx_full.ico")
    root.minsize(1052,550)
    root.maxsize(1052,550)
    root.config(background=general_bg_color)

    make_top_menu()

    left_panel = tk.Frame(root, bg=panel_color, bd=1, relief="ridge", width=290)
    left_panel.pack(pady=10, padx=10, side="left")

    MapCount = tk.IntVar(root)
    scale = tk.Scale(left_panel, variable=MapCount, font=slider_font, bg=panel_color, orient='horizontal', from_=10, to=100,
          resolution=1, tickinterval=10, length=300,
          label='Amount of maps desired')
    scale.pack(pady=5, padx=20)

    AwardsCount = tk.IntVar(root)
    scale2 = tk.Scale(left_panel, variable=AwardsCount, font=slider_font, bg=panel_color, orient='horizontal', from_=0, to=25,
          resolution=1, tickinterval=5, length=300,
          label='Minimum Award Count (rng only)')
    scale2.pack(pady=5, padx=20)

    popups = tk.Frame(left_panel, bg=panel_color, width=290)
    popups.pack(pady=10, padx=10)
    # creating control variables and adding the popups
    Length = tk.StringVar(root)
    create_dropdown(popups, length, Length, "Length")
    Operator = tk.StringVar(root)
    create_dropdown(popups, lengthop, Operator, "Operator")
    Vehicles = tk.StringVar(root)
    create_dropdown(popups, vehicles, Vehicles, "Vehicles")
    Style = tk.StringVar(root)
    create_dropdown(popups, style, Style, "Style")
    Environment = tk.StringVar(root)
    create_dropdown(popups, environments, Environment, "Environment")
    Ordering = tk.StringVar(root)
    create_dropdown(popups, ordering, Ordering, "Ordering")

    Map_List = tk.StringVar(root)
    Map_Folder = tk.StringVar(root)
    Web_Site = tk.StringVar(root)
    with open("userdata/settings.json") as setup_file :
        options = json.load(setup_file)
        Map_Folder.set(options["dl_folder"])

    buttons = tk.Frame(root, bg=general_bg_color, width=290)
    buttons.pack(pady=10, padx=10)
    # the buttons generating the map lists
    button = tk.Button(buttons, text="Use the API", font=font_params, bg=button_color, fg="black", command=lambda: search())
    button.pack(padx="10", side="left")
    button2 = tk.Button(buttons, text="BlessRNG", font=font_params, bg=button_color, fg="black", command=lambda: rng_find(db))
    button2.pack(padx="10", side="right")
    # a button to allow download of the map list
    dl_button = tk.Button(buttons, text="Download to your folder", font=font_params, bg=button_color, fg="black", command=lambda:dl_maps())
    dl_button.pack(padx="10", side="right")
    dl_button.pack_forget()

    #setting the final string that will be printed
    final_str = tk.StringVar(root)
    final_label = tk.Text(root, bg=panel_color, bd=1, relief="sunken")
    final_label.insert(tk.END, help_text)
    final_label.config(width=293)
    final_label.pack(pady=10, padx=10)

    root.mainloop()
