# İzmir House Price Predictor

I built this project to learn how to create a complete machine learning application from scratch. As a Computer Engineering student, I wanted to go beyond standard datasets. My goal was to build the entire system myself, starting from collecting the raw data all the way to publishing a live website.

**Live Demo:** [Click Here to Open App](https://irfanburakege-izmir-house-price-pred.streamlit.app)

## Tools I Used
* Python
* Selenium (for scraping)
* Pandas and NumPy (for analysis)
* Scikit Learn (for machine learning)
* Streamlit (for the website)
* Git and GitHub

## How I Built It

### 1. Getting the Data
I decided to build my own dataset instead of downloading one. I wrote a custom bot using Selenium to visit Turkish real estate websites. This was challenging because the websites try to block automated tools. I solved this by adding random delays to the code. This made my bot act more like a human user and allowed me to collect over 1,000 real listings.

### 2. Cleaning the Errors
Real data is very messy. I found many mistakes in the listings, such as houses with 1 square meter of size or rental prices mixed into the sales category. I wrote logic rules to remove these errors. For example, I removed any house listed for less than 500,000 TL because that is not a realistic sale price in İzmir.

### 3. Solving the Location Problem
I ran into a confusing issue during analysis. My model initially thought that bigger houses were cheaper in some districts. This happened because rural areas have large but cheap houses, while the city center has small but expensive apartments. I fixed this by creating a Tier system. I grouped districts into three levels based on their average price. This helped the model understand the difference between a luxury area and a budget area.

### 4. The Prediction Model
I used a Random Forest algorithm for the predictions. I chose this over simple regression because house prices are complex. They do not follow a simple straight line and are heavily influenced by the specific location tier.

## Current Limitations
The model does not know if a house has a sea view or which floor it is on. These are important factors in İzmir that my current data does not capture. Also, these prices are a snapshot from November 2025 and market conditions can change.

**Created by İrfan Burak Ege**