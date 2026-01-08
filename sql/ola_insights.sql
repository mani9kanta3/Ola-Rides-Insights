CREATE TABLE rides (
    booking_id VARCHAR PRIMARY KEY,
	customer_id VARCHAR NOT NULL,
    booking_datetime TIMESTAMP NOT NULL,
    booking_date DATE NOT NULL,
    booking_time TIME NOT NULL,
    booking_status VARCHAR NOT NULL,
    vehicle_type VARCHAR NOT NULL,
    pickup_location VARCHAR NOT NULL,
    drop_location VARCHAR NOT NULL,
	incomplete_rides VARCHAR,
	canceled_rides_by_customer VARCHAR,
	canceled_rides_by_driver VARCHAR,
	incomplete_rides_reason VARCHAR,
    ride_distance NUMERIC NOT NULL,
    payment_method VARCHAR,
    driver_ratings NUMERIC,
    customer_rating NUMERIC,
    v_tat NUMERIC,
    c_tat NUMERIC,
    quoted_fare NUMERIC NOT NULL,
    realized_revenue NUMERIC NOT NULL,
    is_success BOOLEAN NOT NULL,
    is_customer_cancel BOOLEAN NOT NULL,
    is_driver_cancel BOOLEAN NOT NULL,
    is_driver_not_found BOOLEAN NOT NULL,
    is_failure BOOLEAN NOT NULL,
    is_incomplete_ride BOOLEAN NOT NULL
); 

--Check Whether Data is loaded or not
SELECT * FROM rides;
SELECT COUNT(*) FROM rides;

-- QUERY 1: Total Successful Bookings
-- Purpose: Identify all bookings that were completed successfully.
-- Business Use: Forms the foundation for revenue, ratings, and distance analysis since only successful rides represent completed transactions.
SELECT *
FROM rides
WHERE is_success = TRUE;

-- QUERY 2: Average Ride Distance by Vehicle Type
-- Purpose: Calculate the average distance travelled for each vehicle category using only successful rides.
-- Business Use: Helps understand usage patterns across vehicle types and supports fleet planning and pricing strategies.
SELECT
    vehicle_type,
    ROUND(AVG(ride_distance), 2) AS avg_ride_distance
FROM rides
WHERE is_success = TRUE
GROUP BY vehicle_type
ORDER BY avg_ride_distance DESC;

-- QUERY 3: Total Customer-Cancelled Rides
-- Purpose: Count the number of bookings cancelled by customers.
-- Business Use: Measures demand-side churn and helps identify customer behavior issues such as change of plans or booking friction.
SELECT
    COUNT(*) AS customer_cancelled_rides
FROM rides
WHERE is_customer_cancel = TRUE;

-- QUERY 4: Top 5 Customers by Number of Bookings
-- Purpose: Identify customers who have made the highest number of ride bookings.
-- Business Use: Highlights high-engagement users who contribute heavily to platform demand and can be targeted for retention or loyalty programs.
SELECT
    customer_id,
    COUNT(*) AS total_bookings
FROM rides
GROUP BY customer_id
ORDER BY total_bookings DESC
LIMIT 5;

-- QUERY 5: Driver Cancellations Due to Personal or Car Issues
-- Purpose: Count rides cancelled by drivers specifically for personal or vehicle-related reasons.
-- Business Use: Helps assess driver reliability and supports operational decisions like driver onboarding, training, or vehicle checks.
SELECT
    COUNT(*) AS driver_personal_car_cancellations
FROM rides
WHERE is_driver_cancel = TRUE
  AND canceled_rides_by_driver = 'Personal & Car related issue';

-- QUERY 6: Driver Rating Extremes for Prime Sedan
-- Purpose: Find the maximum and minimum driver ratings for Prime Sedan bookings.
-- Business Use: Evaluates service quality boundaries within a premium vehicle category and monitors driver performance consistency.
SELECT
    MAX(driver_ratings) AS max_driver_rating,
    MIN(driver_ratings) AS min_driver_rating
FROM rides
WHERE is_success = TRUE
  AND vehicle_type = 'Prime Sedan';

-- QUERY 7: Successful Rides Paid via UPI
-- Purpose: Retrieve all completed rides where UPI was used as the payment method.
-- Business Use: Supports digital payment analysis and helps assess adoption and performance of UPI transactions.
SELECT *
FROM rides
WHERE payment_method = 'UPI'
  AND is_success = TRUE;

-- QUERY 8: Average Customer Rating by Vehicle Type
-- Purpose: Calculate the average customer rating for each vehicle category using only successful rides.
-- Business Use: Compares customer satisfaction across vehicle types and helps prioritize service improvement areas.
SELECT
    vehicle_type,
    ROUND(AVG(customer_rating), 2) AS avg_customer_rating
FROM rides
WHERE is_success = TRUE
GROUP BY vehicle_type
ORDER BY avg_customer_rating DESC;

-- QUERY 9: Total Booking Value of Successful Rides
-- Purpose: Calculate the total quoted booking value for rides that were completed successfully.
-- Business Use: Represents realized demand value and helps evaluate how much attempted booking value converted into completed rides.
SELECT
    SUM(quoted_fare) AS total_successful_booking_value
FROM rides
WHERE is_success = TRUE;

-- QUERY 10: Incomplete Rides with Cancellation Indicators
-- Purpose: List all rides that did not complete along with related cancellation information.
-- Business Use: Used for failure diagnostics to identify operational issues causing ride incompletion.
SELECT
    booking_id,
    booking_datetime,
    vehicle_type,
    incomplete_rides,
    canceled_rides_by_customer,
    canceled_rides_by_driver
FROM rides
WHERE is_incomplete_ride = TRUE;