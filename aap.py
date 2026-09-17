import streamlit as st
import pandas as pd
import joblib

# Load model
model = joblib.load("server_failure_model.pkl")

st.set_page_config(
    page_title="Enterprise Server Failure Prediction",
    page_icon="💻",
    layout="wide"
)

st.title("💻 Enterprise Server Failure Prediction")


st.write(
    """
    Predict whether a server is likely to fail based on
    infrastructure monitoring metrics.
    """
)

st.markdown("""
### Project Objective

This application predicts enterprise server failures using
Machine Learning.

The prediction is based on:

- CPU Usage
- Memory Usage
- Disk Activity
- Network Traffic
- Temperature
- Error Logs
- Maintenance History

The goal is to reduce unexpected downtime.
""")

st.markdown("## 📊 Model Performance")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Accuracy", "99.96%")
col2.metric("Precision", "99.95%")
col3.metric("Recall", "99.97%")
col4.metric("F1 Score", "99.96%")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.header("Server Inputs")

with col2:
    st.header("Server Status")

st.sidebar.header("Server Information")

# ----------------------------
# About Section
# ----------------------------
st.sidebar.title("About")

st.sidebar.info("""
**Enterprise Server Failure Prediction**

🤖 Machine Learning Model: XGBoost

📊 Predicts server failure based on system metrics.

👨‍💻 Developer: Priyanshi Sharma
""")

cpu_usage = st.sidebar.slider("CPU Usage (%)",0,100,50)

memory_usage = st.sidebar.number_input(
    "Memory Usage (GB)",
    value=8.0
)

memory_available = st.sidebar.number_input(
    "Memory Available (GB)",
    value=8.0
)

disk_read = st.sidebar.number_input(
    "Disk Read (MB/s)",
    value=50.0
)

disk_write = st.sidebar.number_input(
    "Disk Write (MB/s)",
    value=40.0
)

network_send = st.sidebar.number_input(
    "Network Send (MB)",
    value=10.0
)

network_receive = st.sidebar.number_input(
    "Network Receive (MB)",
    value=10.0
)

temperature = st.sidebar.number_input(
    "Temperature (°C)",
    value=45.0
)

running_processes = st.sidebar.number_input(
    "Running Processes",
    value=100
)

ping_ms = st.sidebar.number_input(
    "Ping (ms)",
    value=20
)

battery_percent = st.sidebar.slider(
    "Battery (%)",
    0,
    100,
    100
)

dayofweek = st.sidebar.slider(
    "Day of Week",
    0,
    6,
    1
)

disk_usage = st.sidebar.slider(
    "Disk Usage (%)",
    0,
    100,
    60
)
error_logs = st.sidebar.number_input(
    "Error Logs",
    value=0
)

crash_logs = st.sidebar.number_input(
    "Application Crash Logs",
    value=0
)

maintenance = st.sidebar.number_input(
    "Days Since Maintenance",
    value=15
)

hour = st.sidebar.slider("Hour",0,23,12)

day = st.sidebar.slider("Day",1,31,15)

month = st.sidebar.slider("Month",1,12,7)

predict = st.sidebar.button("Predict")

if predict:

    data = pd.DataFrame({

        "cpu_usage":[cpu_usage],
        "memory_usage":[memory_usage],
        "memory_availabale_gb":[memory_available],
        "disk_read_mb":[disk_read],
        "disk_right_md":[disk_write],
        "network_set_mb":[network_send],
        "network_recive_mb":[network_receive],
        "temperature":[temperature],
        "error_logs":[error_logs],
        "application_crash_logs":[crash_logs],
        "days_since_maintenance":[maintenance],
        "hour":[hour],
        "day":[day],
        "month":[month],
        "running_processes":[running_processes],
        "ping_ms":[ping_ms],
        "battery_percent":[battery_percent],
        "dayofweek":[dayofweek],
        "disk_usage":[disk_usage]


    })

    prediction = model.predict(data)[0]
    probability = model.predict_proba(data)[0][1]

    st.subheader("Prediction Result")

    if prediction == 0:
        st.success("🟢 Healthy Server")

    elif probability < 0.70:
        st.warning("🟡 Warning: Monitor the Server")

    else:
        st.error("🔴 Critical: High Risk of Server Failure")

    st.subheader("Failure Probability")

    

    st.metric(
    "Probability",
    f"{probability*100:.2f}%"
)

    st.progress(float(probability))

    st.write(f"Failure Risk: {probability*100:.2f}%")

# Show the values entered by the user
    

    # Show current input values
    st.subheader("Current Server Metrics")
    st.dataframe(data)

# ----------------------------
# Feature Importance
# ----------------------------
    import matplotlib.pyplot as plt

    feature_names = model.named_steps["preprocessor"].get_feature_names_out()

    importance = model.named_steps["classifier"].feature_importances_

    fig, ax = plt.subplots(figsize=(8,6))

    ax.barh(feature_names, importance)

    ax.set_title("Feature Importance")

    st.pyplot(fig)

    # ==========================
# ADD BATCH PREDICTION HERE
# ==========================

st.markdown("---")
st.header("📁 Batch Prediction")

uploaded_file = st.file_uploader(
    "Upload a CSV file",
    type=["csv"]
)

if uploaded_file is not None:

    batch_data = pd.read_csv(uploaded_file)

    predictions = model.predict(batch_data)

    batch_data["Prediction"] = predictions

    st.subheader("Prediction Results")
    st.dataframe(batch_data)

    csv = batch_data.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download Results",
        csv,
        "prediction_results.csv",
        "text/csv"
    )

    # ----------------------------
    # Footer (Add here)
    # ----------------------------
    st.markdown("---")

    st.write(
        "Built using **Streamlit** • **Scikit-Learn** • **XGBoost**"
    ) 