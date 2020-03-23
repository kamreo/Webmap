import folium
import pandas as pd
import random
import numpy as np

data=pd.read_csv("Volcanoes_USA.txt")

def color_maker(elevation):
    if elevation <1000:
        return 'green'
    elif 1000<=elevation<3000:
        return 'orange'
    else:
        return 'red'

map = folium.Map( location=[48.853, 2.35], zoom_start=6,tiles='cartodbdark_matter')

fg = folium.FeatureGroup(name="My Map")

latitude=list(data["LAT"])
longitude=list(data["LON"])
elevation= list(data["ELEV"])

fgv = folium.FeatureGroup(name="Volcanoes in USA")

for lt,ln,el in zip(latitude,longitude,elevation):
    popup_message="Height: "+str(el)+"m"
    fgv.add_child(folium.CircleMarker(location=[lt,ln], radius =6, fill_color=color_maker(el),
                                popup=popup_message, color = 'black',fill_opacity=0.7, fill=True))


fgp=folium.FeatureGroup(name="Population")

fgp.add_child(folium.GeoJson(data=open('world.json','r',encoding='utf-8-sig').read(),
                             style_function=lambda x: {'fillColor':'blue' if x['properties']['POP2005']<10000000
                                                      else 'green' if 10000000 <= x['properties']['POP2005']<20000000
                                                      else 'yellow' if 20000000<= x['properties']['POP2005']<100000000
                                                      else 'red'}))


map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())



#code for generating random coordinates
# w, h = 2, 10;
# generated_coordinates = [[0 for x in range(w)] for y in range(h)]
#
# # generating random coordinates
# for x in range (0,h):
#     latitude=random.uniform(-90,90)
#     longitude=random.uniform(-180,180)
#     generated_coordinates[x][0]=latitude
#     generated_coordinates[x][1]=longitude
#
# generated_coordinates=np.array(generated_coordinates)
# dimensions=generated_coordinates.shape
# rows=dimensions[0]
# columns=dimensions[1]

# creating markers using our coordinates array

# for x in range(0,rows):
#
#     popup_message="Latitude:{} Longitude:{}".format(generated_coordinates[x][0],generated_coordinates[x][1])
#     fg.add_child(folium.Marker(location=generated_coordinates[x],
#                                popup=popup_message,icon=folium.Icon(color='white')))
#
#     map.add_child(fg)


map.save("Map1.html")
