import functions as funk
import random, time
import enum_values as EV


def check_valid(param, enum):
    parameters = {}
    for list_param in enum :
        if str(param).lower() in list_param.lower() :
            return list_param
    if param == None :
        return None
    elif param == "" :
        return None
    else :
        print(f"'{param}' has to be one of {[v for v in enum]}")

def define_parameters(car=None, envi=None, style="Default", awards=0, len1="15 secs", len2="Long"):
    parameters = {}
    parameters["VehicleName"] = check_valid(car, EV.vehicles)
    parameters["EnvironmentName"] = check_valid(envi, EV.environments)
    parameters["Min Time"] = check_valid(str(len1), EV.length)
    parameters["Max Time"] = check_valid(str(len2), EV.length)
    parameters["Style"] = check_valid(style, EV.style)
    try :
        if awards >= 0 :
            parameters["awards"] = awards
    except Exception as e :
        print(f"\nYour put '{awards}' as min award count.\n{e}\nAwards set to 0\n")
        parameters["awards"] = 0
    return parameters

def check_parameters(map_dict, parameters):
    if parameters["VehicleName"] == None :
        pass
    elif parameters["VehicleName"] != map_dict["VehicleName"] :
        return False

    if parameters["EnvironmentName"] == None :
        pass
    elif parameters["EnvironmentName"] != map_dict["EnvironmentName"] :
        return False

    if parameters["Style"] == None :
        pass
    elif parameters["Style"] == "Default":
        pass
    elif parameters["Style"] != map_dict["StyleName"] :
        return False

    map_lengths = ["15 secs", "30 secs", "45 secs", "1 min", "1 m 15 s",
        "1 m 30 s", "1 m 45 s", "2 min", "2 m 30 s", "3 min", "3 m 30 s",
        "4 min" , "4 m 30 s", "5 min", "Long"]
    if not (map_lengths.index(parameters["Min Time"]) <=
        map_lengths.index(map_dict["LengthName"]) <=
        map_lengths.index(parameters["Max Time"])) :
        return False

    if int(map_dict["AwardCount"]) >= int(parameters["awards"]) :
        return True
    else :
        return False

def alt_search(db, parameters, map_amount):
    loop_start = time.time()
    list_maps = []
    final_list = []
    for i in range(len(db)) :
        exec_time = round(time.time() - loop_start, 1)
        if check_parameters(db[i], parameters) and db[i]["TrackID"] not in list_maps :
            list_maps.append(db[i]["TrackID"])
    i = 0
    if len(list_maps) >= map_amount :
        while i < map_amount :
            rng = random.randint(0, len(list_maps)-1)
            if list_maps[rng] not in final_list :
                # print(f"{rng}, {len(list_maps)}")
                final_list.append(list_maps[rng])
                i+=1
        return final_list, len(list_maps)
    else :
        return list_maps, len(list_maps)

def look4map(db, map_amount=20, parameters="default"):
    timeout=3
    TO = False
    string = ""
    loop_start = time.time()
    if parameters == "default" :
        print("DEFAULT PARAMETERS")
        parameters = {'VehicleName': 'StadiumCar', 'EnvironmentName': 'Stadium',
                    'length1': '15 secs', 'length2': 'Long', 'awards': 0}
    list_maps = []
    loop = True
    list_numbers = []
    while loop :
        exec_time = time.time() - loop_start
        number = random.randint(0, len(db)-1)
        if number not in list_numbers :
            list_numbers.append(number)
            if check_parameters(db[number], parameters) and db[number]["TrackID"] not in list_maps :
                list_maps.append(db[number]["TrackID"])
        if len(list_maps) == map_amount :
            loop = False
        if exec_time > timeout :
            TO = True
            loop = False
            list_maps, total_maps = alt_search(db, parameters, map_amount)
            string+=f"Only {total_maps} map(s) exist in the database with the desired parameters\n"
    if not TO :
        string+=f"{len(list_numbers)} unique maps parsed out of {len(db)}\n"

    string+=f"Time to find the maps : {round(exec_time, 2)}\n"
    string+="Your search parameters : \n"
    for parameter in parameters :
        string+=f"\t{parameter} : {parameters[parameter]}\n"
    string+="\n//mx add "
    for map in list_maps :
        string += f"{map} "
    return string


def test(db, parameters):
    loop_start = time.time()
    loop = True
    list_maps = []
    list_numbers = []
    stats = {}
    while loop :
        exec_time = round(time.time() - loop_start, 1)
        if exec_time >= 30 :
            loop = False
        number = random.randint(0, len(db)-1)
        stats[exec_time] = len(list_maps)
        if number not in list_numbers :
            list_numbers.append(number)
            if check_parameters(db[number], parameters) and db[number]["TrackID"] not in list_maps :
                list_maps.append(db[number]["TrackID"])
    with open("stats.csv", "w+") as stat_file :
        final_str = ""
        for stat in stats :
            final_str+=f"{stat},{stats[stat]}\n"
        stat_file.write(final_str)


if __name__ == "__main__" :
    start_time = time.time()
    db = funk.load_database()
    print(len(db))
    print(f"Loading database in {time.time()-start_time} seconds\n")
    map_parameters = {"car" : "stadium", "envi" : "stadium", "awards" : 0, "length" : "15 secs"}
    parameters = define_parameters(car="sta", envi="stadium", awards=5, len1=15, len2="long")
    print(f"Parameters : {parameters}\n")
    # test2(db, parameters)
    look4map(parameters=parameters)