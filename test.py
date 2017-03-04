import elevation
import traffic

def main():
    from_address = '4711 Ravenna AVE NE, Seattle, WA 98105'
        # 'University of Washington, Seattle, WA, United States'
        # '4711 Ravenna AVE NE, Seattle, WA 98105'
    to_address = '3900 E Stevens Way NE, Seattle, WA 98195'
        # 'Legend House, Roosevelt Way Northeast, Seattle, WA, United States'
        # '3900 E Stevens Way NE, Seattle, WA 98195'

    start_coords = traffic.address_to_coords(from_address)
    end_coords = traffic.address_to_coords(to_address)

    print start_coords
    print end_coords

    waze_resp = traffic.get_waze_resp(start_coords, end_coords) # raw data from waze website
    route_info = traffic.get_route_info(waze_resp) # processed route data
    route = traffic.get_route(waze_resp)
    traffic.exportToJSON(route, 'raw_route_data.json')
    traffic.plotOnMap(start_coords, route_info)

    ele = elevation.Elevation()
    elevations = ele.getElevations(route)



main()
