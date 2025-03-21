from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Explicit Routes</title>
    </head>
    <body>
        <h1>URL Checker (Explicit Routes)</h1>
        <form id="urlForm">
            <input type="text" id="url" placeholder="Enter URL">
            <button type="submit">Check</button>
        </form>
        <div id="result"></div>
        
        <script>
            document.getElementById('urlForm').addEventListener('submit', function(e) {
                e.preventDefault();
                const url = document.getElementById('url').value;
                
                // Use absolute URL path
                const apiUrl = window.location.origin + '/predict';
                console.log("Sending request to:", apiUrl);
                
                fetch(apiUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ url: url }),
                })
                .then(response => {
                    console.log("Response status:", response.status);
                    return response.json();
                })
                .then(data => {
                    console.log("Response data:", data);
                    document.getElementById('result').innerText = JSON.stringify(data);
                })
                .catch(error => {
                    console.error("Error:", error);
                    document.getElementById('result').innerText = 'Error: ' + error;
                });
            });
        </script>
    </body>
    </html>
    """

@app.route('/predict', methods=['POST'])
def predict():
    print("POST request received at /predict")
    try:
        data = request.get_json()
        return jsonify({
            "success": True,
            "message": f"Processed URL: {data.get('url', 'No URL provided')}",
            "prediction": [0.7, 0.3]
        })
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

# Add a GET handler for /predict to see if that's the issue
@app.route('/predict', methods=['GET'])
def predict_get():
    print("GET request received at /predict")
    return jsonify({
        "error": "GET method not supported for /predict. Please use POST."
    }), 405

if __name__ == '__main__':
    app.run(debug=True, port=5003)