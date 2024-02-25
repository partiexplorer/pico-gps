from math import radians, degrees, sin, cos, sqrt, atan2

lat1=45.39884
lon1=-73.48219
lat2=45.39885
lon2=-73.48224

R = 6371000  # Rayon de la Terre en mètres
phi1 = radians(lat1)
phi2 = radians(lat2)
delta_phi = radians(lat2 - lat1)
delta_lambda = radians(lon2 - lon1)

a = sin(delta_phi / 2)**2 + cos(phi1) * cos(phi2) * sin(delta_lambda / 2)**2
c = 2 * atan2(sqrt(a), sqrt(1 - a))

distance = R * c

print(distance)
