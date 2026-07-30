
# Import necessary libraries
import joblib
import pandas as pd
from flask import Flask, request, jsonify

# Initialize Flask app
superkart_predictor_api = Flask("SuperKart Sales Prediction App")

# Load the trained sales prediction model
model = joblib.load("superkart_sales_forecast_v1_0.joblib")


# Define a route for the home page
@superkart_predictor_api.get("/")
def home():
    return "Welcome to the SuperKart Sales Prediction API"


# Define an endpoint to predict sales for a single product-store record
@superkart_predictor_api.post("/v1/predict")
def predict_sales():

    # Get JSON data from the request
    data = request.get_json()

    # Validate that JSON data was provided
    if data is None:
        return jsonify(
            {
                "error": "Request body must contain valid JSON data."
            }
        ), 400

    try:
        # Extract the model input features.
        # The column names and order must match the training data.
        sample = {
            "Product_Weight": data["Product_Weight"],
            "Product_Sugar_Content": data[ "Product_Sugar_Content"],
            "Product_Allocated_Area": data["Product_Allocated_Area"],
            "Product_MRP": data["Product_MRP"],
            "Store_Size": data["Store_Size"],
            "Store_Location_City_Type": data["Store_Location_City_Type"],
            "Store_Type": data["Store_Type"],
            "Product_Category": data["Product_Category"],
            "Store_Age": data["Store_Age"],
            "Product_Groups": data["Product_Groups"],
        }

        # Convert the extracted data into a DataFrame
        input_data = pd.DataFrame([sample])

        # Generate the sales prediction
        prediction = model.predict(input_data).tolist()[0]

        # Convert NumPy numeric types into a standard Python float
        prediction = float(prediction)

        # Return the prediction as JSON
        return jsonify(
            {
                "Sales": prediction
            }
        ), 200

    except KeyError as error:
        return jsonify(
            {
                "error": f"Missing required input field: {error.args[0]}"
            }
        ), 400

    except Exception as error:
        return jsonify(
            {
                "error": "Unable to generate prediction.",
                "details": str(error),
            }
        ), 500


# Run the Flask app in debug mode
if __name__ == "__main__":
    superkart_predictor_api.run(debug=True)
