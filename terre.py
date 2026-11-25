import xml.etree.ElementTree as ET
from pyproj import Transformer


def lambert1_vers_wgs84(points_lambert1: list[tuple[str, float, float]]) -> list[dict]:
    transformer = Transformer.from_crs("EPSG:26191", "EPSG:4326", always_xy=True)

    resultats = []
    for nom, x, y in points_lambert1:
        lon, lat = transformer.transform(x, y)
        resultats.append({
            "nom": nom,
            "x_lambert1": x,
            "y_lambert1": y,
            "lon": lon,
            "lat": lat,
        })
    return resultats


def fichier_kml(points_wgs84: list[dict], nom_fichier: str = "trace_lambert1.kml") -> None:
    kml = ET.Element("kml", xmlns="http://www.opengis.net/kml/2.2")
    document = ET.SubElement(kml, "Document")

    nom_doc = ET.SubElement(document, "name")
    nom_doc.text = "Tracé Lambert Zone I Maroc (WGS 84)"

    style_ligne = ET.SubElement(document, "Style", id="styleTrace")
    line_style = ET.SubElement(style_ligne, "LineStyle")
    color = ET.SubElement(line_style, "color")
    color.text = "ff0000ff"  
    width = ET.SubElement(line_style, "width")
    width.text = "4"

    for pt in points_wgs84:
        placemark_pt = ET.SubElement(document, "Placemark")
        nom_pt = ET.SubElement(placemark_pt, "name")
        nom_pt.text = pt["nom"]

        desc_pt = ET.SubElement(placemark_pt, "description")
        desc_pt.text = (
            f"Lambert I : X={pt['x_lambert1']:.2f}, Y={pt['y_lambert1']:.2f}\n"
            f"WGS 84 : Lat={pt['lat']:.6f}, Lon={pt['lon']:.6f}"
        )

        point_elem = ET.SubElement(placemark_pt, "Point")
        coords_pt = ET.SubElement(point_elem, "coordinates")
        coords_pt.text = f"{pt['lon']:.8f},{pt['lat']:.8f},0"

    if len(points_wgs84) >= 2:
        placemark_ligne = ET.SubElement(document, "Placemark")
        nom_ligne = ET.SubElement(placemark_ligne, "name")
        nom_ligne.text = "Tracé des points"

        style_url = ET.SubElement(placemark_ligne, "styleUrl")
        style_url.text = "#styleTrace"

        line_string = ET.SubElement(placemark_ligne, "LineString")
        tessellate = ET.SubElement(line_string, "tessellate")
        tessellate.text = "1"  # Suit le relief terrestre

        coords_ligne = ET.SubElement(line_string, "coordinates")
        liste_coords = [f"{pt['lon']:.8f},{pt['lat']:.8f},0" for pt in points_wgs84]
        coords_ligne.text = " ".join(liste_coords)

    arbre = ET.ElementTree(kml)
    ET.indent(arbre, space="  ")
    arbre.write(nom_fichier, encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    points = [
        ("B1", 640503.59, 507739.08),
        ("18", 640535.79, 507731.57),
        ("B2", 640556.85, 507728.87),
        ("19", 640545.64, 507719.63),
        ("20", 640521.90, 507696.57),
        ("B3", 640521.27, 507703.03),
        ("B4", 640490.62, 507663.66),
        ("B5", 640567.28, 507557.68),
        ("B6", 640554.08, 507561.57),
        ("B7", 640528.70, 507576.58),
        ("B8", 640513.57, 507589.41),
        ("B9", 640480.72, 507617.79),
        ("B10", 640451.34, 507646.50),
    ]

    points_convertis = lambert1_vers_wgs84(points)

    for p in points_convertis:
        print(
            f"{p['nom']} -> "
            f"Lat: {p['lat']:.6f}, Lon: {p['lon']:.6f}"
        )

    fichier_kml(points_convertis, "points.kml")
    print("\nFichier 'points.kml' généré avec succès.")