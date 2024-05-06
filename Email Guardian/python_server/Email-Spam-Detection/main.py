import pickle
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
import string
from nltk.stem.porter import PorterStemmer
from sklearn.ensemble import RandomForestClassifier
from flask_cors import CORS
ps = PorterStemmer()
def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)
    y = []
    for i in text:
        if i.isalnum():
            y.append(i)
    text = y[:]
    y.clear()
    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)
    text = y[:]
    y.clear()
    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)

#final function
tfidf=pickle.load(open('vectorizer.pkl','rb'))
model : RandomForestClassifier =pickle.load(open('model.pkl','rb'))

def check_for_spam(input_email):
    transform_txt=transform_text(input_email)
    vector_input=tfidf.transform([transform_txt])   #vectorization

    result=model.predict(vector_input) #predict
    if result[0] == 1:
        return "spam"
    else:
        return "ham"

def check_for_spam2(input_email):
    transform_txt=transform_text(input_email)
    vector_input=tfidf.transform([transform_txt])   #vectorization

    result=model.predict_proba(vector_input) #predict
    if result[0][1] > 0.5:
        return f"spam ({result[0][1] * 100}%)"
    else:
        return f"ham({result[0][0] * 100}%)"


# here you can implement API call to retrieve the email input from Chrome extension
from flask import Flask, request, jsonify

app = Flask(__name__)
CORS(app)

# Define a route to handle incoming data
@app.route('/email_spam', methods=['POST'])
def receive_data():
    data = request.json
    # Process the received data here
    print("Received data:", data)
    result = check_for_spam2(data['content'])
    print("Result : ", result)
    return jsonify({
        'result': result,
        'status': 'success'
    })

if __name__ == '__main__':
    # Run the Flask app, listening on port 5000 by default
    app.run(debug=True, port=5000)


#--------------------------------




#print("Probability : ")
#print(model.predict_proba(vector_input))
    
    



