from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")  # Connect to MongoDB server
db = client['testing1']  # Use the 'testing1' database
collection = db['collection_Test']  # Use the 'collection_Test' collection

# Endpoint to handle login data
@app.route('/login', methods=['POST'])
def login():
    try:
        # Get the JSON data from the request
        data = request.get_json()

        # Extract username and password
        username = data.get('username')
        password = data.get('password')

        # Insert the captured data into MongoDB
        login_data = {
            'username': username,
            'password': password
        }

        # Insert the data into the 'collection_Test' collection
        result = collection.insert_one(login_data)

        # Respond with a success message
        response = {
            'message': 'Login data has been stored successfully!',
            'inserted_id': str(result.inserted_id)  # Return the inserted document's ID
        }
        return jsonify(response), 200

    except Exception as e:
        # Catch any exception and return an error message
        print(f"Error: {e}")
        return jsonify({'message': f"Error storing data: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
