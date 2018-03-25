from flask import Flask, render_template, url_for, request, redirect
import json

app = Flask(__name__)

def findVehicle(saveData, vehicleName):
    for i in range(0, len(saveData)):
        for vehicle in saveData[i]["vehicles"]:
            if (vehicleName == vehicle["name"]):
                return vehicle, vehicleName
    
    return 1

def writeDef(vehicle, vehicleName):
    partsDef = []
    for part in vehicle["parts"]:
        partsDef.append({"x": part["mount_dx"],
                         "y": part["mount_dy"],
                         "part": part["id"]})

    vehicleDef = {"id": vehicleName,
                   "type": "vehicle",
                   "name": vehicleName,
                   "parts": partsDef}

    return json.dumps(vehicleDef)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.args.get("validate", default=0, type=int):
        try:
            if findVehicle(json.loads(request.form["mapdata"]), request.form["vehicleName"]) == 1:
                return render_template("index.html", error="Vehicle identifier not found in map data")
        except ValueError:
            return render_template("index.html", error="Data could not be parsed as JSON")

        return redirect(url_for("presentOut"), code=307)

    return render_template("index.html")

@app.route("/out", methods=["POST"])
def presentOut():
    return render_template("out.html",
                            output=writeDef(*findVehicle(json.loads(request.form["mapdata"]), request.form["vehicleName"])),
                            error="JSON validated")
