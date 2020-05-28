limit100 = "&limit=100"

help_text = "This program can use 2 methods to fetch a list of map IDs that you can then paste in your server controller.\n\n\
	- First one is an api call that is equal to a research on mania-exchange. You can select your parameters, the ordering, and the program will give you the x amount of maps desired.\n\n\
	- Second one is based on random number generation. It randomly picks maps from the database as long as they fit your criterias.\n\n\
\
The api call ignore the award count, as you can choose to order the search result by a whole set of options including awards. If you use the random method, the \nordering is ignored.\n\n\
Calling the API is better for higly specific research parameters (high award \ncount, envimix, long maps of a specific style...) while using the random method \ngives you a nice un-predictable result and may give you access to hidden gems (as well as a pile of shit)"

ordering = {
	"Uploaded_newest" : "&priord=2",
	"Uploaded_oldest" : "&priord=3",
	"Trackname_alphabetical" : "&priord=0",
	"Authorname_alphabetical" : "&priord=1",
	"Updated_newest" : "&priord=4",
	"Updated_oldest" : "&priord=5",
	"Activity_most_recent" : "&priord=6",
	"Activity_least_recent" : "&priord=7",
	"Awards_most" : "&priord=8",
	"Awards_least" : "&priord=9",
	"Comments_most" : "&priord=10",
	"Comments_least" : "&priord=11",
	"Difficulty_easiest" : "&priord=12",
	"Difficulty_hardest" : "&priord=13",
	"Length_shortest" : "&priord=14",
	"Length_longest" : "&priord=15",
	"Trackvalue_lowest" : "&priord=24",
	"Trackvalue_highest" : "&priord=25",
	"Onlinerating_MXKarma_lowest" : "&priord=26",
	"Onlinerating_MXKarma_highest" : "&priord=27",
}

environments = {
    "Stadium" : "&environments=2",
    "Canyon" : "&environments=1",
    "Valley" : "&environments=3",
    "Lagoon" : "&environments=4",
    "Speed" : "&environments=5",
    "Alpine" : "&environments=6",
    "Rally" : "&environments=7",
    "Coast" : "&environments=8",
    "Bay" : "&environments=9",
    "Island" : "&environments=10" ,
    "TMOne Desert" : "&environments=11",
}

vehicles = {
    "StadiumCar" : "&vehicles=2",
    "CanyonCar" : "&vehicles=1",
    "ValleyCar" : "&vehicles=3",
    "LagoonCar" : "&vehicles=4",
    "DesertCar" : "&vehicles=5",
    "SnowCar" : "&vehicles=6",
    "RallyCar" : "&vehicles=7",
    "CoastCar" : "&vehicles=8",
    "BayCar" : "&vehicles=9",
    "IslandCar" : "&vehicles=10" ,
    "SpeedCarv2" : "&vehicles=11",
}

length = {
    "15 secs" : "&length=0",
    "30 secs" : "&length=1",
    "45 secs" : "&length=2",
    "1 min" : "&length=3",
    "1 m 15 s" : "&length=4",
    "1 m 30 s" : "&length=5",
    "1 m 45 s" : "&length=6",
    "2 min" : "&length=7",
    "2 m 30 s" : "&length=8",
    "3 min" : "&length=9",
    "3 m 30 s" : "&length=10",
    "4 min" : "&length=11",
    "4 m 30 s" : "&length=12",
    "5 min" : "&length=13",
    "Long" : "&length=14",
}

lengthop = {
    ">=" : "&lengthop=4",
    "=" : "&lengthop=0",
    "<" : "&lengthop=1",
    ">" : "&lengthop=2",
    "<=" : "&lengthop=3",
}

style = {
    "Default" : "",
    "Race" : "&style=1",
    "Fullspeed" : "&style=2",
    "Tech" : "&style=3",
    "RPG" : "&style=4",
    "LOL" : "&style=5",
    "Press Forward" : "&style=6",
    "Speedtech" : "&style=7",
    "Multilap" : "&style=8",
    "Offroad" : "&style=9",
    "Trial" : "&style=10",
}

track_example = {
   "TrackID":194208,
   "UserID":24940,
   "Username":"chacalouu",
   "UploadedAt":"2020-05-23T14:10:18.267",
   "UpdatedAt":"2020-05-23T14:10:18.267",
   "Name":"STAR LEAGUE #6",
   "TypeName":"Race",
   "MapType":"Race",
   "TitlePack":"TMStadium",
   "Hide":False,
   "StyleName":"Race",
   "Mood":"Day",
   "DisplayCost":2834,
   "ModName":"",
   "Lightmap":7,
   "ExeVersion":"3.3.0",
   "ExeBuild":"2019-11-19_18_50",
   "EnvironmentName":"Stadium",
   "VehicleName":"StadiumCar",
   "UnlimiterRequired":False,
   "RouteName":"Single",
   "LengthName":"1 min",
   "Laps":1,
   "DifficultyName":"Beginner",
   "ReplayTypeName":"None",
   "ReplayWRID":"None",
   "ReplayCount":0,
   "TrackValue":0,
   "Comments":"",
   "Unlisted":False,
   "AwardCount":0,
   "CommentCount":0,
   "MappackID":0,
   "ReplayWRTime":"None",
   "ReplayWRUserID":"None",
   "ReplayWRUsername":"None",
   "Unreleased":False,
   "Downloadable":True,
   "GbxMapName":"STAR LEAGUE #6",
   "RatingVoteCount":0,
   "RatingVoteAverage":0.0,
   "TrackUID":"cqnS3phDcOQokW0uFFGe1nsgrU0",
   "HasScreenshot":False,
   "HasThumbnail":True,
   "HasGhostBlocks":True,
   "EmbeddedObjectsCount":2,
   "AuthorLogin":"chacalouu",
   "IsMP4":True,
   "SizeWarning":False,
   "InPLList":False
}

track_example_light = {
   "TrackID":194208,
   "MapType":"Race",
   "TitlePack":"TMStadium",
   "StyleName":"Race",
   "EnvironmentName":"Stadium",
   "VehicleName":"StadiumCar",
   "LengthName":"1 min",
   "DifficultyName":"Beginner",
   "TrackValue":0,
   "Unlisted":False,
   "AwardCount":0,
   "Unreleased":False,
   "Downloadable":True,
}