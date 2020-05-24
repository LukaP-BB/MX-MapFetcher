#!/usr/bin/python3.6
# -*-coding:utf-8 -*
import requests as req
import re, json, time
import sys
import argparse, tkinter as tk
from enum_values import *

def page(link, num):
    link+=f"&page={num}"
    return link

def create_db():
    start_time = time.time()
    """creates the database of all current maps on MX,
    if the file already exists, update the base"""
    database = []
    limit = False
    i = 1
    while not limit :
        parse_start = time.time()
        with open("database.json", "r") as db_file :
            try :
                database = json.load(db_file)
            except Exception as e :
                print(f"exception at {i} : \n{e}")
                pass
        api_link = "https://tm.mania-exchange.com/tracksearch2/search?api=on"+limit100
        api_link = page(api_link, i)
        result = req.get(api_link)
        js = json.loads(result.text)
        if len(js["results"]) == 0 :
            end_time = time.time()
            print(f"limit has been reached after {round(end_time - start_time, 1)} seconds and {i} page loaded")
            limit = True
        for result in js["results"] :
            database.append({
                   "TrackID": result["TrackID"],
                   "MapType": result["MapType"],
                   "TitlePack": result["TitlePack"],
                   "StyleName": result["StyleName"],
                   "EnvironmentName": result["EnvironmentName"],
                   "VehicleName": result["VehicleName"],
                   "LengthName": result["LengthName"],
                   "DifficultyName": result["DifficultyName"],
                   "TrackValue": result["TrackValue"],
                   "Unlisted": result["Unlisted"],
                   "AwardCount": result["AwardCount"],
                   "Unreleased": result["Unreleased"],
                   "Downloadable": result["Downloadable"],
                })
        if not limit :
            with open("database.json", "w") as db_file :
                json.dump(database, db_file, indent=1)
        parse_end = time.time()
        print(f"Page {i} parsed in {parse_end-parse_start} seconds")
        i += 1

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

def create_popup(window, enum, name, label_name):
    #the action when something is selected
    def fonction_test(*args):
        # link+=enum[name.get()]
        print(enum[name.get()])
        # return enum[name.get()]
    #grouping the dropdown and a label
    frame = tk.Frame(window, bg="white", bd=1, relief="sunken")
    frame.config(width=290)
    frame.pack()
    # label of the dropdown
    label_title = tk.Label(frame, text=label_name, font=("Calibri", 15), bg="white", fg="black")
    label_title.pack(side="left")
    #creating the dropdown
    name.set(next(iter(enum))) #sets the default action to the first element of the dict
    popup = tk.OptionMenu(frame, name, *enum)
    name.trace('w', fonction_test)
    popup.pack(side="right")



if __name__ == '__main__' :
    create_db()
    # # creating an instance for the main window
    # root = tk.Tk()
    # root.title("Map ID picker") #setting title
    # # base_window.iconbitmap("path/to/file.ico")
    # root.minsize(300,150)
    # root.config(background="white")
    #
    # # the link for the api call
    # link = tk.StringVar()
    # link.set("https://tm.mania-exchange.com/tracksearch2/search?api=on")
    #
    # # creating control variables and adding the popups
    # Length = tk.StringVar(root)
    # create_popup(root, length, Length, "Length")
    # Operator = tk.StringVar(root)
    # create_popup(root, lengthop, Operator, "Operator")
    # Vehicles = tk.StringVar(root)
    # create_popup(root, vehicles, Vehicles, "Vehicles")
    # Style = tk.StringVar(root)
    # create_popup(root, style, Style, "Style")
    # Environment = tk.StringVar(root)
    # create_popup(root, environments, Environment, "Environment")
    # Ordering = tk.StringVar(root)
    # create_popup(root, ordering, Ordering, "Ordering")
    #
    # # add submit button
    # button = tk.Button(root, text="Get me those map id's !", font=("Calibri", 15), bg="grey", fg="black", command=lambda: search())
    # button.pack(pady="10")
    # #setting the final string that will be printed
    # final_str = tk.StringVar(root)
    # final_label = tk.Text(root, bg="white", bd=1, relief="sunken")
    # final_label.insert(tk.END, "Here your string")
    # final_label.pack()
    #
    # root.mainloop()

