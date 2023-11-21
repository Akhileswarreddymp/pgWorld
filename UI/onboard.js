document.getElementById("Onboard_form").addEventListener("submit", function (e) {
    e.preventDefault(); // Prevent the form from submitting normally.

    // Get the entered username and password.
    var pg_name = document.getElementById("pg_name").value;
    var pg_code = document.getElementById("pg_code").value;
    var email = document.getElementById("email").value;
    var state = document.getElementById("state").value;
    var city = document.getElementById("city").value;
    var pincode = document.getElementById("pincode").value || 0;
    var area = document.getElementById("area").value;
    var total_no_of_rooms = document.getElementById("total_rooms").value || 0;
    var no_of_floors = document.getElementById("total_floors").value || 0;
    var no_of_5sharing_rooms = document.getElementById("5_sharing").value || 0;
    var no_of_4sharing_rooms = document.getElementById("4_sharing").value || 0;
    var no_of_3sharing_rooms = document.getElementById("3_sharing").value || 0;
    var no_of_2sharing_rooms = document.getElementById("2_sharing").value || 0;
    var no_of_single_sharing_rooms = document.getElementById("single_sharing").value || 0;
    var morethan_5sharing_rooms = document.getElementById("morethan_5").value || 0;
    var cost_of_5sharing = document.getElementById("5_sharing_cost").value || 0;
    var cost_of_4sharing = document.getElementById("4_sharing_cost").value || 0;
    var cost_of_3sharing = document.getElementById("3_sharing_cost").value || 0;
    var cost_of_2sharing = document.getElementById("2_sharing_cost").value || 0;
    var cost_of_single_sharing = document.getElementById("1_sharing_cost").value || 0;
    var cost_for_morethan_5sharing = document.getElementById("morethan_5_sharing_cost").value || 0;
    var without_food = document.getElementById("yes_or_no").value || 0;
    var cost_without_food = document.getElementById("cost_wof_food").value || 0;
    var overall_rating = document.getElementById("rating").value || 0;
    var advance = document.getElementById("advance").value || 0;
    var maintenance_charge = document.getElementById("maintenance_charge").value || 0;
    var negotiable = document.getElementById("nego_yes_or_no").value || 0;
    console.log(without_food)
    console.log(negotiable)

    console.log(cost_without_food)
    // Create an object to hold the data to be sent to the API.
    var data = {
        pg_name: pg_name,
        pg_code: pg_code,
        email:email,
        state:state,
        city:city,
        pincode:pincode,
        area:area,
        total_no_of_rooms:total_no_of_rooms,
        no_of_floors:no_of_floors,
        no_of_5sharing_rooms:no_of_5sharing_rooms,
        no_of_4sharing_rooms:no_of_4sharing_rooms,
        no_of_3sharing_rooms:no_of_3sharing_rooms,
        no_of_2sharing_rooms:no_of_2sharing_rooms,
        no_of_single_sharing_rooms:no_of_single_sharing_rooms,
        morethan_5sharing_rooms:morethan_5sharing_rooms,
        cost_of_5sharing:cost_of_5sharing,
        cost_of_4sharing:cost_of_4sharing,
        cost_of_3sharing:cost_of_3sharing,
        cost_of_2sharing:cost_of_2sharing,
        cost_of_single_sharing:cost_of_single_sharing,
        cost_for_morethan_5sharing:cost_for_morethan_5sharing,
        cost_of_5sharing_wof : cost_of_5sharing-cost_without_food,
        cost_of_4sharing_wof : cost_of_4sharing-cost_without_food,
        cost_of_3sharing_wof : cost_of_3sharing-cost_without_food,
        cost_of_2sharing_wof : cost_of_2sharing-cost_without_food,
        cost_of_single_sharing_wof : cost_of_single_sharing,
        cost_for_morethan_5sharing_wof : cost_for_morethan_5sharing-cost_without_food,
        overall_rating:{
            food_rating:overall_rating,
            cleaning:overall_rating,
            maintenance:overall_rating,
            water_facility:overall_rating,
            freedom:overall_rating,
            worth_for_money:overall_rating,
            over_all_rating:overall_rating
        },
        advance:advance,
        maintenance_charge:maintenance_charge,
        negotiable:negotiable,
        on_boarded_time : null,
        updated_time : null,
        total_vacancy : 0

    };
    console.log(data)
    // Clear any previous error messages.
    document.getElementById("error-message").textContent = '';

    // Make an API request using the fetch() function.
    fetch('http://127.0.0.1:8001/api/pgonboard/pg_onboard', {
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
            window.location.href = "main_UI.html";
        } else {
            // Handle authentication failure and display error message.
            throw new Error('Onboarding failed');
        }
    })
    .catch(function(error) {
        // Display the error message for authentication failure.
        document.getElementById("error-message").textContent = "Onboarding Failed";
    });
});


