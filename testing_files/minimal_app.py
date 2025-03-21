from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Minimal URL Checker</title>
    </head>
    <body>
        <h1>URL Checker</h1>
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
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Response status: ' + response.status);
                    }
                    return response.json();
                })
                .then(data => {
                    document.getElementById('result').innerText = JSON.stringify(data);
                })
                .catch(error => {
                    document.getElementById('result').innerText = 'Error: ' + error;
                    console.error('Error:', error);
                });
            });
        </script>
    </body>
    </html>
    """

@app.route('/predict', methods=['POST'])
def predict():
    print("Request received at /predict")
    print("Request method:", request.method)
    print("Request content type:", request.content_type)
    print("Request data:", request.data)
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data received"}), 400
            
        url = data.get('url', 'No URL provided')
        return jsonify({
            "success": True,
            "message": f"Processed URL: {url}",
            "prediction": [0.7, 0.3]
        })
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Using a different port