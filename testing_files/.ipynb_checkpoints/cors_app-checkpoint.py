from flask import Flask, request, jsonify
from flask_cors import CORS  # You may need to install this: pip install flask-cors

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>CORS Test</title>
    </head>
    <body>
        <h1>URL Checker with CORS</h1>
        <form id="urlForm">
            <input type="text" id="url" placeholder="Enter URL">
            <button type="submit">Check</button>
        </form>
        <div id="result"></div>
        
        <script>
            document.getElementById('urlForm').addEventListener('submit', function(e) {
                e.preventDefault();
                const url = document.getElementById('url').value;
                document.getElementById('result').innerText = 'Processing...';
                
                fetch('/predict', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ url: url }),
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('result').innerText = JSON.stringify(data);
                })
                .catch(error => {
                    document.getElementById('result').innerText = 'Error: ' + error;
                });
            });
        </script>
    </body>
    </html>
    """

@app.route('/predict', methods=['POST'])
def predict():
    print("Request received at /predict")
    try:
        data = request.get_json()
        return jsonify({
            "success": True,
            "message": f"Processed URL: {data.get('url', 'No URL provided')}",
            "prediction": [0.7, 0.3]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5002)