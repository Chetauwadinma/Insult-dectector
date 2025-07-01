# app.py

import pandas as pd
import numpy as np
import pickle
# Let's pretend you use scikit-learn in your model
from sklearn.ensemble import RandomForestClassifier
from flask import Flask, request, jsonify, render_template

# --- Create a Flask application ---
app = Flask(__name__)

# --- Load the pre-trained model and vectorizer ---
# Use a try-except block to catch errors if files are missing
try:
    # Your model is the Support Vector Classifier (SVC) you trained last
    model = pickle.load(open('model.pkl', 'rb'))
    # Your vectorizer was fitted on the original, uncleaned text
    vectorizer = pickle.load(open('cv.pkl', 'rb'))
    print("Model and vectorizer loaded successfully.")
except FileNotFoundError:
    print("FATAL ERROR: 'model.pkl' or 'cv.pkl' not found.")
    print("Please make sure the pickle files are in the same directory as app.py.")
    exit() # Stop the app if files are missing

# --- Define a route for the home page ---
# This function serves the index.html file to the user's browser
@app.route('/')
def home():
    return render_template('index.html')

# --- Define a route for the prediction ---
# This function is called by the JavaScript in your HTML
@app.route('/predict', methods=['POST'])
def predict():
    # 1. Get the user input from the form
    user_input = request.form['text']
    
    # 2. IMPORTANT: DO NOT pre-process the text (no .lower(), no cleaning)
    #    Your vectorizer was trained on raw text, so it expects raw text.
    
    # --- Debugging: Print to the terminal to see what the server receives ---
    print(f"Received raw input: '{user_input}'")
    # --------------------------------------------------------------------------

    # 3. Vectorize the raw input text
    input_vector = vectorizer.transform([user_input])
    
    # 4. Make a prediction
    prediction = model.predict(input_vector)
    
    # 5. Get the output. It will be a string: 'Clean' or 'offensive'
    output = prediction[0]
    
    # --- Debugging: Print the model's prediction to the terminal ---
    print(f"Model prediction is: '{output}'")
    # ---------------------------------------------------------------
    
    # 6. Return the string prediction as a JSON response
    #    The JavaScript will check if this string is 'offensive'
    return jsonify({'prediction': output})


# --- Run the app ---
if __name__ == "__main__":
    # debug=True will automatically reload the server when you save the file
    app.run(debug=True)
