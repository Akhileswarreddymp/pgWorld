document.getElementById("register_user").addEventListener("submit", function (e) {
    e.preventDefault(); // Prevent the form from submitting normally.

    // Get the entered username and password.
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    var re_password = document.getElementById("re_password").value;
    var name = document.getElementById("name").value;
    var contact_number = document.getElementById("number").value;
    var role = document.getElementById("role").value;
    const now = new Date();
    const isoString = now.toISOString();

console.log(isoString);

    // Create an object to hold the data to be sent to the API.
    var data = {
        username: username,
        password: password,
        re_password : re_password,
        name : name,
        contact_number : contact_number,
        role : role,
        created_time : null,
        updated_time : null,
        profile_pic : ""
    };

    console.log("data===>",data)
    // Clear any previous error messages.
    document.getElementById("error-message").textContent = '';

    // Make an API request using the fetch() function.
    fetch('http://127.0.0.1:8001/user_register', {
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
            window.location.href = "otp_page.html";
        } else {
            // Handle authentication failure and display error message.
            throw new Error('Registeration failed');
        }
    })
    .catch(function(error) {
        // Display the error message for authentication failure.
        document.getElementById("error-message").textContent = "Wrong Credentials";
    });
});