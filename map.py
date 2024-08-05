import zipfile
from collections import defaultdict

import folium
from fastkml import kml

kmz = zipfile.ZipFile("./not_bike_paths")
kml_content = kmz.open("doc.kml", "r").read()

k = kml.KML()
k.from_string(kml_content)

# Extract coordinates by placemark type (name)
objects = defaultdict(list)

for document in k.features():
    for folder in document.features():
        for placemark in folder.features():
            if placemark.geometry:
                if placemark.geometry.geom_type == 'LineString':
                    objects[placemark.name+'LineString'].append(list(
                        [(pt[0], pt[1]) for pt in placemark.geometry.coords]))
                elif placemark.geometry.geom_type == 'Point':
                    objects[placemark.name+'Point'].append((placemark.geometry.y, placemark.geometry.x))

print(objects.keys())

colors = ['blue', 'red', 'green', 'orange']

# Create Folium map
mapit = folium.Map(location=[49.1659, -123.9401], zoom_start=12) 
for i, (name, name_objects) in enumerate(objects.items()):
  if name.endswith('LineString'):
    for obj in name_objects:
      locations = [(lat, lon) for (lon, lat) in obj]
      folium.PolyLine(
        locations=locations, 
        color=colors[i%4],
        tooltip=name,
        weight=2.5,
        opacity=1
      ).add_to(mapit)      
  elif name.endswith('Point'):
    for obj in name_objects:
      folium.CircleMarker(
            location=(obj[0], obj[1]),
            radius=3,
            tooltip=name,
            color=colors[i%4],
            fill=True,
            fill_color=colors[i%4],
            fill_opacity=0.6
        ).add_to(mapit)

mapit.save('index.html')