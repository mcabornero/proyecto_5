import xml.etree.ElementTree as ET
import os
import csv
import shutil
import math

from Scripts.pywin32_testall import project_root

# Rutas (ajusta si es necesario)
xml_path = r"/proyecto5-Mario-2025-06-05/labeled-data/video1/annotations.xml"
imagenes_origen = r"C:\Users\Usuario01\PycharmProjects\PythonProject\proyecto5-Mario-2025-06-05\labeled-data\video1"
dlc_video_folder = r"C:\Users\Usuario01\PycharmProjects\PythonProject\proyecto5-Mario-2025-06-05\labeled-data\video1"
os.makedirs(dlc_video_folder, exist_ok=True)

scorer = "Mario"

# Nuevos puntos clave
keypoints = [
    "08_P_Narina",
    "12_P_AletaDorsalSup",
    "13_P_AletaDorsalInf",
    "20_P_Ojo_Izq",
    "20_P_Ojo_Der",
    "11_P_AletaPectoral_Izq",
    "11_P_AletaPectoral_Der",
    "17_P_ColaInf",
]

# Parsing de los puntos
def parse_points(points_str):
    coords = []
    for pair in points_str.strip().split(";"):
        if pair:
            x, y = map(float, pair.strip().split(","))
            coords.append((x, y))
    return coords

def vector_cross_z(p1, p2, p):
    """Calcula el producto vectorial para saber en qué lado está `p` respecto a la línea p1-p2."""
    return (p2[0] - p1[0]) * (p[1] - p1[1]) - (p2[1] - p1[1]) * (p[0] - p1[0])

# Parsear XML
tree = ET.parse(xml_path)
root = tree.getroot()

header = ["scorer"] + [scorer] * len(keypoints) * 2
bodyparts = ["bodyparts"] + [kp for kp in keypoints for _ in ("x", "y")]
coords = ["coords"] + ["x" if i % 2 == 0 else "y" for i in range(len(keypoints) * 2)]
rows = [header, bodyparts, coords]

for image in root.iter("image"):
    filename = image.attrib["name"]
    puntos = {k: [] for k in keypoints}

    # Extraer puntos por tipo
    for point in image.iter("points"):
        label = point.attrib["label"]
        coords = parse_points(point.attrib["points"])
        if label == "20_P_Ojo":
            puntos["ojos"] = coords
        elif label == "11_P_AletaPectoral":
            puntos["aletas"] = coords
        elif label in keypoints:
            puntos[label].extend(coords)

    # Determinar línea base
    base_line = None
    if puntos["08_P_Narina"] and puntos["12_P_AletaDorsalSup"]:
        base_line = (puntos["08_P_Narina"][0], puntos["12_P_AletaDorsalSup"][0])
    elif puntos["08_P_Narina"] and puntos["13_P_AletaDorsalInf"]:
        base_line = (puntos["08_P_Narina"][0], puntos["13_P_AletaDorsalInf"][0])

    # Clasificar ojos y aletas pectorales según el lado
    if base_line:
        p1, p2 = base_line
        if "ojos" in puntos:
            for o in puntos["ojos"]:
                side = vector_cross_z(p1, p2, o)
                if side > 0:
                    puntos["20_P_Ojo_Izq"] = [o]
                else:
                    puntos["20_P_Ojo_Der"] = [o]
        if "aletas" in puntos:
            for a in puntos["aletas"]:
                side = vector_cross_z(p1, p2, a)
                if side > 0:
                    puntos["11_P_AletaPectoral_Izq"] = [a]
                else:
                    puntos["11_P_AletaPectoral_Der"] = [a]

    fila = [os.path.join("../../proyecto3-Mario-2025-05-27/labeled-data", "video1", filename)]
    for k in keypoints:
        coords_k = puntos[k]
        if coords_k:
            x, y = coords_k[0]
            fila.extend([x, y])
        else:
            fila.extend(["", ""])
    rows.append(fila)

# Guardar CSV
csv_path = os.path.join(dlc_video_folder, f"CollectedData_{scorer}.csv")
with open(csv_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(rows)

csv_path
