#!/usr/bin/python3.6
# -*-coding:utf-8 -*
import requests as req
import re, json, time
import sys
import argparse, tkinter as tk
from enum_values import *
import functions as funk
import rng_map as rng

import tkinter.font

def rng_find():
    Length.get()
    parameters = define_parameters(
        car=Vehicles.get(),
        envi=Environment.get(),
        awards=5,
        len1=,
        len2="1 min"
        )
    look4map(parameters=parameters)

def search():
    final_link = (
        link.get()
        +length[Length.get()]
        +lengthop[Operator.get()]
        +vehicles[Vehicles.get()]
        +style[Style.get()]
        +environments[Environment.get()]
        +ordering[Ordering.get()]
        )
    print(final_link)
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
        print(enum[name.get()]) # changes the StringVar and keeps it somewhere to be retreived
    #grouping the dropdown and a label
    frame = tk.Frame(window, bg="#F4A261", bd=1, relief="ridge", width=290)
    # frame.config()
    frame.pack(side="bottom")
    # label of the dropdown
    label_title = tk.Label(frame, text=label_name, font=("Impact", 12), bg="#F4A261", fg="black")
    label_title.pack(side="left")
    #creating the dropdown
    name.set(next(iter(enum))) #sets the default action to the first element of the dict
    popup = tk.OptionMenu(frame, name, *enum)
    popup.config(bg="#F4A261", font=("Impact", 10))
    name.trace('w', fonction_test)
    popup.pack(side="right")



if __name__ == '__main__' :
    start_time = time.time()
    db = funk.load_database()
    print(time.time()-start_time)
    print(len(db))
    # print(db[1])

    # creating an instance for the main window
    root = tk.Tk()
    root.title("Map ID picker") #setting title
    root.iconbitmap("mx_full.ico")
    root.minsize(300,150)
    root.config(background="#2A9D8F")

    # the link for the api call
    link = tk.StringVar()
    link.set("https://tm.mania-exchange.com/tracksearch2/search?api=on")

    left_panel = tk.Frame(root, bg="#F4A261", bd=1, relief="ridge", width=290)
    left_panel.pack(pady=10, padx=10, side="left")

    scale2 = tk.Scale(left_panel, font=("Impact", 11), bg="#F4A261", orient='horizontal', from_=10, to=100,
          resolution=1, tickinterval=10, length=350,
          label='Amount of maps desired')
    scale2.pack()

    scale = tk.Scale(left_panel, font=("Impact", 11), bg="#F4A261", orient='horizontal', from_=0, to=60,
          resolution=1, tickinterval=5, length=350,
          label='Minimu Award Count (for randomly picked maps)')
    scale.pack()

    popups = tk.Frame(left_panel, bg="#F4A261", width=290)
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

    # add submit button
    button = tk.Button(root, text="Get me those map id's !", font=("Impact", 12), bg="#E76F51", fg="black", command=lambda: search())
    button.pack(pady="10")
    #setting the final string that will be printed
    final_str = tk.StringVar(root)
    final_label = tk.Text(root, bg="#E9C46A", bd=1, relief="sunken")
    final_label.insert(tk.END, "Here your string")
    final_label.pack(pady=10, padx=10)

    root.mainloop()

