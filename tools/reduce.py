import os
import glob
import math
import xml.etree.ElementTree as ET
import sys

def read_gpx_file(file_path):
    # Lit un fichier GPX et extrait les coordonnées
    tree = ET.parse(file_path)
    root = tree.getroot()
    ns = {'gpx': 'http://www.topografix.com/GPX/1/1'}
    coords = []
    for trk in root.findall('.//gpx:trk', ns):
        for trkseg in trk.findall('.//gpx:trkseg', ns):
            for trkpt in trkseg.findall('.//gpx:trkpt', ns):
                lat = float(trkpt.attrib['lat'])
                lon = float(trkpt.attrib['lon'])
                time = trkpt.find('.//gpx:time', ns).text
                coords.append((lon, lat, time))  # Note: longitude avant latitude pour Ramer-Douglas-Peucker
    return coords

def distance_to_line(p, start, end):
    # Calcule la distance entre un point p et la ligne définie par les points start et end
    x0, y0, _ = p  # Ignorer le temps dans le calcul de la distance
    x1, y1, _ = start
    x2, y2, _ = end
    return abs((y2-y1)*x0 - (x2-x1)*y0 + x2*y1 - y2*x1) / math.sqrt((y2-y1)**2 + (x2-x1)**2)

def simplify_coords(coords, epsilon):
    # Applique l'algorithme de Ramer-Douglas-Peucker pour simplifier les coordonnées
    if len(coords) <= 2:
        return coords
    dmax = 0.0
    index = 0
    end = len(coords) - 1
    for i in range(1, end):
        d = distance_to_line(coords[i], coords[0], coords[end])
        if d > dmax:
            index = i
            dmax = d
    if dmax > epsilon:
        rec_results1 = simplify_coords(coords[:index+1], epsilon)
        rec_results2 = simplify_coords(coords[index:], epsilon)
        results = rec_results1[:-1] + rec_results2
    else:
        results = [coords[0], coords[end]]
    return results

def write_gpx_file(coords, file_path):
    # Crée une nouvelle structure GPX avec les coordonnées simplifiées
    gpx = ET.Element('gpx', version='1.1', xmlns='http://www.topografix.com/GPX/1/1')
    trk = ET.SubElement(gpx, 'trk')
    trkseg = ET.SubElement(trk, 'trkseg')
    for lon, lat, time in coords:
        trkpt = ET.SubElement(trkseg, 'trkpt', lat=str(lat), lon=str(lon))
        time_elem = ET.SubElement(trkpt, 'time')
        time_elem.text = time

    # Écrit la structure XML dans un fichier
    tree = ET.ElementTree(gpx)
    tree.write(file_path, encoding='utf-8', xml_declaration=True)

def select_gpx_to_simplify():
    directory = "."

    # Liste des fichiers GPX
    gpx_files = glob.glob(os.path.join(directory, "*.gpx"))
    gpx_files.sort()

    gpx_file_names = [os.path.basename(file) for file in gpx_files]

    for i, file in enumerate(gpx_file_names, start=1):
        print(f"{i}. {file}")

    selection = input("Sélectionnez un gpx à simplifier (ou 'q' pour quitter) : ")
    if selection.isdigit() and 1 <= int(selection) <= len(gpx_file_names):
        selected_file = gpx_file_names[int(selection) - 1]
        return selected_file
    else:
        return None

gpx_file = select_gpx_to_simplify()
print(f"Vous avez sélectionné le fichier : {gpx_file}")
if gpx_file is None:
    sys.exit(1)

coords = read_gpx_file(gpx_file)
epsilon = 0.0001  # Valeur d'epsilon à ajuster selon la précision souhaitée
simplified_coords = simplify_coords(coords, epsilon)
gpx_file_reduce = gpx_file.replace(".gpx","_{:.10f}".format(epsilon).rstrip('0').rstrip('.').replace(".","_") + ".gpx")
write_gpx_file(simplified_coords, gpx_file_reduce)
print(f"Fichier GPX simplifiées : {gpx_file_reduce}")
