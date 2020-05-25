import functions as funk
import random, time
from enum_values import *

start_time = time.time()
db = funk.load_database()
print(f"Loading database in {time.time()-start_time} seconds\n")


map_parameters = {"car" : "stadium", "envi" : "stadium", "awards" : 0, "length" : "15 secs"}

def check_valid(param, enum):
    parameters = {}
    for list_param in enum :
        if str(param).lower() in list_param.lower() :
            return list_param
    if param == None :
        return None
    else :
        print(f"'{param}' has to be one of {[v for v in enum]}")

def define_parameters(car=None, envi=None, awards=0, len1="15 secs", len2="Long"):
    parameters = {}
    parameters["VehicleName"] = check_valid(car, vehicles)
    parameters["EnvironmentName"] = check_valid(envi, environments)
    parameters["length1"] = check_valid(str(len1), length)
    parameters["length2"] = check_valid(str(len2), length)
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

    map_lengths = ["15 secs", "30 secs", "45 secs", "1 min", "1 m 15 s",
        "1 m 30 s", "1 m 45 s", "2 min", "2 m 30 s", "3 min", "3 m 30 s",
        "4 min" , "4 m 30 s", "5 min", "Long"]
    if not (map_lengths.index(parameters["length1"]) <=
        map_lengths.index(map_dict["LengthName"]) <=
        map_lengths.index(parameters["length2"])) :
        return False

    if int(map_dict["AwardCount"]) >= int(parameters["awards"]) :
        return True
    else :
        return False



def look4map(map_amount=20, parameters="default", timeout=20):
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
        if exec_time > timeout :
            loop = False
            if len(list_maps) == 0 :
                print("No map found du to timeout")
            else :
                print(f"Time to find the maps : {exec_time}")

        number = random.randint(0, len(db)-1)
        if number not in list_numbers :
            list_numbers.append(number)
            if check_parameters(db[number], parameters) and db[number]["TrackID"] not in list_maps :
                list_maps.append(db[number]["TrackID"])


        if len(list_maps) == map_amount :
            loop = False
            print(f"Time to find the maps : {exec_time}")

    print(list_maps)
    print(f"{len(list_numbers)} unique maps parsed out of {len(db)}")


if __name__ == "__main__" :
    parameters = define_parameters(car="sta", envi="sta", awards=5, len1=30, len2="1 min")
    print(f"Parameters : {parameters}\n")
    look4map(parameters=parameters)