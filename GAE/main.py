from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    date_value = request.form.get('date')
    time_hour = request.form.get('hour')
    ampm = request.form.get('ampm')
    return render_template('index.html', date=date_value, hour=time_hour, ampm=ampm)


if __name__ == "__main__":
    app.run(debug=True)



#GAEEEEEEEE
from flask import Flask, render_template, request, session

app = Flask(__name__)

app.secret_key = 'johorscrape'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    session['date_value'] = request.form.get('date')
    session['time_hour'] = request.form.get('hour')
    session['ampm'] = request.form.get('ampm')
    return render_template("index.html", method=request.method, date=session.get('date_value'), hour=session.get('time_hour'), ampm=session.get('ampm'))

if __name__ == "__main__":
    app.run(debug=True)




#GAE w ML
from flask import Flask, render_template, request
from datetime import datetime
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)

rfr_model = joblib.load('rfr_model.joblib')
cols = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'hour_sin', 'hour_cos']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.form['date']:
        date_value = request.form.get('date')
        time_hour = request.form.get('hour')
        ampm = request.form.get('ampm')
        input_df = pd.DataFrame(np.zeros((1, 8)), columns=cols)
        date_obj = datetime.strptime(date_value, '%Y-%m-%d')
        day_abbr = date_obj.weekday()
        if day_abbr < 6:
            input_df.iloc[0, day_abbr] = 1
        if ampm == 'PM':
            time_hour = float(time_hour + 12)
        input_df['hour_sin'] = np.sin(2 * np.pi * float(time_hour) / 24)
        input_df['hour_cos'] = np.cos(2 * np.pi * float(time_hour) / 24)
        prediction = rfr_model.predict(input_df)
        return render_template("index.html", date=date_value, time=time_hour, ampm=ampm, pred=round(prediction[0], 3), pic_no=round(prediction[0], 0))
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
