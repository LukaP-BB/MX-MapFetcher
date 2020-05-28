# MX-MapFetcher - V 1.0
## What's the point of this program ?
The original idea behind this was to be able to randomly pick maps from [ManiaExchange](https://tm.mania-exchange.com/) and be able to give a command to my server controller (which is PyPlanet) to download a bunch of maps.

This way, by setting a few parameters and pushing a button, I would be able to get 10 to 100 maps at once and download them instantly on my server.

Example :

![Example](https://github.com/LukaP-BB/MX-MapFetcher/blob/master/Capture.PNG)

This was also an excuse to learn tkinter and do my first program with a GUI. It's still ugly but I'll see how I can improve.
## How does it work ?
Two methods are available to retreive maps :
* First method use an API call ([MX api](https://api.mania-exchange.com/)) and acts as a research. You give parameters such as style, length etc.. and you'll get the first page of results. It's great for several needs :
    * Getting the most recent maps
    * Getting maps that are rare (lots of awards, long maps, envimix...)
    * Getting interesting maps thanks to the ordering option such as *activity, awards, comments, difficulty, MX_karma* and so on...
* Second method is based on Random Number Generation. It randomly picks maps from the database as long as they fit your criterias. This method is great to gather random shit and find the occasional gem that might have been unnoticed. The database is auto-updated each time you start the program.
## Installation
Either clone this repository or directlty download the files in a folder of your choice.

As it is, you'll need Python 3 installed on your computer, as well as two modules that may or may not come with the default Python installation :
* Tkinter
* Requests

You can install them with pip :
```
pip install tkinter
pip install requests
```
Then, go to your folder and launch main.py in the console.
```
cd path/to/your/folder/
py -3 main.py
OR
python3 main.py
```
