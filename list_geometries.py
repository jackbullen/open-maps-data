import zipfile
from collections import Counter, defaultdict

from fastkml import kml

kmz = zipfile.ZipFile("./nanaimo_transportation.kmz")
kml_content = kmz.open("doc.kml", "r").read()

k = kml.KML()
k.from_string(kml_content)

geometries = list()
placemarks = defaultdict(list)

####: Printout of # of placemarks in each document and folder

print("Printout of # of placemarks in each document and folder\n", "-"*60)
for document in k.features():
  print(document.name)
  for folder in document.features():
    print("\t", folder.name)
    for placemark in folder.features():
      placemarks[document.name + "/" + folder.name].append(placemark)

####

print()

####: Inspect the placemarks in each folder in Transportation document

print("Inspect the placemarks in each folder in Transportation document\n", "-"*60)
for dir, pms in placemarks.items():
  geometries = [pm.geometry for pm in pms if pm.geometry]
  geom_types = [geometry.geom_type for geometry in geometries]
  print(dir, len(pms), Counter(geom_types))

####