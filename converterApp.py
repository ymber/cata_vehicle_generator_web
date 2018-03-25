from flask import Flask, render_template, url_for, request
import json

app = Flask(__name__)

def findVehicle(saveData, vehicleName):
    for i in range(0, len(saveData)):
        for vehicle in saveData[i]["vehicles"]:
            if (vehicleName == vehicle["name"]):
                return vehicle, vehicleName

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

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/out", methods=["POST"])
def rawOut():
    return render_template("out.html",
                            output=writeDef(*findVehicle(json.loads(request.form["mapdata"]), request.form["vehicleName"])),
                            error="JSON validated")
