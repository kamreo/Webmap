import folium

map = folium.Map( location=[48.853, 2.35], zoom_start=6,tiles='cartodbdark_matter')

fg = folium.FeatureGroup(name="My Map")
fg.add_child(folium.Marker(location=[38.2, -99.1], popup="Hi I am a marker",icon=folium.Icon(color='white')))
map.add_child(fg)


map.save("Map1.html")
