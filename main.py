#!/usr/bin/python3.6
# -*-coding:utf-8 -*
import requests as req      #http calls to the api
import re, json, time, sys  #utilities
import tkinter as tk        #the GUI
from enum_values import *   #loading dicts with api values as global variables
import functions as funk    #loads the function relative to database management
import rng_map as rng       #loads the functions for random map picking (with parameters)

general_bg_color = "#f3e9d2"
panel_color = "#c6dabf"
button_color = "#ffe1a8"

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
    final_label.insert(tk.INSERT, string)

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
    # tk.Tk().clipboard_append(string)
    # api_link = "https://tm.mania-exchange.com/tracksearch2/search?api=on"

def create_dropdown(window, enum, name, label_name):
    #the action when something is selected in the dropdown
    def fonction_test(*args):
        enum[name.get()] # changes the StringVar and keeps it somewhere to be retreived
    #grouping the dropdown and a label
    frame = tk.Frame(window, bg=button_color, bd=1, relief="ridge", width=290)
    # frame.config()
    frame.pack(side="bottom")
    # label of the dropdown
    label_title = tk.Label(frame, text=label_name, font=("Impact", 12), bg=button_color, fg="black")
    label_title.pack(side="left")
    #creating the dropdown
    name.set(next(iter(enum))) #sets the default action to the first element of the dict
    popup = tk.OptionMenu(frame, name, *enum)
    popup.config(bg=button_color, font=("Impact", 10))
    name.trace('w', fonction_test)
    popup.pack(side="right")



if __name__ == '__main__' :
    funk.update_db()
    start_time = time.time()
    db = funk.load_database()
    print(f"Database loaded in {round(time.time()-start_time, 1)} seconds, with {len(db)} entries")

    # creating an instance for the main window
    root = tk.Tk()
    root.title("Map ID picker") #setting title
    root.iconbitmap("media/mx_full.ico")
    root.minsize(1052,500)
    root.maxsize(1052,500)
    root.config(background=general_bg_color)

    left_panel = tk.Frame(root, bg=panel_color, bd=1, relief="ridge", width=290)
    left_panel.pack(pady=10, padx=10, side="left")

    MapCount = tk.IntVar(root)
    scale = tk.Scale(left_panel, variable=MapCount, font=("Impact", 11), bg=panel_color, orient='horizontal', from_=10, to=100,
          resolution=1, tickinterval=10, length=350,
          label='Amount of maps desired')
    scale.pack()

    AwardsCount = tk.IntVar(root)
    scale2 = tk.Scale(left_panel, variable=AwardsCount, font=("Impact", 11), bg=panel_color, orient='horizontal', from_=0, to=25,
          resolution=1, tickinterval=5, length=350,
          label='Minimum Award Count (for randomly picked maps)')
    scale2.pack()

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

    buttons = tk.Frame(root, bg=general_bg_color, width=290)
    buttons.pack(pady=10, padx=10)
    # add submit button
    button = tk.Button(buttons, text="Use the API", font=("Impact", 12), bg=button_color, fg="black", command=lambda: search())
    button.pack(padx="10", side="left")
    button2 = tk.Button(buttons, text="BlessRNG", font=("Impact", 12), bg=button_color, fg="black", command=lambda: rng_find(db))
    button2.pack(padx="10", side="right")

    #setting the final string that will be printed
    final_str = tk.StringVar(root)
    final_label = tk.Text(root, bg=panel_color, bd=1, relief="sunken")
    final_label.insert(tk.END, help_text)
    final_label.config(width=293)
    final_label.pack(pady=10, padx=10)

    root.mainloop()

