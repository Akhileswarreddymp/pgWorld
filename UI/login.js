document.getElementById("loginForm").addEventListener("submit", function (e) {
    e.preventDefault(); // Prevent the form from submitting normally.

    // Get the entered username and password.
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;

    // Create an object to hold the data to be sent to the API.
    var data = {
        username: username,
        password: password
    };

    // Clear any previous error messages.
    document.getElementById("error-message").textContent = '';

    // Make an API request using the fetch() function.
    fetch('http://127.0.0.1:8001/api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(function(response) {
        console.log("Response status code:", response.status);
        
        if (response.status === 200) {
            console.log("Authentication successful. Redirecting in 2 seconds...");
            setTimeout(function () {
                window.location.href = "onboard.html";
            }, 2000); 
        } else {
            // Handle authentication failure and display error message.
            throw new Error('Authentication failed');
        }
    })
    .catch(function(error) {
        // Display the error message for authentication failure.
        document.getElementById("error-message").textContent = "Wrong Credentials";
    });
});


