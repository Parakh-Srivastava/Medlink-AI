from flask import Flask, render_template, request, url_for
from promt import AI
from emergencyData import fastkey as fk
import json
import os
from dotenv import load_dotenv

app = Flask(__name__)
def getApi():
    load_dotenv()
    API_KEY = os.getenv("GEMINI_API_KEY")
    return API_KEY

@app.route('/', methods=['GET','POST'])
def index():

    API_KEY = getApi()
    css_ = url_for('static', filename='styles.css')
    answer = None
    submitted = False
    data = None

    if request.method == "POST":
        submitted = True

        try:
            query = request.form.get("userQuery").lower().strip()

            for keyword,value in fk.EMERGENCY_MAP.items():
                
                if keyword in query:
                    data = value
                    break
            
            if data:
                answer = {
                    "responseHeading": data["heading"],
                    "responseBody": data["body"],
                    "responseConclusion": data["conclusion"]
                }
            else:
                rawResponse = AI.generate(API_KEY,query)
                answer = json.loads(rawResponse)

        except Exception as e:
            print(f"Error: {e}")
            answer = None
    
    return render_template('index.html', answer=answer, submit=submitted, css_path = css_)

if __name__ == '__main__':
    app.run(debug=True)