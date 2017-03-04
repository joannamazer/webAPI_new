import traffic
import directions
import json
import gmplot

def intro():
    currentLocation = raw_input("Current Location Address: ")
    destination = raw_input("End Destination Address: ")
    currentLocation = '4711 Ravenna AVE NE, Seattle, WA 98105'    # temporary hardcoded location
    destination =  '3900 E Stevens Way NE, Seattle, WA 98105'     # temporary hardcoded destination
    print(" -- Routing from \"" + currentLocation + "\" to \"" + destination + "\"\n")
    start_coords = traffic.address_to_coords(currentLocation)
    end_coords = traffic.address_to_coords(destination)
    print 'start coordinates' + str(start_coords)
    print 'end coordinates' + str(end_coords) + '\n'
    return {'start': start_coords, 'end': end_coords}


def export_to_JSON(dictionary, fileName):
    with open(fileName, 'w') as outfile:
        json.dump(  dictionary,
                    outfile,
                    sort_keys=True,
                    indent=4,
                    ensure_ascii=False  )

def plot_coords(latitudes, longitudes, node_types, zoom, plotfile):
    gmap = gmplot.GoogleMapPlotter(latitudes[0], longitudes[0], zoom)
    # gmap.plot(latitudes, longitudes, 'cornflowerblue', edge_width=10)
    counter = 0
    waze_coordinates = [[] for i in range(2)]
    google_coordinates = [[] for i in range(2)]

    for i in node_types:
        if (i == 'WAZE'):
            waze_coordinates[0].append(latitudes[counter])
            waze_coordinates[1].append(longitudes[counter])
        else:
            google_coordinates[0].append(latitudes[counter])
            google_coordinates[1].append(longitudes[counter])
        counter = counter + 1
    gmap.scatter(waze_coordinates[0], waze_coordinates[1], 'r', marker=True)
    gmap.scatter(google_coordinates[0], google_coordinates[1], 'g', marker=True)
    gmap.draw(plotfile)
