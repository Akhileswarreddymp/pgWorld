document.getElementById("otp_sent").addEventListener("submit", function (e) {
    e.preventDefault(); // Prevent the form from submitting normally.

    // Get the entered username and password.
    var otp = document.getElementById("otp").value;

    // Create an object to hold the data to be sent to the API.
    var data = {
        otp: otp,
    };

    // Clear any previous error messages.
    document.getElementById("error-message").textContent = '';

    // Make an API request using the fetch() function.
    fetch('http://127.0.0.1:8001/verify_user_otp', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(function(response) {
        console.log("Response status code:", response.status);
        if (response.status === 200) {
            // Redirect to the "sign_reg.html" page on successful login.
            // window.location.href = "../backend/payment.html";
            window.location.href = "login.html";
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