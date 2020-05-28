#!/usr/bin/python3.6
# -*-coding:utf-8 -*
import requests as req
import re, json, time,csv
import sys
import argparse, tkinter as tk
from enum_values import *
import functions as funk


def update_db():
    """creates the database of all current maps on MX,
    if the file already exists, update the base"""
    start_time = time.time()
    database = load_database()
    print(f"Most recent track : {database[0]['TrackID']}")
    db_size = len(database)
    found = False
    i = 1
    while not found :
        parse_start = time.time()
        api_link = "https://tm.mania-exchange.com/tracksearch2/search?api=on"+limit100
        api_link = page(api_link, i)
        result = req.get(api_link)
        js = json.loads(result.text)
        for result in js["results"] :
            if int(database[0]["TrackID"]) != int(result["TrackID"]) :
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
            else :
                found = True
                break
        parse_end = time.time()
        print(f"Page {i} parsed in {round(parse_end-parse_start, 1)} seconds")
        i += 1

    database = sorted(database, key=lambda result:(int(result["TrackID"])), reverse=True)
    with open("database.csv", "w+") as csv_file :
        writer = csv.DictWriter(csv_file, fieldnames=[key for key in database[0]])
        writer.writeheader()
        for row in database :
            writer.writerow(row)
    print(f"{len(database)-db_size} maps have been added to the database")


def page(link, num):
    link+=f"&page={num}"
    return link

def load_database():
    database = []
    with open("database.csv", "r") as db_file:
        reader = csv.DictReader(db_file)
        for row in reader :
            database.append(row)
        return database

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
        print(f"Page {i} parsed in {round(parse_end-parse_start, 1)} seconds")
        i += 1


def transform_db():
    with open("database.json", "r") as db_file :
        database = json.load(db_file)
    with open("database.csv", "w+") as csv_file :
        writer = csv.DictWriter(csv_file, fieldnames=[key for key in database[0]])
        writer.writeheader()
        for row in database :
            writer.writerow(row)
    return database

if __name__ == "__main__" :
    # print("restoring database...")
    # transform_db()
    print("updating...")
    update_db()