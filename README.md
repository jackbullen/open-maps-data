# open maps data

Reference information about geographic information processing with Python, HTML+JS, and PostGIS.

## Scripts

### [map.py](./map.py)

Opens a compressed KML file (KMZ) with the Python standard library [zipfile](https://docs.python.org/3/library/zipfile.html). Then uses two third-party libraries. Read the KML content with [fastkml](https://pypi.org/project/fastkml/) and create a map with [folium](https://pypi.org/project/folium/). A defaultdict from Python standard library [collections](https://docs.python.org/3/library/collections.html) is used to simplify processing.

### [list_geometries.py](./list_geometries.py)

KML files contain structured geographic information. This script prints out the various documents and folders in a KML file along with the number of different fastkml data objects present in each directory.

### [bikemap.py](./bikemap.py)

The `nanaimo_transportation.kmz` file contains a folder called BIKE_ROUTES. In this folder are several [pygeoif](https://github.com/cleder/pygeoif) [GeometryCollection objects](https://github.com/cleder/pygeoif/blob/develop/pygeoif/geometry.py#L984) (likely the kml does not contain GeometryCollection objects, this is just how it is parsed by this library, since in their documentation they state that GeometryCollection type is non-standard in GIS applications). Each of these collections contains two items: a Point and a LineString. Not sure what the points represent since the routes are just lines.

## Data

### [nanaimo_transportation.kmz](./nanaimo_transportation.kmz)
Source: [nanaimo.ca/open-data-catalogue](https://www.nanaimo.ca/open-data-catalogue)

There are a few items at the above website that provide this file (BikeRoutes and Intersections being two). It contains several folders

- Bike routes: 575 GeometryCollection
- Crosswalks: 1370 LineString
- Intersections: 3405 Point
- Laneways: 666 LineString
- Road Centerlines: 4205 GeometryCollection and 3 MultiPoint
- Sidewalks: 4414 LineString and 41 MultiLineString
- Truck Routes: 312 GeometryCollection
  
