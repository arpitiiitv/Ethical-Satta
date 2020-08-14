#!/usr/bin/env python
# coding: utf-8
import pickle
from sklearn.linear_model import Ridge
import pandas as pd
df = pd.read_csv('ipl.csv')
less_useful_columns = ['mid','venue','batsman','bowler','striker','non-striker']
df.drop(labels =less_useful_columns, axis = 1 , inplace = True) 
regular_playing_teams = ['Kolkata Knight Riders', 'Chennai Super Kings', 'Rajasthan Royals','Mumbai Indians',
                         'Kings XI Punjab','Royal Challengers Bangalore', 'Delhi Daredevils', 'Sunrisers Hyderabad']
df = df[(df['bat_team'].isin(regular_playing_teams)) & (df['bowl_team'].isin(regular_playing_teams))]
df = df[df['overs']>=5.0]
df['date'] = df['date'].apply(lambda x:int(x.split('-')[0]))
df = pd.get_dummies(data = df , columns = ['bat_team','bowl_team'])
X_train = df.drop(labels='total',axis=1)[df['date']<=2016]
X_test = df.drop(labels='total',axis=1)[df['date']>=2017]
Y_train = df[df['date']<=2016]['total'].values
Y_test = df[df['date']>=2017]['total'].values
X_train.drop(labels='date',axis=1,inplace=True)
X_test.drop(labels='date',axis=1,inplace=True)
ridge_reg = Ridge(alpha=200, copy_X=True, fit_intercept=True, max_iter=None,
                  normalize=False, random_state=None, solver='auto', tol=0.001)
ridge_reg.fit(X_train,Y_train)
filename = 'first-innings-score-lr-model.pkl'
pickle.dump(ridge_reg, open(filename, 'wb'))
