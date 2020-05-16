# pumped
Breast-pumping today is often a stressful, painful, and ineffective process for many women. For women who want to feed their child breastmilk but also want to work, breast-pumping is their only option. Our project, Ada, aims to improve on the breast-pumping experience by innovating on the form factor and adding personalized pumping tips via an app. The code in this repo represents the data analytics involved in the personalization component of Ada. 

##fake_macro.py
This file contains the generator for the synthetic pumping data used to train the personalization algorithms. One of the largest challenges behind innovating on breast-pumping is very little data is available on pumping volumes, patterns, and changes within and among women. Using research and available information, factors contributing to a milk flow rate were determined. Random white noise was added to these factors to create a statistically realistic model of a woman's breast-pumping patterns. The following features are included within the synthetic data:
- time of day
- length of session
- frequency of sessions in a day
- pump power level
- let down length

##anomaly_detection.py
This file uses a moving average and a percentage difference to detect major changes within letdown time and milk production. This alerts women if there are any major changes in their normal milk production, enabling them to proactively seek medical advice if needed.

##linear_regression.py
This file analyses the various factors contributing to the milk rate from the synthetic data, and produces a line of best fit. Based on this line, and the coefficients of each parameter, recommendations can be made so that a woman can optimize her pumping routine. Pandas and numpy are used to preprocess the data. Sklearn is used to create a 6th degree polynomial, and a linear regression classifier is used to train and test data.
Depending on the number of data points provided (meaning, the number of pumping sessions produced by the synthetic data generator) regression model results in, on average, 95% accuracy. 

##classification.py
The classification.py code uses a KNN classifier from the sklearn module to group pumping sessions into high, medium, and low volume sessions. This information is then graphed, providing a visual representation of how certain features can impact pumping output.

##app.py
This file contains the commands needed to send and fetch data from the GCP Firebase database being used to store the app data. 