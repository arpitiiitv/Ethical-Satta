from flask import Flask, render_template, request
import pickle
import numpy as np
app = Flask(__name__)


filename = 'first-innings-score-lr-model.pkl'
with open(filename, 'rb') as f:
    ridge_reg = pickle.load(f)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        form_data = list()
        total_score = request.form['runs']
        wicket = request.form['wickets']
        over = float(request.form['overs'])
        runs_in_last5 = request.form['runs_in_prev_5']
        wicket_int_last5 = request.form['wickets_in_prev_5']
        form_data = [int(total_score),int(wicket),float(over),int(runs_in_last5),int(wicket_int_last5)]

        bat_team = request.form['batting-team']
        if bat_team == "Chennai Super Kings":
            form_data = form_data + [1, 0, 0, 0, 0, 0, 0, 0]
        elif bat_team == 'Delhi Daredevils':
            form_data = form_data + [0, 1, 0, 0, 0, 0, 0, 0]
        elif bat_team == 'Kings XI Punjab':
            form_data = form_data + [0, 0, 1, 0, 0, 0, 0, 0]
        elif bat_team == 'Kolkata Knight Riders':
            form_data = form_data + [0, 0, 0, 1, 0, 0, 0, 0]
        elif bat_team == 'Mumbai Indians':
            form_data = form_data + [0, 0, 0, 0, 1, 0, 0, 0]
        elif bat_team == 'Rajasthan Royals':
            form_data = form_data + [0, 0, 0, 0, 0, 1, 0, 0]
        elif bat_team == 'Royal Challengers Bangalore':
            form_data = form_data + [0, 0, 0, 0, 0, 0, 1, 0]
        else:
            form_data = form_data + [0, 0, 0, 0, 0, 0, 0, 1]

        bowl_team = request.form['Bowling-team']
        if bowl_team == "Chennai Super Kings":
            form_data = form_data + [1, 0, 0, 0, 0, 0, 0, 0]
        elif bowl_team == 'Delhi Daredevils':
            form_data = form_data + [0, 1, 0, 0, 0, 0, 0, 0]
        elif bowl_team == 'Kings XI Punjab':
            form_data = form_data + [0, 0, 1, 0, 0, 0, 0, 0]
        elif bowl_team == 'Kolkata Knight Riders':
            form_data = form_data + [0, 0, 0, 1, 0, 0, 0, 0]
        elif bowl_team == 'Mumbai Indians':
            form_data = form_data + [0, 0, 0, 0, 1, 0, 0, 0]
        elif bowl_team == 'Rajasthan Royals':
            form_data = form_data + [0, 0, 0, 0, 0, 1, 0, 0]
        elif bowl_team == 'Royal Challengers Bangalore':
            form_data = form_data + [0, 0, 0, 0, 0, 0, 1, 0]
        else:
            form_data = form_data + [0, 0, 0, 0, 0, 0, 0, 1]
        data = np.array([form_data])
        pred = ridge_reg.predict(data)
        # print(bat_team, bowl_team, total_score, wicket, over, runs_in_last5 , wicket_int_last5 , pred)
        return render_template('result.html', lower = int(pred)-5 , upper = int(pred)+10)
    except Exception as e:
        return "Please Fill the details"

app.run(debug=True)