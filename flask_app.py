from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, url_for
from promt import AI
from emergencyData import fastkey as fk
import json
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

def getApi():
    load_dotenv()
    API_KEY = os.getenv("GEMINI_API_KEY")
    return API_KEY



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Emergency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(100), unique=True, nullable=False) # e.g., "Burn"
    heading = db.Column(db.String(255))
    body = db.Column(db.Text) # We'll store the list as a string
    conclusion = db.Column(db.Text)

# Create the DB
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET','POST'])
def index():
    API_KEY = getApi()
    css_ = url_for('static', filename='styles.css')
    answer = None
    submitted = False

    if request.method == "POST":
        submitted = True
        try:
            query = request.form.get("userQuery").lower().strip()
            
            data = Emergency.query.all()
            matched = next((e for e in data if e.keyword in query), None)

            if matched:
                answer = {
                    "responseHeading": matched.heading,
                    "responseBody": json.loads(matched.body),
                    "responseConclusion": matched.conclusion
                }
                
            if not answer:
                for key in fk.EMERGENCY_MAP.keys():
                    if key.lower() in query:
                        # You were missing this line to define 'data'
                        data = fk.EMERGENCY_MAP[key] 
                        answer = {
                            "responseHeading": data["heading"],
                            "responseBody": data["body"], 
                            "responseConclusion": data["conclusion"]
                        }
                        break

            if not answer:
                rawResponse = AI.generate(API_KEY, query)
                
                clean_json = rawResponse.strip()
                if clean_json.startswith("```"):

                    lines = clean_json.splitlines()
                    if len(lines) > 2:
                        clean_json = "\n".join(lines[1:-1])

                try:
                    answer = json.loads(clean_json)
                    
                    exists = Emergency.query.filter_by(keyword=answer['keyword'].lower()).first()
                    if not exists:
                        new_entry = Emergency(
                            keyword=answer['keyword'].lower(),
                            heading=answer['responseHeading'],
                            body=json.dumps(answer['responseBody']),
                            conclusion=answer['responseConclusion']
                        )
                        db.session.add(new_entry)
                        db.session.commit()
                except json.JSONDecodeError as je:
                    print(f"JSON Error: {je} | Raw output was: {rawResponse}")
                    answer = {
                        "responseHeading": "AI Format Error",
                        "responseBody": ["The AI provided a response we couldn't read."],
                        "responseConclusion": "Please try again. Stay safe!"
                    }

        except Exception as e:
            print(f"Error: {e}")
            answer = {"responseHeading": "Error", "responseBody": ["Something went wrong."], "responseConclusion": "Please try again."}
    
    # Always end with render_template
    return render_template('index.html', answer=answer, submit=submitted, css_path=css_)

@app.route('/view-data')
def view_data():
    # Fetch all entries from the SQL database
    all_emergencies = Emergency.query.all()
    
    # Simple HTML table for grunt work debugging
    html = "<h1>Saved Emergency Data</h1><table border='1'>"
    html += "<tr><th>Keyword</th><th>Heading</th><th>Body</th></tr>"
    
    for e in all_emergencies:
        html += f"<tr><td>{e.keyword}</td><td>{e.heading}</td><td>{e.body}</td></tr>"
    
    html += "</table>"
    return html

if __name__ == "__main__":
    app.run(debug=True)