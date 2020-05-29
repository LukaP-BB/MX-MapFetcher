import requests

dl = "https://tm.mania-exchange.com/tracks/download/155554"
a = requests.get(dl)
# with open("test.gbx", "w+") as test :
#     test.write(a.text)

with open('test.gbx', 'wb') as handle:
        response = requests.get(dl, stream=True)
        if not response.ok:
            print (response)
        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)