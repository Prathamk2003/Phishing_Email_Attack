# Phishing_Email_Attack

This project implements a secure login system using Flask for the backend, MongoDB for data storage, and includes features for data encryption and email notifications.

## 🚀 Features

* **User Authentication**: Simple login form for capturing username and password.
* **Data Storage**: Stores login credentials in MongoDB.
* **Data Encryption**: Utilizes AES encryption to secure sensitive user data (username, password) before storing it in the database.
* **Decryption and Retrieval**: Provides an endpoint to retrieve and decrypt stored login information.
* **CORS Enabled**: Configured to handle cross-origin requests.
* **Email Notifications**: Includes a Python script for sending email notifications (e.g., for alerts or confirmations).

## 🛠️ Technologies Used

* **Backend**:
    * **Flask**: Python web framework.
    * **PyMongo**: MongoDB driver for Python.
    * **Flask-CORS**: Extension for handling Cross-Origin Resource Sharing.
    * **Cryptography**: For robust encryption functionalities (AES).
* **Frontend**:
    * **HTML**: Structure of the login page.
    * **JavaScript (login.js)**: Handles form submission and communicates with the Flask backend.
    * **Tailwind CSS**: For styling the login form (included via CDN).
* **Database**:
    * **MongoDB**: NoSQL database for storing user data.
* **Email**:
    * **Yagmail**: Python library for sending emails easily.
    * **python-dotenv**: For managing environment variables.
    * **getpass**: For securely handling password input.

## 📂 Project Structure
```
.
├── app.py                  # Flask backend for basic login (without encryption)
├── app1.py                 # Flask backend with AES encryption and decryption
├── login.js                # Frontend JavaScript for handling login form submission
├── index.html              # Frontend HTML for the login page
├── secure_email.py         # Python script for sending secure emails
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables for email configuration
├── email_logs.log          # Log file for email sending activities
└── package.json            # Node.js dependencies (for frontend, if any, though not strictly used in this setup)
└── package-lock.json       # Node.js dependency lock file
```

## ⚙️ Setup and Installation

### Prerequisites

Before you begin, ensure you have the following installed:

* **Python 3.x**
* **pip** (Python package installer)
* **MongoDB Community Edition**: [Installation Guide](https://docs.mongodb.com/manual/installation/)
* **npm** (Node Package Manager - generally used for `package.json` but not strictly required for this project's functionality as presented)

### Backend Setup (`app1.py` and `app.py`)

1.  **Clone the repository (or download the files):**

    ```bash
    git clone <your-repository-url>
    cd <your-repository-name>
    ```

2.  **Install Python dependencies:**

    It's recommended to use `app1.py` for the secure version. The `requirements.txt` file contains all necessary dependencies for both `app.py` and `app1.py`, including `cryptography` for encryption.

    ```bash
    pip install -r requirements.txt
    ```
    [cite_start]This will install Flask, PyMongo, Flask-CORS, Cryptography, and other necessary libraries[cite: 3].

3.  **Start MongoDB:**
    Ensure your MongoDB server is running. By default, it runs on `mongodb://localhost:27017/`.

4.  **Run the Flask application:**

    For the **secure version** with encryption (recommended):

    ```bash
    python app1.py
    ```

    For the **basic version** (without encryption, for demonstration purposes only):

    ```bash
    python app.py
    ```

    The Flask application will run on `http://0.0.0.0:5000` (or `http://127.0.0.1:5000`).

### Frontend Setup (`index.html` and `login.js`)

1.  **Open `index.html`:**
    Simply open the `index.html` file in your web browser. This file contains the login form and links to `login.js` for handling the submission.

2.  **Verify `login.js` endpoint:**
    In `login.js`, ensure the `fetch` URL `http://127.0.0.1:5000/login` matches the address where your Flask server is running.

### Email Sender Setup (`secure_email.py`)

1.  **Create a `.env` file:**
    If it doesn't exist, create a file named `.env` in the root directory of your project. [cite_start]This file is used to store environment variables[cite: 1].

2.  **Add environment variables to `.env`:**
    You'll need to configure your Gmail SMTP details. **Crucially, for Gmail, you need to use an App Password, not your regular Gmail password.**

    ```dotenv
    SMTP_SERVER=smtp.gmail.com
    SMTP_PORT=587
    SENDER_EMAIL=your_email@gmail.com
    SENDER_PASSWORD=your_app_password_16_chars
    ```
    Replace `your_email@gmail.com` with your Gmail address and `your_app_password_16_chars` with the 16-character App Password generated from your Google Account security settings.

3.  **Run the email script:**

    ```bash
    python secure_email.py
    ```
    This script will prompt you for sender email, app password, recipient, subject, and message. [cite_start]It also logs email sending attempts to `email_logs.log`[cite: 2].

## 🚀 How to Use

### Login System

1.  Start the Flask backend (`app1.py` recommended).
2.  Open `index.html` in your web browser.
3.  Enter a username and password in the login form.
4.  Click "Login". The `login.js` script will send this data to the Flask backend.
5.  The Flask backend (`app1.py`) will encrypt the username and password using a randomly generated AES session key, store both the encrypted and original (decrypted) values, along with the session key, in the `collection_Test_Decrypted` collection in the `testing1` MongoDB database.
6.  You will receive an alert indicating success or an error.

### Retrieving and Decrypting Data

The `app1.py` Flask application includes an endpoint `/retrieve_and_store_decrypted` that allows you to retrieve a document by its MongoDB `_id`, decrypt the username and password using the stored session key, and update the document with the decrypted values.

To use this:

1.  Make a **POST** request to `http://127.0.0.1:5000/retrieve_and_store_decrypted`.
2.  The request body should be JSON and contain the `_id` of the document you want to decrypt, e.g.:
    ```json
    {
        "id": "65f2a9b3d4e5f6g7h8i9j0k1"
    }
    ```
    (Replace with an actual `_id` from your MongoDB collection).
3.  The response will contain the decrypted username and password.

### Sending Emails

1.  Run `python secure_email.py`.
2.  Follow the prompts to enter your Gmail address, App Password, recipient email, subject, and message.
3.  Confirm to send the email.
4.  [cite_start]Check `email_logs.log` for a record of the email sending attempt[cite: 2].

## ⚠️ Security Considerations

* **Session Key Storage**: In `app1.py`, the AES `session_key` is currently stored alongside the encrypted data and the decrypted data in MongoDB. **This is for demonstration purposes only and is NOT secure for a production environment.** In a real-world scenario, the session key should be handled securely, perhaps via a key management system, or a more robust asymmetric encryption scheme (like RSA) would be used for key exchange.
* **App Passwords for Gmail**: Using App Passwords for programmatic access to Gmail is more secure than using your main password, but ensure you manage these App Passwords carefully.
* [cite_start]**Error Logging**: The `email_logs.log` file captures success and error messages for email sending[cite: 2]. Regularly review these logs for any issues.
* **CORS**: While CORS is enabled for convenience (`CORS(app)`), in a production environment, it's crucial to restrict CORS to only trusted origins to prevent security vulnerabilities.

## 📄 License

This project is licensed under the MIT License - see the `LICENSE` file (if you create one) for details.
