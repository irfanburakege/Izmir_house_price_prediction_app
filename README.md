# 🏠 İzmir House Price Predictor

A Machine Learning application that estimates real estate prices in İzmir, Turkey based on district, size, and room count.

🔗 **Live Demo:** [Click Here to Open App](https://irfanburakege-izmir-house-price-pred.streamlit.app)

## 🛠️ Technologies Used
* **Data Engineering:** Python, Selenium (Custom Scraper), BeautifulSoup
* **Machine Learning:** Scikit-Learn (Random Forest Regressor), Pandas, NumPy
* **Deployment:** Streamlit Cloud, CI/CD via GitHub

## 📊 Methodology
1.  **Scraping:** Collected 1,000+ listings from major Turkish real estate platforms using a custom Selenium bot with anti-detection measures.
2.  **Cleaning:** Implemented "Sanity Filters" to remove rental listings, commercial properties, and outliers.
3.  **Feature Engineering:** Solved "Simpson's Paradox" in location data by engineering a `Tier` system (Luxury, Mid, Budget) based on district average price.
4.  **Modeling:** Trained a Random Forest Regressor to handle non-linear relationships between location tiers and price.

## ⚠️ Limitations
* The model does not currently account for "Floor Number" or "View" (Sea/City), which are significant price drivers in İzmir.
* Data is a snapshot from November 2025.