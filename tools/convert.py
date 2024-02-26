import os
import glob
from gpx_converter import Converter
import sys

def convert_csv_to_gpx(csv_file):
    gpx_file = csv_file.replace(".csv",".gpx")
    Converter(input_file=csv_file).csv_to_gpx(lats_colname='lat', longs_colname='lon', times_colname='time', alts_colname='ele', output_file=gpx_file)
    return gpx_file

def select_csv_to_convert():
    directory = "."

    # Liste des fichiers CSV
    csv_files = glob.glob(os.path.join(directory, "*.csv"))

    # Liste des fichiers GPX
    gpx_files = glob.glob(os.path.join(directory, "*.gpx"))

    # Extraire les noms de fichiers sans extension pour les fichiers CSV et GPX
    csv_file_names = [os.path.splitext(os.path.basename(file))[0] for file in csv_files]
    gpx_file_names = [os.path.splitext(os.path.basename(file))[0] for file in gpx_files]

    # Trouver les fichiers CSV qui n'ont pas de fichier GPX avec le même nom
    missing_gpx_files = [file for file in csv_file_names if file not in gpx_file_names]
    missing_gpx_files.sort()

    print("Fichiers CSV sans fichier GPX correspondant:")
    for i, file in enumerate(missing_gpx_files, start=1):
        print(f"{i}. {file}" + ".csv")

    selection = input("Sélectionnez un fichier pour traiter (ou 'q' pour quitter) : ")
    if selection.isdigit() and 1 <= int(selection) <= len(missing_gpx_files):
        selected_file = missing_gpx_files[int(selection) - 1]
        return selected_file + ".csv"
    else:
        return None

csv_file = select_csv_to_convert()
print(f"Vous avez sélectionné le fichier : {csv_file}")
if csv_file is None:
    sys.exit(1)

gpx_file = convert_csv_to_gpx(csv_file)
print(f"Fichier GPX créé à partir du CSV : {gpx_file}")
