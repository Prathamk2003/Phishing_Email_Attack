from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS  # Import CORS
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import base64
from bson import ObjectId  # For MongoDB ObjectId handling

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")  # Connect to MongoDB server
db = client['testing1']  # Use the 'testing1' database
collection = db['collection_Test_Decrypted']  

# Helper function to encrypt data using AES
def encrypt_data(session_key, data):
    iv = os.urandom(16)  # Initialization vector for AES
    cipher = Cipher(algorithms.AES(session_key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padded_data = data + (16 - len(data) % 16) * b' '  # Pad data to be a multiple of 16 bytes
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return iv + encrypted_data  # Return IV + encrypted data

# Helper function to decrypt data using AES
def decrypt_data(session_key, encrypted_data):
    iv = encrypted_data[:16]  # Extract the IV
    cipher = Cipher(algorithms.AES(session_key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data[16:]) + decryptor.finalize()
    return decrypted_data.rstrip(b' ')  # Remove padding

# Endpoint to handle login data with secure encryption (symmetric only)
@app.route('/login', methods=['POST'])
def login():
    try:
        # Get the JSON data from the request
        data = request.get_json()

        # Extract username and password
        username = data.get('username')
        password = data.get('password')

        # Generate a random AES session key (256-bit AES)
        session_key = os.urandom(32)

        # Encrypt the data using AES
        encrypted_username = encrypt_data(session_key, username.encode())
        encrypted_password = encrypt_data(session_key, password.encode())

        # Insert the encrypted data into MongoDB (you would store this in the 'ttt' collection)
        login_data = {
            'username': base64.b64encode(encrypted_username).decode(),
            'password': base64.b64encode(encrypted_password).decode(),
            'session_key': base64.b64encode(session_key).decode(),  # Store the session key (not recommended for production)
            'decrypted_username': username,  # Store decrypted username
            'decrypted_password': password   # Store decrypted password
        }

        # Insert the data into the 'ttt' collection
        result = collection.insert_one(login_data)

        # Respond with a success message
        response = {
            'message': 'Login data has been stored securely!',
            'inserted_id': str(result.inserted_id)  # Return the inserted document's ID
        }
        return jsonify(response), 200

    except Exception as e:
        # Catch any exception and return an error message
        print(f"Error: {e}")
        return jsonify({'message': f"Error storing data: {str(e)}"}), 500

# Endpoint to handle retrieving, decrypting, and updating the stored data
@app.route('/retrieve_and_store_decrypted', methods=['POST'])
def retrieve_and_store_decrypted():
    try:
        # Get the input _id to retrieve the data
        data = request.get_json()
        object_id = data.get('id')  # The MongoDB document id

        if not object_id:
            return jsonify({"message": "ObjectId not provided"}), 400

        # Retrieve the document from MongoDB by ObjectId
        document = collection.find_one({"_id": ObjectId(object_id)})

        if not document:
            return jsonify({"message": "No data found"}), 404

        # Get the encrypted data from MongoDB
        encrypted_username = base64.b64decode(document['username'])
        encrypted_password = base64.b64decode(document['password'])
        session_key = base64.b64decode(document['session_key'])

        # Decrypt the data using AES
        decrypted_username = decrypt_data(session_key, encrypted_username).decode()
        decrypted_password = decrypt_data(session_key, encrypted_password).decode()

        # Update the document with decrypted values in MongoDB
        collection.update_one(
            {"_id": ObjectId(object_id)},
            {"$set": {"decrypted_username": decrypted_username, "decrypted_password": decrypted_password}}
        )

        # Return the decrypted details
        return jsonify({
            "decrypted_username": decrypted_username,
            "decrypted_password": decrypted_password
        }), 200

    except Exception as e:
        # Catch any exception and return an error message
        print(f"Error: {e}")
        return jsonify({'message': f"Error retrieving data: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
