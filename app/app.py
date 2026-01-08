import streamlit as st
from db import run_query

# --------------------------------------------------
# Page configuration
# --------------------------------------------------
st.set_page_config(
    page_title="OLA Analytics Platform",
    layout="wide"
)

# --------------------------------------------------
# Header
# --------------------------------------------------
st.title("🚖 OLA Analytics Platform")
st.caption(
    "End-to-end analytics system powered by PostgreSQL, SQL, Power BI, and Streamlit"
)

st.divider()

# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------
st.subheader("📌 Key Performance Indicators")

kpi_query = """
SELECT
    COUNT(*) AS total_bookings,
    SUM(CASE WHEN is_success THEN 1 ELSE 0 END) AS successful_bookings,
    SUM(realized_revenue) AS total_revenue
FROM rides;
"""

kpis = run_query(kpi_query)

col1, col2, col3 = st.columns(3)

col1.metric(
    label="Total Bookings",
    value=int(kpis.loc[0, "total_bookings"])
)

col2.metric(
    label="Successful Bookings",
    value=int(kpis.loc[0, "successful_bookings"])
)

col3.metric(
    label="Total Revenue",
    value=f"{int(kpis.loc[0, 'total_revenue']):,}"
)

st.divider()

# --------------------------------------------------
# SQL QUERIES SECTION
# --------------------------------------------------
st.subheader("📊 Business Insights (SQL Driven)")

# 1. All successful bookings
with st.expander("1️⃣ Retrieve all successful bookings"):
    query = """
    SELECT *
    FROM rides
    WHERE is_success = TRUE;
    """
    st.dataframe(run_query(query), use_container_width=True)

# 2. Average ride distance per vehicle type
with st.expander("2️⃣ Average ride distance by vehicle type"):
    query = """
    SELECT
        vehicle_type,
        ROUND(AVG(ride_distance), 2) AS avg_ride_distance
    FROM rides
    WHERE is_success = TRUE
    GROUP BY vehicle_type
    ORDER BY avg_ride_distance DESC;
    """
    st.dataframe(run_query(query), use_container_width=True)

# 3. Total cancelled rides by customers
with st.expander("3️⃣ Total number of rides cancelled by customers"):
    query = """
    SELECT
        COUNT(*) AS customer_cancelled_rides
    FROM rides
    WHERE is_customer_cancel = TRUE;
    """
    st.dataframe(run_query(query), use_container_width=True)

# 4. Top 5 customers by number of rides
with st.expander("4️⃣ Top 5 customers by highest number of bookings"):
    query = """
    SELECT
        customer_id,
        COUNT(*) AS total_bookings
    FROM rides
    GROUP BY customer_id
    ORDER BY total_bookings DESC
    LIMIT 5;
    """
    st.dataframe(run_query(query), use_container_width=True)

# 5. Driver cancellations due to personal/car issues
with st.expander("5️⃣ Driver cancellations due to personal & car-related issues"):
    query = """
    SELECT
        COUNT(*) AS driver_personal_car_cancellations
    FROM rides
    WHERE is_driver_cancel = TRUE
      AND canceled_rides_by_driver = 'Personal & Car related issue';
    """
    st.dataframe(run_query(query), use_container_width=True)

# 6. Max & Min driver ratings for Prime Sedan
with st.expander("6️⃣ Max & Min driver ratings for Prime Sedan"):
    query = """
    SELECT
        MAX(driver_ratings) AS max_driver_rating,
        MIN(driver_ratings) AS min_driver_rating
    FROM rides
    WHERE is_success = TRUE
      AND vehicle_type = 'Prime Sedan';
    """
    st.dataframe(run_query(query), use_container_width=True)

# 7. Rides paid using UPI
with st.expander("7️⃣ All rides where payment was made using UPI"):
    query = """
    SELECT *
    FROM rides
    WHERE payment_method = 'UPI'
      AND is_success = TRUE;
    """
    st.dataframe(run_query(query), use_container_width=True)

# 8. Average customer rating per vehicle type
with st.expander("8️⃣ Average customer rating per vehicle type"):
    query = """
    SELECT
        vehicle_type,
        ROUND(AVG(customer_rating), 2) AS avg_customer_rating
    FROM rides
    WHERE is_success = TRUE
    GROUP BY vehicle_type
    ORDER BY avg_customer_rating DESC;
    """
    st.dataframe(run_query(query), use_container_width=True)

# 9. Total booking value of successful rides
with st.expander("9️⃣ Total booking value of successfully completed rides"):
    query = """
    SELECT
        SUM(quoted_fare) AS total_successful_booking_value
    FROM rides
    WHERE is_success = TRUE;
    """
    st.dataframe(run_query(query), use_container_width=True)

# 10. Incomplete rides with reasons
with st.expander("🔟 List of all incomplete rides with reasons"):
    query = """
    SELECT
        booking_id,
        booking_datetime,
        vehicle_type,
        canceled_rides_by_customer,
        canceled_rides_by_driver
    FROM rides
    WHERE is_incomplete_ride = TRUE;
    """
    st.dataframe(run_query(query), use_container_width=True)

st.divider()

# --------------------------------------------------
# POWER BI SECTION (LINKED, NOT EMBEDDED)
# --------------------------------------------------
st.subheader("📈 Power BI Dashboard")

st.info(
    "Power BI embedding requires a Pro license. "
    "Due to license limitations, the dashboard is linked below."
)

st.markdown(
    "[🔗 Open Power BI Dashboard](https://app.powerbi.com/groups/me/reports/0c1d285f-a7d4-432d-9e74-563b8a90ea50)",
    unsafe_allow_html=True
)

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.divider()
st.caption(
    "Built with PostgreSQL, SQL, Power BI, and Streamlit • Portfolio-grade analytics system"
)