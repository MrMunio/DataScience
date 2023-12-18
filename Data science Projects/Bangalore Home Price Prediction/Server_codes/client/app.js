
// Function to erase location dropdown options
function eraseLocationDropdownOptions() {
    var locationOptionsElement = document.getElementById("uiLocations");
    locationOptionsElement.innerHTML = '';
}

// Function to get location list from the server
function getLocationList() {
    var apiUrl = "http://127.0.0.1:5000/get_location_names";

    // Callback function to populate location options
    function populateLocationOptions(data) {
        var locationOptionsElement = document.getElementById("uiLocations");

        if (data) {
            eraseLocationDropdownOptions();

            var locationsList = data.locations;

            for (var i in locationsList) {
                var opt = new Option(locationsList[i]);
                $('#uiLocations').append(opt);
            }
        }
    }

    $.get(apiUrl, populateLocationOptions);
}

// Function to get the selected BHK value
function getBHK() {
    // Use querySelector to find the checked radio button
    var selectedRadio = document.querySelector('input[name="uiBHK"]:checked');

    if (selectedRadio) {
        // If a radio button is checked, return its value
        return selectedRadio.value;
    } else {
        // If no radio button is checked, return -1
        return -1;
    }
}

// Function to print the price result on the page
function printPriceResult(result) {
    var displayLoc = document.getElementById("uiEstimatedPrice");
    displayLoc.innerHTML = "<h2>" + result.toString() + " Lakh Rupees </h2>";
}

// Function to handle the estimate price button click
function onClickedEstimatePrice() {
    var location = document.getElementById("uiLocations").value;
    var bhk = getBHK();
    var areaSqft = document.getElementById("uiSqft").value;

    var parameters = {
        "total_sqft": areaSqft,
        "location": location,
        "bhk": bhk
    };

    var apiUrlForPrediction = "http://127.0.0.1:5000/predict_home_price";

    // Callback function to display the result
    function displayResult(data) {
        console.log(data.estimated_price);
        printPriceResult(data.estimated_price);
    }

    // Make a POST request to predict home price
    $.post(apiUrlForPrediction, parameters, displayResult);
}

// Trigger the getLocationList function on window load
window.onload = getLocationList;
