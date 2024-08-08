import zipfile
from collections import defaultdict

import folium
from fastkml import kml
from fastkml.geometry import Point, LineString

kmz = zipfile.ZipFile("./nanaimo_transportation.kmz")
kml_content = kmz.open("doc.kml", "r").read()

k = kml.KML()
k.from_string(kml_content)

# Extract coordinates by placemark type (name)
bike_routes = defaultdict(list)

for document in k.features():
  for folder in document.features():
    if folder.name == "BIKE_ROUTES": # everthing here is of type GeometryCollection
      for placemark in folder.features():
        if placemark.geometry:
          # GeometryCollection is class with a property called geoms, which is a 
          # generator for other Geometry types
          geoms = [x for x in placemark.geometry.geoms]

          # in this specific kml file folder, there are two Geometry objects in each
          # of these collections, a Point and a LineString
          bike_routes[placemark.name].append({"point": geoms[0], 
                                              "line": geoms[1]})

# Create Folium map
mapit = folium.Map(location=[49.1659, -123.9401], zoom_start=12) 

# Define two functions for adding stuff to the above map

def add_linestring_to_map(linestring: LineString, name: str, color: str, dash_array=None):
  """Adds a folium PolyLine from fastkml LineString to global scoped folium Map object mapit
     Params:
      linestring: fastkml LineString
      name:       Name of the line
      color:      Color of the line
  """
  folium.PolyLine(
    locations=[(x[1], x[0]) for x in linestring.coords], 
    color=color,
    tooltip=name,
    weight=5,
    opacity=1,
    dash_array=dash_array
  ).add_to(mapit)  

def add_point_to_map(point: Point, name: str, color: str):
  """Adds a folium CircleMarker from fastkml Point to global scoped Map object mapit
     Params:
      point: fastkml Point 
      name:  Name of the marker
      color: Color of the marker
  """
  folium.CircleMarker(
        location=(point.y, point.x),
        radius=0.1,# increase radius to see the points...
        tooltip=name,
        color=color,
        fill=False,
    ).add_to(mapit)

# Add the bike routes

for route in bike_routes["Current Bicycle Route"]:
  # vars can be typed, which can make life easier
  point: Point = route['point'] 
  line: LineString = route['line']
  add_point_to_map(point, name="Current", color="green")
  add_linestring_to_map(route['line'], name="Current", color="green")

for route in bike_routes["Proposed Bicycle Route"]:
  point, line = route.values()
  add_point_to_map(point, name="Proposed", color="red")
  add_linestring_to_map(line, name="Proposed", color="red", dash_array="10")

mapit.save('bike_routes.html')