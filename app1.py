from flask import Flask, render_template, request
import requests
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_message', methods=['POST'])
def submit_message():
    if request.method == 'POST':
        raw_text = request.form['msg']
        date_time = datetime.now().strftime("%H:%M")
        grades = ["1st", "2nd", "3rd", "4th", "1", "2", "3", "4"]
        valid_grades = ["6th", "7th", "8th", "9th", "10th", "11th", "12th", "5th", "5", "6", "7", "8", "9", "10", "11", "12"]

        if raw_text in grades:
            bot_message = "You asked! only 5th to 12th grade ICSE syllabus"
        elif raw_text in valid_grades:
            bot_message = "OK ask!"
        else:
            try:
                response = requests.post("URL KEY",
                                         headers={"Content-Type": "application/json",
                                                  "Authorization": "Bearer API KEY"},
                                         json={"model": "gpt-3.5-turbo",
                                               "messages": [{"role": "user", "content": raw_text}]})
                response_data = response.json()
                bot_message = response_data['choices'][0]['message']['content']
            except Exception as e:
                print("Error fetching or parsing response:", e)
                bot_message = "Sorry, I couldn't understand that."

        return json.dumps({"user_message": raw_text, "bot_message": bot_message, "time": date_time})

if __name__ == '__main__':
    app.run(debug=True)
