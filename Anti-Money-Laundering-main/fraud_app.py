from flask import Flask, request, jsonify, render_template
import pandas as pd
import joblib
from flask_cors import CORS  # For handling CORS (Cross-Origin Resource Sharing)

# Initialize Flask app
chat_app = Flask(__name__)

# Enable CORS for the app to allow cross-origin requests
CORS(chat_app)

# Load and preprocess the dataset
data_path = './data.csv'  # Ensure the file path is correct
data = pd.read_csv(data_path)

def preprocess_data(data):
    # Clean dataset by removing unnecessary columns and handling missing values
    data_cleaned = data.drop(columns=['Unnamed: 0', 'nameOrig', 'nameDest'], errors='ignore')
    for col in data_cleaned.columns:
        if data_cleaned[col].dtype == 'object':
            data_cleaned[col] = data_cleaned[col].fillna(data_cleaned[col].mode()[0])
        else:
            data_cleaned[col] = data_cleaned[col].fillna(data_cleaned[col].mean())
    return data_cleaned

data = preprocess_data(data)

# Load the trained fraud detection model
model = joblib.load('fraud_model.pkl')

# Simple intent detection based on keywords
def detect_intent(user_message):
    user_message = user_message.lower()
    if "fraud" in user_message and "transaction" in user_message:
        return "find_fraud"
    elif "help" in user_message:
        return "help"
    elif "show all" in user_message:
        return "show_all"
    else:
        return "unknown"

# Handle intents
def handle_intent(intent, user_message):
    if intent == "find_fraud":
        frauds = data[data['isFraud'] == 1]
        response = {
            "message": f"Found {len(frauds)} fraud transactions.",
            "transactions": frauds.head(5).to_dict(orient='records')  # Display top 5 as example
        }
    elif intent == "help":
        response = {
            "message": "I can help you with the following queries:\n- Show fraud transactions\n- Show all transactions"
        }
    elif intent == "show_all":
        response = {
            "message": f"Displaying all transactions (top 5 for brevity):",
            "transactions": data.head(5).to_dict(orient='records')
        }
    else:
        response = {"message": "I'm sorry, I didn't understand your query. Try asking about fraud transactions or type 'help'."}
    return response

# Chatbot endpoint
@chat_app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    intent = detect_intent(user_message)
    response = handle_intent(intent, user_message)
    return jsonify(response)

# Frontend endpoint
@chat_app.route('/')
def index():
    return render_template('index.html')

# Run the Flask app
if __name__ == '__main__':
    chat_app.run(debug=True, port=5001)
