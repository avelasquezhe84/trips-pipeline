from flask import Flask, jsonify, request, Response
from markupsafe import escape

import json
import load_data

app = Flask(__name__)

@app.route("/api/health")
def health():
	status_code = Response(status=200)
	return status_code

@app.post("/api/load")
def load():
    content_type = request.mimetype
    if content_type == "application/json":
        body = json.loads(request.data.decode("utf8"))
        source = body["source"]
        url = body["url"]
        try:
            load_data.main(source, url)
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": "CSV file loading failed...",
                "error":  e
            })
        return jsonify({
            "status": "success",
            "message": "CSV file loaded into the database successfully.",
            "error": ""
        })
    return jsonify({
        "status": "error",
        "message": "Request Body is {}.".format(content_type),
        "error": "Request Body is not JSON."
    })

@app.post("/api/trips")
def weekly_average_trips_by_bounding_box():
    content_type = request.mimetype
    if content_type == "application/json":
        body = json.loads(request.data.decode("utf8"))
        min_lat = float(body["min_lat"])
        min_lon = float(body["min_lon"])
        max_lat = float(body["max_lat"])
        max_lon = float(body["max_lon"])
        try:
            result = load_data.get_weekly_average_by_bounding_box(min_lat, min_lon, max_lat, max_lon)
            return jsonify({
                "status": "success",
                "result": result,
                "error":  ""
            })
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": "Process failed...",
                "error":  e
            })
    return jsonify({
        "status": "error",
        "message": "Request Body is {}.".format(content_type),
        "error": "Request Body is not JSON."
    })

@app.get("/api/trips/<region>")
def weekly_average_trips_by_region(region: str):
    region = escape(region)
    try:
        result = load_data.get_weekly_average_by_region(region)
        return jsonify({
            "status": "success",
            "result": result,
            "error":  ""
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Process failed...",
            "error":  e
        })

if __name__ == "__main__":
    app.run()
