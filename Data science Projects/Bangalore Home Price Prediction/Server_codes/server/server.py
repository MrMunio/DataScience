from flask import Flask, request, jsonify
import util


# Create a Flask web application instance
app = Flask(__name__)


# Endpoint to get location names
@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    # Get the list of location names from the util module
    response = jsonify({
        'locations': util.get_locations()
    })
    # Add CORS header to allow cross-origin requests from any domain
    response.headers.add('Access-Control-Allow-Origin', '*')

    # Return the JSON response
    return response


# Endpoint to predict home price
@app.route('/predict_home_price', methods=['GET', 'POST'])
def predict_home_price():
    # Extract input features from the form data
    total_sqft = float(request.form['total_sqft'])
    location = request.form['location']
    bhk = int(request.form['bhk'])

    # Get the estimated home price using the util module
    response = jsonify(dict(estimated_price=util.get_estimated_prices(total_sqft, bhk, location)))
    # Add CORS header to allow cross-origin requests from any domain
    response.headers.add('Access-Control-Allow-Origin', '*')

    # Return the JSON response
    return response


# Main block to start the Flask server
if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")

    # Load the saved machine learning model and artifacts
    util.load_artifacts()

    # Run the Flask application on the development server
    app.run()
