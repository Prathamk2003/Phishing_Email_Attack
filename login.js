document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Check if both fields are filled
    if (!username || !password) {
        alert('Please enter both username and password');
        return;
    }

    // Send the login data to the Flask server
    fetch('http://127.0.0.1:5000/login', {  // Change to the correct Flask server address
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })  // Convert form data to JSON
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to store data');  // Handle failed response
        }
        return response.json();  // Parse JSON if response is OK
    })
    .then(data => {
        console.log('Success:', data);  // Log the success message
        alert(data.message || 'Login data has been stored successfully!');
    })
    .catch((error) => {
        console.error('Error:', error);  // Log the error for debugging
        alert('Error storing data: ' + error.message);  // Show alert with error message
    });
});
