document.getElementById("vacant_form").addEventListener("submit", function (e) {
    e.preventDefault(); // Prevent the form from submitting normally.

    // Get the entered username and password.
    var pg_name = document.getElementById("pg_name").value;
    var pg_code = document.getElementById("pg_code").value;
    var room_number = document.getElementById("room_number").value;
    var sharing = document.getElementById("sharing").value;
    var occupied = document.getElementById("occupied").value;
    var availability = document.getElementById("availablity").value;


    // Create an object to hold the data to be sent to the API.
    var data = {
        pg_name : pg_name,
        pg_code : pg_code,
        room_number : room_number,
        no_of_sharing : sharing,
        no_of_occupied_beds : occupied,
        no_of_vacant_beds : sharing - occupied,
        description : [""],
        status : {
            available : availability
        }
    };

    console.log("data===>",data)
    // Clear any previous error messages.
    document.getElementById("error-message").textContent = '';

    // Make an API request using the fetch() function.
    fetch('http://127.0.0.1:8001/api/roomonboard/vacant_rooms', {
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