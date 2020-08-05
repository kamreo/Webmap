import folium
import pandas as pd
import random
import numpy as np
from branca.element import Template, MacroElement

data=pd.read_csv("Volcanoes_USA.txt")

def color_maker(elevation):
    if elevation <1000:
        return 'green'
    elif 1000<=elevation<3000:
        return 'orange'
    else:
        return 'red'

map = folium.Map( location=[48.853, 2.35], zoom_start=6, tiles='cartodbdark_matter')

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
                             style_function=lambda x: {'fillColor':'blue' if x['properties']['POP2005']<9000000
                                                      else 'green' if 9000000 <= x['properties']['POP2005']<20000000
                                                      else 'yellow' if 20000000<= x['properties']['POP2005']<100000000
                                                      else 'red'}))



template = """
{% macro html(this, kwargs) %}

<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Map</title>
  <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

  <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
  <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>

  <script>
  $( function() {
    $( "#maplegend" ).draggable({
                    start: function (event, ui) {
                        $(this).css({
                            right: "auto",
                            top: "auto",
                            bottom: "auto"
                        });
                    }
                });
});

  </script>
</head>
<body>


<div id='maplegend' class='maplegend'
    style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
     border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 20px;'>

<div class='legend-title'>Population size</div>
<div class='legend-scale'>
  <ul class='legend-labels'>
    <li><span style='background:red;opacity:0.7;'></span>Big (more than 100 million people)</li>
    <li><span style='background:orange;opacity:0.7;'></span>Medium (between 20 and 100 million people)</li>
    <li><span style='background:green;opacity:0.7;'></span>Small (between 10 and 20 million people)</li>
    <li><span style='background:blue;opacity:0.7;'></span>Very Small (less than 10 million people)</li>

  </ul>
</div>
</div>

</body>
</html>

<style type='text/css'>
  .maplegend .legend-title {
    text-align: left;
    margin-bottom: 5px;
    font-weight: bold;
    font-size: 90%;
    }
  .maplegend .legend-scale ul {
    margin: 0;
    margin-bottom: 5px;
    padding: 0;
    float: left;
    list-style: none;
    }
  .maplegend .legend-scale ul li {
    font-size: 80%;
    list-style: none;
    margin-left: 0;
    line-height: 18px;
    margin-bottom: 2px;
    }
  .maplegend ul.legend-labels li span {
    display: block;
    float: left;
    height: 16px;
    width: 30px;
    margin-right: 5px;
    margin-left: 0;
    border: 1px solid #999;
    }
  .maplegend .legend-source {
    font-size: 80%;
    color: #777;
    clear: both;
    }
  .maplegend a {
    color: #777;
    }
</style>
{% endmacro %}"""

macro = MacroElement()
macro._template = Template(template)

map.get_root().add_child(macro)
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
