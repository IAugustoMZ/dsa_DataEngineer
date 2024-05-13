# API creation for consuming the trained model
import os
import pickle
import warnings
import pandas as pd
from flask import Flask, request, render_template
# from pycaret.classification import load_model, predict_model

# ignore warnings
warnings.filterwarnings('ignore')

# create the app
app = Flask(__name__)

# load the model
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model', 'vote_model.pkl')
# model = load_model(MODEL_PATH)
model = pickle.load(open(MODEL_PATH, 'rb'))

# route for main page
@app.route('/')
def home():
    return render_template('index.html')

# route for prediction
@app.route('/predict', methods=['POST'])
def predict():
    
    # get the input data
    sensor = pd.DataFrame(
        columns=list(request.form.keys())
    )
    sensor.loc[0, :] = [float(value) for value in request.form.values()]

    # make prediction
    # prediction = predict_model(model, sensor)
    failure = model.predict(sensor)[0]
    prob = model.predict_proba(sensor)[0]
    # failure = prediction['prediction_label'][0]
    # prob = prediction['prediction_score'][0]

    # interpret result
    if failure == 1:
        text = 'The turbofan will fail in the next 30 cycles. (Probabability: {:.2f} %)'.format(prob * 100)
    else:
        text = 'The turbofan will not fail in the next 30 cycles. (Probabability: {:.2f} %)'.format(prob * 100)

    return render_template(
        'index.html',
        prediction_text=text
    )

# run the app
if __name__ == '__main__':
    app.run(debug=True)
