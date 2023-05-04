import os

import folium
import requests
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
EPA_api_key = os.environ['EPA_api_key']
CWB_api_key = os.environ['CWB_api_key']

fmap = folium.Map(location=[23.768001, 120.927373], zoom_start=7, world_copy_jump=True)
r_aqi = requests.get(
    f'https://data.epa.gov.tw/api/v2/aqx_p_432?language=zh&offset=23&limit=100&api_key={EPA_api_key}')

r_eq = requests.get(
    f'https://opendata.cwb.gov.tw/api/v1/rest/datastore/E-A0016-001?Authorization={CWB_api_key}&limit=1&format=JSON&timeFrom=2023-05-01T00%3A00%3A00')

list_of_dicts_aqi = r_aqi.json()
list_of_dicts_eq = r_eq.json()

feature_gp_aqi = folium.FeatureGroup(name="aqi")

for item in list_of_dicts_aqi['records']:
    aqi_in_each_site = item['aqi']
    # fmap.add_child(folium.Marker(location=[item['latitude'], item['longitude']],
    #                              popup=f'{aqi_in_each_site}'), )
    color = ''
    if aqi_in_each_site:
        index = int(aqi_in_each_site)
        if index <= 50:
            color = 'green'
        elif 51 < index <= 100:
            color = 'yellow'
        elif 101 < index <= 150:
            color = 'orange'
        elif 151 < index <= 200:
            color = 'red'
        elif 201 < index <= 300:
            color = 'purple'
        elif 301 < index <= 500:
            color = 'brown'
        folium.Circle(location=(item['latitude'], item['longitude']),
                      color=color,  # Circle 顏色
                      radius=2000,
                      popup=f'{aqi_in_each_site}',
                      fill=True,  # 填滿中間區域
                      fill_opacity=0.5  # 設定透明度
                      ).add_to(feature_gp_aqi)

feature_gp_aqi.add_to(fmap)

feature_gp_eq = folium.FeatureGroup(name="earthquake")
for item in list_of_dicts_eq['records']['Earthquake']:
    lat_epi = item['EarthquakeInfo']['Epicenter']['EpicenterLatitude']
    lon_epi = item['EarthquakeInfo']['Epicenter']['EpicenterLongitude']
    folium.Marker(location=(lat_epi, lon_epi),
                  icon=folium.Icon(color='yellow', icon='glyphicon-star')).add_to(feature_gp_eq)
    intensity = item['Intensity']['ShakingArea']
    for info in intensity:
        for eq_station_info in info['EqStation']:
            station_lat = eq_station_info['StationLatitude']
            station_lon = eq_station_info['StationLongitude']
            seismic_intensity = eq_station_info['SeismicIntensity']
            icon = folium.DivIcon(html=f"{seismic_intensity}")
            folium.Marker(location=(station_lat, station_lon), icon=icon).add_to(feature_gp_eq)

feature_gp_eq.add_to(fmap)
folium.LayerControl().add_to(fmap)
fmap.save('test.html')
