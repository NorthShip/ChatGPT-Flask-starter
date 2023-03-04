from flask import Flask, render_template, request
import openai_secret_manager
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        prompt = request.form['prompt']
        max_tokens = 100

        # Get the API key
        secrets = openai_secret_manager.get_secret("openai")
        api_key = secrets["api_key"]

        # Define the payload
        payload = {
            "prompt": prompt,
            "max_tokens": max_tokens
        }

        # Set the headers
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        # Send the request
        response = requests.post("https://api.openai.com/v1/engines/davinci-codex/completions", headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()["choices"][0]["text"]
        else:
            result = "Error: " + response.text

        return render_template('home.html', result=result)
    else:
        return render_template('home.html')

if __name__ == '__main__':
    app.run()
