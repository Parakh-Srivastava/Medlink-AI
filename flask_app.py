from flask import Flask, render_template, request, url_for
from promt import AI
import json
import os
from dotenv import load_dotenv

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])

def getApi():
    load_dotenv()
    API_KEY = os.getenv("GEMINI_API_KEY")
    return API_KEY

def index():

    API_KEY = getApi()
    css_ = url_for('static', filename='styles.css')
    answer = None
    submitted = False

    if request.method == "POST":
        submitted = True

        try:
            query = request.form.get("userQuery")

            rawResponse = AI.generate(API_KEY,query)

            answer = json.loads(rawResponse)


        except (ValueError,TypeError):
            answer = None
    
    return render_template('index.html', answer=answer, submit=submitted, css_path = css_)

if __name__ == '__main__':
    app.run(debug=True)