import gmplot

def graph_coordinates(lat_list, long_list, center_lat, center_long, zoom, file="map.html"):
    gmap = gmplot.GoogleMapPlotter(center_lat, center_long, zoom)
    gmap.scatter(lat_list, long_list, 'red', marker=True)
    gmap.draw(file)

def main():
    lat_list =  [30.288444, 30.289]
    long_list = [-97.735677, -97.736]
    graph_coordinates(lat_list, long_list, 30.288444, -97.735677, 16)
    
if __name__ == '__main__':
    main()
