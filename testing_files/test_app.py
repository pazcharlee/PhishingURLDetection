from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test App</title>
    </head>
    <body>
        <h1>Test Form</h1>
        <form id="testForm">
            <input type="text" id="testInput" placeholder="Enter text">
            <button type="submit">Submit</button>
        </form>
        <div id="result"></div>
        
        <script>
            document.getElementById('testForm').addEventListener('submit', function(e) {
                e.preventDefault();
                const text = document.getElementById('testInput').value;
                
                fetch('/test', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ text: text }),
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('result').innerText = data.message;
                })
                .catch(error => {
                    document.getElementById('result').innerText = 'Error: ' + error;
                });
            });
        </script>
    </body>
    </html>
    """

@app.route('/test', methods=['POST'])
def test():
    print("Request received at /test")
    data = request.get_json()
    print("Received data:", data)
    return jsonify({"message": f"You sent: {data.get('text', 'no text')}"})

if __name__ == '__main__':
    app.run(debug=True)