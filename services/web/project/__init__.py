from project.data import LoadData
from project.celery_config import celery_init_app
from celery import shared_task
from celery.result import AsyncResult
from flask import Flask, jsonify, request, Response
from markupsafe import escape
import logging
import json

app = Flask(__name__)
app.config.from_object("project.config.Config")
load_data = LoadData(app.config['SQLALCHEMY_DATABASE_URI'])
app.config.from_mapping(
    CELERY=dict(
        broker_url="redis://redis",
        result_backend="redis://redis",
        task_ignore_result=True,
    ),
)

celery_app = celery_init_app(app)

@shared_task(ignore_result=False)
def load_data_from_remote_file(source: str, url: str):
    load_data.main(source, url)

@app.get("/api/health")
def health():
	status_code = Response(status=200)
	return status_code

@app.post("/api/start_load")
def start_load():
    content_type = request.mimetype
    if content_type == "application/json":
        body = json.loads(request.data.decode("utf8"))
        source = body["source"]
        url = body["url"]
        try:
            result = load_data_from_remote_file.delay(source, url)
            return jsonify(
                process_id = result.id,
                status = "success",
                message = "CSV file is being loaded into the database successfully.",
                error = ""
            )
        except Exception as e:
            logging.exception(e)
            return jsonify(
                process_id = 0,
                status = "error",
                message = "CSV file loading failed...",
                error = "CSV file loading failed..."
            )
    return jsonify(
        process_id = 0,
        status = "error",
        message = "Request Body is {}.".format(content_type),
        error = "Request Body is not JSON."
    )

@app.get("/api/status/<process_id>")
def get_process_status(process_id):
    result = AsyncResult(process_id)
    if not result:
        return jsonify(
            process_id = process_id,
            ready = "",
            successful = "",
            message = "Process not found",
        )
    return jsonify(
        process_id = process_id,
        ready = result.ready(),
        successful = result.successful(),
        message = "CSV file is being loaded into the database successfully." if result.ready() else "CSV file is still being loaded into the database.",
    )

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
            return jsonify(
                status = "success",
                result = result,
                error =  ""
            )
        except Exception as e:
            logging.exception(e)
            return jsonify(
                status = "error",
                message = "Process failed...",
                error =  "Process failed..."
            )
    return jsonify(
        status = "error",
        message = "Request Body is {}.".format(content_type),
        error = "Request Body is not JSON."
    )

@app.get("/api/trips/<region>")
def weekly_average_trips_by_region(region: str):
    region = escape(region)
    try:
        result = load_data.get_weekly_average_by_region(region)
        return jsonify(
            status = "success",
            result = result,
            error =  ""
        )
    except Exception as e:
        logging.exception(e)
        return jsonify(
            status = "error",
            message = "Process failed...",
            error =  "Process failed..."
        )
