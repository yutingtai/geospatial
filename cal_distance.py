# calculate how long it takes when I go out to have lunch from the office
# route 1 : the Family Mart that is the nearst one to the office with more seats
# route 2 : there is no available seats in the first Family Mart, so I will go to another
# Family Mart where are full of seats
# route 3 : Go to Mcdonald
# walking speed: 1-1.8 m/s(my walking speed : 1.5 m/s)


from geopy.geocoders import Nominatim
from geopy.distance import geodesic

walking_speed = float(input('Please enter your walking speed(m/s): '))
geolocator = Nominatim(user_agent="qsid1130@gmail.com")
address_office = '民德大樓, 民權西路102巷, 民權里, 大同區, 雙連, 臺北市, 10364, 臺灣'
office = geolocator.geocode(address_office)
office_point = (office.latitude, office.longitude)
print(office_point)
location = geolocator.reverse('25.0625094,121.5175432532111')
# print(location.address)

address_FamilyMart = '全家便利商店, 民權西路144巷, 民權里, 大同區, 雙連, 臺北市, 10361, 臺灣'
FamilyMart = geolocator.geocode(address_FamilyMart)
FamilyMart_point = (FamilyMart.latitude, FamilyMart.longitude)
print(FamilyMart_point)

address_mc = 'Dr.stretch, 民權西路, 集英里, 中山區, 雙連, 臺北市, 10365, 臺灣'
mc = geolocator.geocode(address_mc)
mc_point = (mc.latitude, mc.longitude)

address_FamilyMart2 = '遠傳電信, 民權西路, 集英里, 中山區, 雙連, 臺北市, 10365, 臺灣'
FamilyMart2 = geolocator.geocode(address_FamilyMart2)
FamilyMart2_point = (FamilyMart2.latitude, FamilyMart2.longitude)

# straight distance
route1 = geodesic(office_point, FamilyMart_point)
time1 = route1.meters * 2 / walking_speed / 60
format_time1 = "{:.2f}".format(time1)
print(f'路線1: {format_time1} 分')

route2 = geodesic(FamilyMart_point, FamilyMart2_point)
route2_2 = geodesic(FamilyMart2_point, office_point)
time2 = (route1.meters + route2.meters + route2_2.meters) / walking_speed / 60
format_time2 = "{:.2f}".format(time2)
print(f'路線2: {format_time2} 分')

route3 = geodesic(office_point, mc_point)
time3 = route3.meters * 2 / walking_speed / 60
format_time3 = "{:.2f}".format(time3)
print(f'路線3: {format_time3} 分')
