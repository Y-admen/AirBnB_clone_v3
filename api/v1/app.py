#!/usr/bin/python3
"""the root of the project """
from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_storage(exception):
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return (jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = "0.0.0.0" if not getenv("HBNB_API_HOST") \
        else getenv("HBNB_API_HOST")
    port = 5000 if not getenv("HBNB_API_PORT") \
        else getenv("HBNB_API_PORT")
    app.run(host=host, port=port, threaded=True)
