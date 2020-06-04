import folium
import pandas
import base64

data = pandas.read_csv("doctors.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
map = folium.Map([43.6532, -79.3832], zoom_start=10, tiles="Stamen Terrain")
encoded = base64.b64encode(open('sign1.jpg', 'rb').read()).decode()

html = '<img src="data:image/jpeg;base64,{}">'.format

iframe = folium.IFrame(html(encoded), width=632+20, height=420+20)

popup = folium.Popup(iframe, max_width=2650)
fgv = folium.FeatureGroup(name="Clinics")
for lt, ln in zip(lat, lon):
    fgv.add_child(folium.CircleMarker(location=[lt, ln], radius=6, popup=popup,
                                      color='red', fill=True, fill_opacity=0.7))

map.add_child(fgv)
map.save("Map.html")
