# Create a new Flask app instance
from flask import Flask, jsonify, request, Blueprint
from flask_cors import CORS
from google.cloud import bigquery
import os, json
from cryptography.fernet import Fernet

app = Flask(__name__)

CORS(app)

# Decrypt service-account-info.bin and save as service-account-info.json
DECRYPT_KEY = os.environ.get('DECRYPT_KEY', '').encode()
fernet = Fernet(DECRYPT_KEY)
with open('service-account-info.bin', 'rb') as f:
    encrypted_data = f.read()
decrypted_data = fernet.decrypt(encrypted_data)
with open('service-account-info.json', 'wb') as f:
    f.write(decrypted_data)

# Authenticate to BigQuery
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'service-account-info.json'
BQ_Client = bigquery.Client()

# Get API_KEY from environment variable
API_KEY = os.environ.get('API_KEY', '')


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

def Decrypt_File():
    with open('service-account-info.bin', 'rb') as f:
        encrypted = f.read()
    fernet = Fernet('JJgw-NhExNoQi2LkoQZmUZ3pRW3zgVhei7vX8nFq4Ww='.encode())
    decrypted_data = fernet.decrypt(encrypted)
    with open('service-account-info.json', 'w') as f:
        json.dump(decrypted_data.decode(), f)


if __name__ == '__main__':
    app.run()

