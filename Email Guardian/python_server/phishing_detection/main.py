from sklearn.tree import DecisionTreeClassifier
from joblib import load
from attrib import extract_features
from flask_cors import CORS
# load the saved model
classifier: DecisionTreeClassifier = load("decision_tree_model.joblib")


# implement the API logic for data retreiving

# url = "https://jhghgjh.com"
# url = "https://1drivemss.click/c/7a7841ab-884e-414e-8301-972b7540f921"
def check_phishing(url: str):
    x_data = []  # it should be a list of 30 elements
    x_data = extract_features(url)
    print(">Features extracted from {url} : ")
    print(x_data)
    for n in range(len(x_data)-1):
        if x_data[n] is None:
            x_data[n] = 0
    # make a prediction
    predictions = classifier.predict([x_data])
    # print(predictions)
    if predictions[0] == 1:
        return "legitimate"
    return "phishing"


def check_phishing_2(url: str):
    x_data = []  # it should be a list of 30 elements
    x_data = extract_features(url)

    # make a prediction
    predictions = classifier.predict_proba([x_data])
    # print(predictions)
    if predictions[0][1] > 0.5:
        return f"legitimate ({predictions[0][1] * 100}%)"
    return f"phishing ({predictions[0][0] * 100}%)"


# API implementation goes here =========================================================
from flask import Flask, request, jsonify

app = Flask(__name__)
CORS(app)


# Define a route to handle incoming data
@app.route('/phishing_detection', methods=['POST'])
def receive_data():
    print(">Received data : ", request.json)
    data = request.json  # Assuming data is sent as JSON
    # Process the received data here
    print(">Processing data ................")
    result = check_phishing(data['url'])
    print(">>URL : ", data['url'], " is ", result)
    return jsonify({'status': 'success', 'result': result})


if __name__ == '__main__':
    app.run(debug=True, port=5002)
