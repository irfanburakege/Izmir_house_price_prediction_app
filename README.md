# İzmir House Price Prediction App 🏠

I wanted to build an ML project with real data.Just me, a browser, and way too many listings in İzmir.
This is a small Streamlit app that estimates house prices based on rooms, size, age, and the district location.

🔗 Live app: [Streamlit link](https://irfanburakege-izmir-house-price-pred.streamlit.app)

## Intro: What this is and why I built it

I built a pipeline that cleans housing listings, clusters districts into economic tiers, trains a model, and serves predictions in a simple web app. My goal was to learn by doing: deal with dirty data, detect outliers, pick a model that fits the problem, and build something people can use.

## How I got the data:

I scraped real listings from İzmir (by using Hepsiemlak.com). The raw data was not friendly:
* Rooms were strings like “2 + 1” and even “Stüdyo”.
* Ages were mixed (“Sıfır Bina”, “10 yaşında”, sometimes 150 years old…).
* District names were buried in long paths like “İzmir / Bornova / …”.
* Sizes had unrealistic values (1 m² to 680 m² popped up). Some were likely land or just wrong.

I hit a wall with bad records, so I cleaned the data:
* Converted room count into integers (2 + 1 -> 3, Stüdyo -> 1).
* Converted ages to numbers (“Sıfır” -> 0, “10 yaşında” -> 10).
* Extracted the district from the text.(İzmir/*Bornova*/Evka-3)
* Removed outliers (price < 500k TL, > 100M TL; size < 30 m², > 400 m²; age >= 90).

After that, correlations made more sense. Price vs size correlation increased from 0.18 to ~0.48.

## Smart engineering: solving location with K-Means

I struggled with location. İzmir has districts where sea view, gardens, and luxury skew everything. Manually ranking districts felt biased.

So I used K-Means on average district prices:
* Grouped districts by their mean price.
* Determined best value for k.
* Applied K-Means with k=4.
* Sorted clusters from cheapest to most expensive and called them Tier 1 to Tier 4.
* Mapped every listing to its tier and used `Tier` as a feature.

This helped the model to know that a home in a Tier 4 district is more expensive.

## The model comparison

I benchmarked a few models on the cleaned features: `Rooms`, `Size_m2`, `Tier`, `Age`.
* Linear Regression: simple, but not good on non-linear data.
* Decision Tree: fast, but unstable.
* Random Forest: solid but not enough.
*Gradient Boost: Best performance. (winner)
So I picked **Gradient Boosting** as the final approach and saved that as the production model (`model.pkl`). The app pulls feature importances directly from it.

## The app:

The app is built with Streamlit.
* Loads the trained Gboost model and the district tier map.
* Lets you pick district, set size(m²), rooms, age.
* Maps your district to its tier and predicts the price.
* Shows feature importances so you can see what drove the estimate.

Just a straight estimate based on the features.

## Built with:

* Jupyter Notebook for EDA, cleaning, clustering, and training.
* Python (scikit-learn, pandas, matplotlib, seaborn).
* Streamlit for the web interface.
* Pickle for model artifacts.

Thanks for reading. If you want to chat about the project or the approach, I’m happy to walk through the notebook and design decisions.

!! Yasal Uyarı: Bu proje tamamen eğitim ve akademik amaçlarla geliştirilmiştir. Kullanılan veriler, halka açık kaynaklardan makine öğrenmesi algoritmalarını test etmek amacıyla örneklenmiştir. Ticari bir amacı yoktur ve veriler gerçek zamanlı piyasa koşullarını yansıtmayabilir.
!! Disclaimer: This project is intended for educational and academic purposes only. The data was sampled from publicly available sources to demonstrate machine learning techniques. It is not intended for commercial use.
