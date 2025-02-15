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