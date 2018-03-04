import gmplot

gmap = gmplot.GoogleMapPlotter(30.288, -97.736, 16)

#gmap.plot([30.288, 2], [-97.736, -97.736], 'cornflowerblue', edge_width=10)
gmap.scatter([(.1 * x) + 30.288 for x in xrange(0, 1000, 1)], [(.1 * x) - 97.736 for x in xrange(0, 1000, 1)], 'red', marker=True)
#gmap.scatter(marker_lats, marker_lngs, 'k', marker=True)
#gmap.heatmap(heat_lats, heat_lngs)

gmap.draw("mymap.html")