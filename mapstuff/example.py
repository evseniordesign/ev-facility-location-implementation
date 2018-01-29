import gmplot

gmap = gmplot.GoogleMapPlotter(30.288444, -97.735677, 16)

lat_list =  [30.288444, 30.289]
long_list = [-97.735677, -97.736]

gmap.scatter(lat_list, long_list, 'red', marker=True)

gmap.draw("map.html")
