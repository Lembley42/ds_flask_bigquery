# Create a new Flask app instance
from flask import Flask, jsonify, request, Blueprint
from flask_cors import CORS
from google.cloud import bigquery
import os, json


app = Flask(__name__)

cors = CORS()
cors.init_app(app)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = json.loads(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', ''))
BQ_Client = bigquery.Client()

API_KEY = os.environ.get('API_KEY', 'oopcqmbblx2y62i7')


# Register Flask blueprint
bp = Blueprint('api', __name__, url_prefix='/<api_key>/<dataset_id>/<table_id>')
app.register_blueprint(bp)


@app.route('/<api_key>/<dataset_id>/<table_id>', methods=['POST'])
def api(api_key, dataset_id, table_id):
    if request.method == 'POST' and api_key == API_KEY:
        # Get the data from the POST request
        data = request.get_json()
        
        # Upload datat to BigQuery
        dataset_ref = BQ_Client.dataset(dataset_id)
        table_ref = dataset_ref.table(table_id)
        table = BQ_Client.get_table(table_ref)
        rows_to_insert = [data]

        errors = BQ_Client.insert_rows(table, rows_to_insert)
        assert errors == []
        
        return jsonify(data), 200


if __name__ == '__main__':
    app.run()