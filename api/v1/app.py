#!/usr/bin/python3
"""the root of the project """
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from os import getenv
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
cors = CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_storage(exception):
    """
    Close the database connection after each request
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """handel not found"""
    return make_response(jsonify({'error': "Not found"}), 404)


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(getenv("HBNB_API_PORT", "5000"))
    app.run(host=host, port=port, threaded=True)
