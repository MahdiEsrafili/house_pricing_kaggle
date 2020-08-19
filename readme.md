# House Price Prediction

In this project, I'm going to make perdiction of house price by some features. Dataset contains lots of feature, I use some feature selection methods like ANOVA, CHI2, Pearson correlation and other tools to select best features. Also in modeling, I used RandomForest, Adaboost, Linear Regression.
In housing_clean_code.ipynb, pipelining added for multiple processes.

in the housing_clean_code.ipynb, I fitted model and exported it with joblib. because i created custom pipeline, its important to export classes as py file and then importing it in target file.

The Dashboard.py is a simple Dashboard created by Plotly Dash.