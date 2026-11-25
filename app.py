import io

from flask import Flask, jsonify, render_template, request, send_file

from terre import fichier_kml, lambert1_vers_wgs84

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generer-kml", methods=["POST"])
def generer_kml():
    donnees = request.get_json(silent=True) or {}
    points_bruts = donnees.get("points", [])

    try:
        points = [
            (str(p["nom"]).strip(), float(p["x"]), float(p["y"]))
            for p in points_bruts
        ]
    except (KeyError, TypeError, ValueError):
        return jsonify({"erreur": "Points invalides."}), 400

    if not points:
        return jsonify({"erreur": "Aucun point à convertir."}), 400

    points_convertis = lambert1_vers_wgs84(points)

    tampon = io.BytesIO()
    fichier_kml(points_convertis, tampon)
    tampon.seek(0)

    return send_file(
        tampon,
        mimetype="application/vnd.google-earth.kml+xml",
        as_attachment=True,
        download_name="points.kml",
    )


if __name__ == "__main__":
    app.run(debug=True)
