
import os

import requests
import streamlit as st


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="SuperKart Sales Predictor",
    layout="centered",
)


# ---------------------------------------------------------
# Backend configuration
# ---------------------------------------------------------

BACKEND_URL = "http://backend:7860"

PREDICTION_ENDPOINT = f"{BACKEND_URL}/v1/predict"


# ---------------------------------------------------------
# Page heading
# ---------------------------------------------------------

st.title("SuperKart Sales Prediction")

st.write(
    "Enter the product and store information below to estimate "
    "the expected product sales."
)


# ---------------------------------------------------------
# Session state
# ---------------------------------------------------------

if "predicted_sales" not in st.session_state:
    st.session_state.predicted_sales = None

if "submitted_data" not in st.session_state:
    st.session_state.submitted_data = None


# ---------------------------------------------------------
# Input form
# ---------------------------------------------------------

with st.form("sales_prediction_form",clear_on_submit=False):

    st.subheader("Product Information")
    product_weight = st.number_input("Product Weight",min_value=0.0,value=10.0,step=0.1)
    product_sugar_content = st.selectbox("Product Sugar Content",options=["Low Sugar","Regular","No Sugar"])
    product_allocated_area = st.number_input("Product Allocated Area",min_value=0.0,value=0.05,step=0.01,format="%.3f")
    product_mrp = st.number_input("Product MRP",min_value=0.0,value=150.0,step=1.0)
    product_cat = st.selectbox("Product Category",options=["FD","DR","NC"],help=("FD = Food, DR = Drinks, NC = Non-Consumable"))
    product_type_category = st.selectbox("Product Type Category",options=["Fresh and Perishable","Packaged Food","Beverages","Non-Food"])
    
    st.subheader("Store Information")
    store_size = st.selectbox("Store Size",options=[ "Small","Medium", "High"])
    store_location_city_type = st.selectbox("Store Location City Type",options=[ "Tier 1","Tier 2","Tier 3"])
    store_type = st.selectbox("Store Type",options=[ "Departmental Store","Supermarket Type1","Supermarket Type2", "Food Mart"])
    store_age_years = st.number_input("Store Age in Years",min_value=0,max_value=100,value=20,step=1)

    submitted = st.form_submit_button(
        "Predict Sales",
        use_container_width=True,
    )


# ---------------------------------------------------------
# Submit request to backend
# ---------------------------------------------------------

if submitted:

    request_data = {
        "Product_Weight": float(product_weight),
        "Product_Sugar_Content": product_sugar_content,
        "Product_Allocated_Area": float(product_allocated_area),
        "Product_MRP": float(product_mrp),
        "Store_Size": store_size,
        "Store_Location_City_Type": store_location_city_type,
        "Store_Type": store_type,
        "Store_Age": int(store_age_years),
        "Product_Category": product_cat,
        "Product_Groups": product_type_category,
    }

    try:
        with st.spinner("Generating sales prediction..."):

            response = requests.post(PREDICTION_ENDPOINT,json=request_data,timeout=60)

        if response.status_code == 200:

            response_data = response.json()
            predicted_sales = response_data.get("Sales")

            if predicted_sales is None:
                st.error("The backend response did not contain a Sales prediction.")
                st.json(response_data)

            else:
                st.session_state.predicted_sales = predicted_sales
                st.session_state.submitted_data = request_data

        else:
            st.error(f"Backend returned status code {response.status_code}.")

    except requests.exceptions.ConnectionError:
        st.error(f"Could not connect to the backend API.Verify that the backend is running at {BACKEND_URL}.")


# ---------------------------------------------------------
# Display latest prediction
# ---------------------------------------------------------

if st.session_state.predicted_sales is not None:
    st.success("Prediction generated successfully.")

    st.metric(
        label="Predicted Product Sales",
        value=f"{st.session_state.predicted_sales:,.2f}",
    )

    with st.expander("View submitted input"):
        st.json(st.session_state.submitted_data)
