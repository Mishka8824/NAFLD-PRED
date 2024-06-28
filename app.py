from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
import joblib
import numpy as np

app = Flask(__name__)
CORS(app, support_credentials=True)

# Loading the ML models
rf = joblib.load('./models/random_forest_model.joblib')
dt = joblib.load('./models/decision_tree_model.joblib')
lr = joblib.load('./models/logistic_regression_model.joblib')
gb = joblib.load('./models/gradient_boosting_model.joblib')

# Defining the form route
@app.route('/')
@cross_origin(supports_credentials=True)
def form():
    return render_template('index.html')

# Defining the prediction route
@app.route('/predict', methods=['POST'])
@cross_origin(supports_credentials=True)
def predict():
    # Getting the form data
    age = float(request.form['age'])
    gender = request.form['male']
    weight = float(request.form['weight'])
    height = float(request.form['height'])
    bmi = float(request.form['bmi'])
    c_h_o_l = float(request.form['c_h_o_l'])
    s_b_p = float(request.form['s_b_p'])
    d_b_p = float(request.form['d_b_p'])
    s_m_o_k_e = float(request.form['s_m_o_k_e'])

    # Preprocessing the data
    male = 1.0 if gender == 'male' else 0.0
    data = np.array([[age, male, weight, height, bmi, c_h_o_l, s_b_p, d_b_p, s_m_o_k_e]]).astype(float)

    # Getting the form data
    form_feature_names = request.form.keys()
    
    # Printing out feature names for debugging
    print("Feature names received from the form:")
    for feature_name in form_feature_names:
        print(feature_name)

    # Printing out form data for debugging
    print("Form data received:")
    print(f"Age: {age}")
    print(f"Gender: {gender}")
    print(f"Weight: {weight}")
    print(f"Height: {height}")
    print(f"BMI: {bmi}")
    print(f"Cholesterol: {c_h_o_l}")
    print(f"SBP: {s_b_p}")
    print(f"DBP: {d_b_p}")
    print(f"Smoking: {s_m_o_k_e}")


    # Printing out data for debugging
    print("Data for prediction:")
    print(data)

    # Making the predictions
    dt_pred = dt.predict(data)[0]
    rf_pred = rf.predict(data)[0]
    lr_pred = lr.predict(data)[0]
    gb_pred = gb.predict(data)[0]

    # Calculating the average prediction
    avg_pred = np.mean([rf_pred, dt_pred, lr_pred, gb_pred])

    # Calculating the confidence score
    results = np.array([rf_pred, dt_pred, lr_pred, gb_pred])
    confidence_score = np.mean(results == round(avg_pred))

    # Determining majority result
    at_risk_count = np.sum(results)
    not_at_risk_count = 4 - at_risk_count
    majority_result = "at_risk" if at_risk_count >= 3 else "not_at_risk"

    # Preparing the results
    predictions = {
        'Random Forest': rf_pred,
        'Decision Tree': dt_pred,
        'Logistic Regression': lr_pred,
        'Gradient Boosting': gb_pred,
        'Average Prediction': avg_pred,
        'Confidence Score': confidence_score
    }

    # Rendering the results template with predictions
    return render_template('pred_results.html', 
                           predictions=predictions,
                           majority_result=majority_result, 
                           at_risk_count=at_risk_count, 
                           not_at_risk_count=not_at_risk_count,
                           confidence_score=confidence_score * 100)

if __name__ == '__main__':
    app.run(debug=True)