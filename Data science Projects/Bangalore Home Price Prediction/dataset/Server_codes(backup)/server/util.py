import pickle
import json
import numpy as np

# Global variables for storing model-related data
__locations = None
__data_columns = None
__model = None

# Function to get the list of locations
def get_locations():
    return __locations

# Function to load model artifacts
def load_artifacts():
    global __data_columns, __locations, __model  # Fix: Remove assignment here

    # Load data columns (features) from the JSON file
    with open(r"D:\Documents\Machine Learning Cource\Projects\Banglore House price\Server_codes\server\artifacts\X_columns.json", "r") as f:
        __data_columns = json.load(f)["data_columns"]
        __locations = __data_columns[2:]  # Extracting location names from data columns

    # Load the machine learning model from the pickle file
    with open(r"D:\Documents\Machine Learning Cource\Projects\Banglore House price\Server_codes\server\artifacts\banglore_home_prices_model.pickle", "rb") as f:
        __model = pickle.load(f)
    print("Loading saved artifacts completed!")

# Function to get estimated prices based on input features
def get_estimated_prices(sqft, bhk, location):
    x = np.zeros(len(__data_columns))
    try:
        loc_index = __data_columns.index(location.lower())
    except ValueError:
        loc_index = -1

    x[0] = sqft
    x[1] = bhk

    if loc_index >= 0:
        x[loc_index] = 1

    # Predict home prices using the loaded model
    return round(__model.predict([x])[0], 2)

# Entry point when the script is executed
if __name__ == "__main__":
    # Load model artifacts when the script is executed
    load_artifacts()

    # Example: Get and print the estimated price for a specific input
    print(get_estimated_prices(4000, 5, "bisuvanahalli"))
