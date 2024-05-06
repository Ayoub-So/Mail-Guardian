from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

f_log = open("log.txt",'w+')
CORS(app)
@app.route('/api/data', methods=['POST'])
def process_data():
    # Check if the request contains JSON data
    print("received = ",request)
    if request.is_json:
        data = request.json
        # Assume the JSON data contains a key called 'data'
        if 'data' in data:
            received_data = data['data']
            # Process the received data (Here, just echoing back)
            print("data body content : "+ received_data)
            f_log.close()
            response = {'message': 'Received data successfully', 'received_data': received_data}
            return jsonify(response), 200
        else:
            return jsonify({'error': 'No data key found in the JSON'}), 400
    else:
        return jsonify({'error': 'Request must be in JSON format'}), 400

if __name__ == '__main__':
    app.run(debug=True)  # You can set debug to False in production


#curl -X POST http://localhost:5000/api/data 'Content-Type: application/json' -d '{"data": "Your JSON data here"}'
