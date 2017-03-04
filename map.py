import directions
import traffic
import polyline
import gmplot
import webbrowser
import matplotlib.pyplot as plt
import pprint
from collections import namedtuple
import map_functions


GMAPI_KEY = 'AIzaSyDjLCEDNPFDYj8kzvwWXVaE3VO6ELF45qI'
WAZE_URL = 'https://www.waze.com/'
NUMBER_OF_PATHS = 1
leg_node_array_total = {}
node_attributes = namedtuple('node_attributes', ['lat', 'lon', 'speed', 'node_type'])


#----- WAZE -----#
def get_waze_nodes(complete_waze, parsed_waze):
    waze_link_coordinates  = traffic.get_route(complete_waze)  # waze link coord
    waze_nodes = {}
    waze_nodes_complete = {}
    waze_lat = []
    waze_lon = []
    waze_node_type = []
    waze_node_speed = []
    node = 0

    for i in range(len(waze_link_coordinates)):
        node = node + 1
        waze_nodes[node] = {}
        waze_nodes_complete[node] = {}

        waze_lat.append(waze_link_coordinates[i][0])
        waze_lon.append(waze_link_coordinates[i][1])
        waze_node_speed.append(parsed_waze[node]['speed'])
        waze_node_type.append('WAZE')

        waze_nodes_complete[node]['lat'] = waze_link_coordinates[i][0]
        waze_nodes_complete[node]['lon'] = waze_link_coordinates[i][1]
        waze_nodes_complete[node]['speed'] = parsed_waze[node]['speed']
        waze_nodes_complete[node]['node_type'] = 'WAZE'

    map_functions.export_to_JSON(waze_nodes_complete, 'waze_nodes.json')
    map_functions.plot_coords(waze_lat, waze_lon, waze_node_type, 16, 'waze_nodes.html')
    return waze_nodes_complete



def get_google_nodes(waze_count, route_index):
    g_lat = []
    g_lon = []
    g_node_speed = []
    g_node_type = []

    index = 1
    waze_i = 1
    total_index = 1
    total_node_index = 1

    while (index < waze_count):
        g_start     = [route_index[index].lat, route_index[index].lon]
        g_end       = [route_index[index + 1].lat, route_index[index + 1].lon]
        leg_nodes   = directions.routeInfo(g_start, g_end, GMAPI_KEY)
        leg_size    = len(leg_nodes)

        leg_node_array = {}
        leg_node_index = 1

        for i in leg_nodes:
            if (leg_node_index == 1) or (leg_node_index == waze_count):  # start node of google leg nodes
                leg_node_array[leg_node_index] = route_index[waze_i]     # replace first leg index with waze point
                g_lat.append(route_index[waze_i].lat)
                g_lon.append(route_index[waze_i].lon)

                g_node_speed.append(route_index[waze_i].speed)
                g_node_type.append(route_index[waze_i].node_type)
                waze_i = waze_i + 1
            else:
                g_lat.append(i.lat)
                g_lon.append(i.lon)
                g_speed = 'n/a'
                g_type = 'google'

                g_node_speed.append(g_speed)
                g_node_type.append(g_type)

                g_index = node_attributes(  i.lat,
                                            i.lon,
                                            g_speed,
                                            g_type)

                leg_node_array[leg_node_index]['lat'] = g_index.lat
                leg_node_array[leg_node_index]['lon'] = g_index.lon
                leg_node_array[leg_node_index]['speed'] = g_index.speed
                leg_node_array[leg_node_index]['node_type'] = g_index.node_type

            leg_node_index = leg_node_index + 1
            total_node_index = total_node_index + 1

        for item in leg_node_array:
            leg_node_array_total[total_index] = leg_node_array[item]
            total_index = total_index + 1
        index = index + 1

    if (index == waze_count):
        leg_node_array_total[total_index] = route_index[waze_count]     # replace first leg index with waze point
        g_lat.append(route_index[waze_count].lat)
        g_lon.append(route_index[waze_count].lon)
        g_node_speed.append(route_index[waze_count].speed)
        g_node_type.append(route_index[waze_count].node_type)
    return [g_lat, g_lon, g_node_speed, g_node_type]



def main():
    route = map_functions.intro()

    start_coords    = route['start']
    end_coords      = route['end']
    complete_waze   = traffic.get_waze_resp(start_coords, end_coords)   # raw data from waze as JSON
    parsed_waze     = traffic.get_route_info(complete_waze)    # processed route info as JSON

    map_functions.export_to_JSON(complete_waze, 'waze_complete.json')

    waze_count = parsed_waze['node_count']

    map_functions.export_to_JSON(parsed_waze, 'waze_full_output.json')
    route_index = get_waze_nodes(complete_waze, parsed_waze)

    total_nodes = get_google_nodes(waze_count, route_index)
    g_lat       = total_nodes[0]
    g_lon       = total_nodes[1]
    g_node_speed    = total_nodes[2]
    g_node_type     = total_nodes[3]

    map_functions.plot_coords(g_lat, g_lon, g_node_type, 16, 'total_nodes.html')
    map_functions.export_to_JSON(leg_node_array_total, 'total_nodes.json')

main()
