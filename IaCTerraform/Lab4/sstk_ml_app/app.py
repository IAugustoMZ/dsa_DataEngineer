# API creation for consuming the trained model
import os
import json
import joblib
import warnings
import pandas as pd
from flask import Flask, request, render_template

# ignore warnings
warnings.filterwarnings('ignore')

# create the app
app = Flask(__name__)

# load the model
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model', 'predictive_maintenance_model.pkl')
model = joblib.load(MODEL_PATH)

# load the model metadata
METADATA_PATH = os.path.join(os.path.dirname(__file__), 'model', 'metadata.json')
with open(METADATA_PATH, 'r') as file:
    metadata = json.load(file)

# convert metadata min and max to str
for item in metadata['features']:
    metadata['features'][item]['min'] = str(metadata['features'][item]['min'])
    metadata['features'][item]['max'] = str(metadata['features'][item]['max'])

# route for main page
@app.route('/')
def home():
    return render_template('index.html', pred_features=metadata)

# route for prediction
@app.route('/predict', methods=['POST'])
def predict():
    
    # get the input data
    sensor = pd.DataFrame(
        columns=list(request.form.keys())
    )
    sensor.loc[0, :] = [float(value) for value in request.form.values()]

    # make prediction
    failure = model.predict(sensor)[0]
    prob = model.predict_proba(sensor)[0][1]

    # interpret result
    if failure == 1:
        text = 'The turbofan will fail in the next 30 cycles. (Probability: {:.2f} %)'.format(prob * 100)
    else:
        text = 'The turbofan will not fail in the next 30 cycles. (Probability: {:.2f} %)'.format((1 - prob) * 100)

    text2 = {k: v for k, v in request.form.items()}

    return render_template(
        'index.html',
        prediction_text=text,
        pred_features=metadata,
        sensor_text=text2
    )

# run the app
if __name__ == '__main__':
    app.run(debug=True)
