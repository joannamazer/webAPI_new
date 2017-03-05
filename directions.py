import texttable as tt  # print as table


class routePoint(object):
    def __init__(   self, inLat, inLon, inSpeed=None, inEle=None, inStart=False,
                    inEnd=False, inType='google'):
        self.lat   = inLat
        self.lon   = inLon
        self.speed = inSpeed
        self.ele   = inEle
        self.start = inStart
        self.end   = inEnd
        self.type  = inType

    def __repr__(self):
        return "<routePoint(lat: %s, lon: %s)>" % (self.lat, self.lon)

    def __str__(self):
        return "<routePoint(lat: %s, lon: %s)>" % (self.lat, self.lon)

    def __getitem__(self, item):
        if (item == 'lat'):
            return self.lat
        elif (item == 'lon'):
            return self.lon
        elif (item == 'speed'):
            return self.speed
        elif (item == 'type'):
            return self.type
        elif (item == 'ele'):
            return self.ele
        else:
            return 'Cannot retrieve value for key (%s)', item


    def display(self):
        print("\n" + repr(self.lat) + "\t" + repr(self.lon) + "\t" + repr(self.ele) +
                "\t" + repr(self.start) + " " + repr(self.end))



def routeInfo(startpnt, endpnt, key, mode='driving', plot=True, plotfile='google_nodes.html'):

    import googlemaps
    import json
    import polyline
    client = googlemaps.Client(key)
    dirResult = client.directions(  startpnt,
                                    endpnt,
                                    mode,
                                    waypoints=None,
                                    alternatives=False,
                                    avoid=None,
                                    language=None,
                                    units="imperial",
                                    region=None,
                                    departure_time='now',
                                    arrival_time=None,
                                    optimize_waypoints=True,
                                    transit_mode=None,
                                    transit_routing_preference=None,
                                    traffic_model='pessimistic' )

    # print json.dumps(dirResult, indent=4, sort_keys=True)

    with open('raw_google.json', 'w') as outfile:
        json.dump(  dirResult,
                    outfile,
                    sort_keys=True,
                    indent=4,)
                    # ensure_ascii=False  )

    #------ initiate all arrays ------#
    routePoints = []    # stores routePoint data structure
    points = []         # for elevation calculation
    latitudes1 = []     # for plotting on map
    longitudes1 = []    # for plotting on map
    samples = 0;

    #------ get lat and lon points from the dictionary ------#
    for item in dirResult[0]['legs'][0]['steps']:
        code = str(item['polyline']['points'])
        poly = polyline.decode(code)

        # for i in poly:
        #     print str(i)

        for coord in poly:
            tmpPoint = routePoint(coord[0], coord[1])
            if (samples == 0):
                tmpPoint.start = True
            routePoints.append(tmpPoint)
            samples = samples + 1
            points.append(coord)
            latitudes1.append(coord[0])
            longitudes1.append(coord[1])

    #------ get elevation points ------#
    eleResult = client.elevation_along_path(points, samples)
    for i in range(0, samples):
        routePoints[i].ele = eleResult[i]['elevation']
        if (i == samples-1):
            routePoints[i].end = True

    #------ plot html map. Saved in mymap.html ------#
    if plot:
        import gmplot
        gmap = gmplot.GoogleMapPlotter(47.6682253, -122.3195193, 16)
        gmap.plot(latitudes1, longitudes1, 'cornflowerblue', edge_width=10)
        gmap.scatter(latitudes1, longitudes1, 'r', marker=True)
        gmap.draw(plotfile)
    return routePoints



def testRoute(startpnt, endpnt, mode, key):
    """Print out latitude, longitude, elevation, for start and end address"""

    start = startpnt
    end = endpnt
    route = routeInfo(start, end, key)

    # import texttable as tt  # print as table
    tab = tt.Texttable()
    x = [[]]                # empty row will have header

    for point in route:
        x.append([point.lat,point.lon,point.ele,point.start,point.end])
    tab.add_rows(x)
    tab.set_cols_align(['r','r','r','r','r'])
    tab.header(['Latitude', 'Longitude', 'Elevation','Start','End'])
    print tab.draw()



startpnt = '4711 Ravenna Ave NE, Seattle, WA 98105'
endpnt = 'University Village, 2666 NE University Village St, Seattle, WA 98105'
mode = 'driving'
key = "AIzaSyDjLCEDNPFDYj8kzvwWXVaE3VO6ELF45qI"
# testRoute(startpnt, endpnt, mode, key)
