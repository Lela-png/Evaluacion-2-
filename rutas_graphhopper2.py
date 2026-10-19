import requests
import urllib.parse

geocode_url = "http://localhost:8082/api/1/geocode?"
route_url = "http://localhost:8082/api/1/route?"
key = "766c70b4-b44a-4c7f-9796-5eb3a64e7a0f"      # Replace with your GraphHopper key (column TU_KEY_GRAPHHOPPER)

def geocoding (location, key):
    while location == "":
        location = input("Vuelva a introduccior su ubicacion: ")
    geocode_url = "http://localhost:8082/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q":location, "limit": "1", "key":key})

    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code

    if json_status == 200 and len(json_data["hits"]) != 0:
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]

        if "country" in json_data["hits"][0]:
            country = json_data["hits"][0]["country"]
        else:
            country=""

        if "state" in json_data["hits"][0]:
            state = json_data["hits"][0]["state"]
        else:
            state=""

        if len(state) !=0 and len(country) !=0:
            new_loc = name + ", " + state + ", " + country
        elif len(state) !=0:
            new_loc = name + ", " + country
        else:
            new_loc = name

        print("Geocodificando la API URL para " + new_loc + " (Location Type: " + value + ")\n" + url)
    else:
        lat="null"
        lng="null"
        new_loc=location
        if json_status == 200:
            json_status = 404
            print("Ubicacion no encontrada: " + location)
        else:
            print("Estado de la Geocodificacion de la  API : " + str(json_status) + "\nError message: " + json_data["message"])
    return json_status,lat,lng,new_loc

while True:
    loc1 = input("Ubicacion iniciada: ")
    if loc1 == "salir" or loc1 == "s":
        break
    orig = geocoding(loc1, key)

    loc2 = input("Destino: ")
    if loc2 == "salir" or loc2 == "s":
        break
    dest = geocoding(loc2, key)

    print("=================================================")
    if orig[0] == 200 and dest[0] == 200:
        op="&point="+str(orig[1])+"%2C"+str(orig[2])
        dp="&point="+str(dest[1])+"%2C"+str(dest[2])
        paths_url = route_url + urllib.parse.urlencode({"key":key}) + op + dp
        paths_status = requests.get(paths_url).status_code
        paths_data = requests.get(paths_url).json()
        print("Estado de enrutamiento de la API: " + str(paths_status) + "\nRouting API URL:\n" + paths_url)

        print("=================================================")
        print("Desde " + orig[3] + " to " + dest[3])
        print("=================================================")
        if paths_status == 200:
            km = (paths_data["paths"][0]["distance"])/1000
            meters = paths_data["paths"][0]["distance"]
            sec = int(paths_data["paths"][0]["time"]/1000%60)
            min = int(paths_data["paths"][0]["time"]/1000/60%60)
            hr = int(paths_data["paths"][0]["time"]/1000/60/60)
            print("Distancia viajada: {0:.2f} km / {1:.2f} m".format(km, meters))
            print("Duracion del viaje: {0:02d}:{1:02d}:{2:02d}".format(hr, min, sec))
            print("=================================================")
            for each in range(len(paths_data["paths"][0]["instructions"])):
                path = paths_data["paths"][0]["instructions"][each]["text"]
                distance = paths_data["paths"][0]["instructions"][each]["distance"]
                print("{0} ( {1:.2f} km / {2:.2f} m )".format(path, distance/1000, distance))
            print("=============================================")
        else:
            print("Error: " + paths_data["message"])
            print("*************************************************")
