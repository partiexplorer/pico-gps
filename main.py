"""
# Pico-GPS - a GPX Tracks Recorder for Rapsberry Pi Pico
# Copyright (c) 2024 Stéphane Bouchard (partiexplorer@gmail.com)
# The MIT License (MIT) - see LICENSE file
"""
from machine import Pin, UART, I2C
#ref.: https://www.youtube.com/watch?v=y2EDhzDiPTE
#ref.: https://github.com/ahmadlogs/rpi-pico-upy/tree/main/gps2-rpi-pico

import utime, time

from math import radians, degrees, sin, cos, sqrt, atan2

#________________________________________________________
from ssd1306 import SSD1306_I2C
#https://github.com/stlehmann/micropython-ssd1306
#________________________________________________________
from micropyGPS import MicropyGPS
#https://github.com/inmcm/micropyGPS
#________________________________________________________

##########################################################
#Oled I2C connection
i2c=I2C(0, sda=Pin(8), scl=Pin(9), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)
##########################################################

##########################################################
#GPS Module UART Connection
gps_module = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
##########################################################

##########################################################
# variables
TIMEZONE = -5
my_gps = MicropyGPS(TIMEZONE, 'ddm')
#my_gps.start_logging('gps.txt')

track_filename = ""
prevLatitude = float(0)
prevLongitude = float(0)
##########################################################


def haversine(lat1, lon1, lat2, lon2):
    """
    Calcule la distance en mètres entre deux points GPS
    """
    R = 6371000  # Rayon de la Terre en mètres
    phi1 = radians(lat1)
    phi2 = radians(lat2)
    delta_phi = radians(lat2 - lat1)
    delta_lambda = radians(lon2 - lon1)
    
    a = sin(delta_phi / 2)**2 + cos(phi1) * cos(phi2) * sin(delta_lambda / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    distance = R * c
    return distance

def ddm_to_dd(coord_ddm_hemi):
    """
    Convertit une coordonnée GPS du format degrés, minutes décimales (DDM) au format décimal (DD)
    """
    coord_dd = coord_ddm_hemi[0] + coord_ddm_hemi[1] / 60.0
    if coord_ddm_hemi[2] == 'S' or coord_ddm_hemi[2] == 'W':
        coord_dd = -coord_dd
    return coord_dd        

def ddm_to_dms(coord_ddm_hemi):
    """
    Convertit une coordonnée GPS du format degrés, minutes décimales (DDM) au format degrés, minutes, secondes (DMS)
    """
    minutes = int(coord_ddm_hemi[1])
    sec_float = (coord_ddm_hemi[1] - minutes) * 60
    return (coord_ddm_hemi[0], int(coord_ddm_hemi[1]), sec_float, coord_ddm_hemi[2])

##########################################################
while True:
    #_________________________________________________
    #print(i2c.scan())
    length = gps_module.any()
    if length>0:
        b = gps_module.read(length)
        for x in b:
            msg = my_gps.update(chr(x))

    #_________________________________________________
    if not my_gps.fix_stat:
        print("Wait for fix " + str(my_gps.satellites_visible()))
        oled.fill(0)
        oled.text("Wait for fix", 0, 0)
        oled.text(str(my_gps.satellites_visible()), 0, 12)
        oled.show()
        utime.sleep(0.25)
        oled.text("Wait for fix.", 0, 0)
        oled.show()
        utime.sleep(0.25)
        oled.text("Wait for fix..", 0, 0)
        oled.show()
        utime.sleep(0.25)
        oled.text("Wait for fix...", 0, 0)
        oled.show()
        utime.sleep(0.25)
        continue

    #_________________________________________________
    t = my_gps.timestamp
    #t[0] => hours : t[1] => minutes : t[2] => seconds
    gpsTime = '{:02d}:{:02d}:{:02}'.format(t[0], t[1], t[2])
    gpsDate = my_gps.date_string('l_ymd')
    gpx_datetime_local = my_gps.gpx_datetime('local')
    gpx_datetime_utc = my_gps.gpx_datetime('utc')
    speed = my_gps.speed_string('kph')

    if track_filename == "":
        track_filename = gpx_datetime_local
        track_filename = track_filename.replace("-", "") # Remplacer les "-" par "-"
        track_filename = track_filename.replace("T", "_") # Remplacer le "T" par "_"
        track_filename = track_filename.replace(":", "") # Remplacer les ":" par ""
        track_filename = track_filename[:-1] # Enlever le dernier "Z"
        track_filename = "track_{}.csv".format(track_filename)
        track_file = open(track_filename, "w")
        track_file.write("lat,lon,time\n")
        track_file.flush() # [TODO] Maybe we don't need to flush if we close right away
        track_file.close()

    latitude = ddm_to_dd(my_gps.latitude)
    longitude = ddm_to_dd(my_gps.longitude)    
#     altitude = my_gps.altitude
    
    d = haversine(prevLatitude, prevLongitude, latitude, longitude)

    #_________________________________________________
    print('Lat:', latitude)
    print('Lon:', longitude)
    print('gpx_datetime_local:', gpx_datetime_local)
#     print('Speed:', speed)
    print('Distance:', str(d))
    #_________________________________________________

    oled.fill(0)
    oled.text(str(latitude), 0, 0)
    oled.text(str(longitude), 0, 12)
#     oled.text('Speed:'+ speed, 0, 24)
    oled.text('Time:'+ gpsTime, 0, 24)
    oled.text(gpsDate, 0, 36)
    oled.text('Dist:'+ '{0:.2f}'.format(d), 0, 48)
    oled.show()

#     utime.sleep(0.1)
    utime.sleep(2)

    if d < 2:
        continue;

    prevLatitude = latitude
    prevLongitude = longitude

    track_file = open(track_filename, "a")
    track_file.write(str(latitude) + "," + str(longitude) + "," + gpx_datetime_utc + "\n")
    track_file.flush()
    track_file.close()

    #_________________________________________________
##########################################################
