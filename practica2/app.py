from flask import Flask, jsonify
from statsmodels.tsa.arima_model import ARIMA
import pandas as pd
import pmdarima as pm

app = Flask(__name__)


@app.route('/servicio/v1/prediccion/24horas/')
def prediction24():
    data_humidity = algorithmH(24)
    data_temperature = algorithmT(24)
    data_dict = doDict(data_humidity, data_temperature)

    return jsonify(data_dict)

@app.route('/servicio/v1/prediccion/24horas/')
def prediction48():
    algorithmH(48)
    algorithmT(48)
    data_dict = doDict(data_humidity, data_temperature)

    return jsonify(data_dict)

@app.route('/servicio/v1/prediccion/24horas/')
def prediction72():
    algorithmH(72)
    algorithmT(72)
    data_dict = doDict(data_humidity, data_temperature)

    return jsonify(data_dict)

def algorithmH(hours):
    df = pd.read_csv('test.csv', header=0)

    model = pm.auto_arima(df["humidity"].fillna(0) , start_p=1, start_q=1,
                          test='adf',  # use adftest to find optimal 'd'
                          max_p=3, max_q=3,  # maximum p and q
                          m=1,  # frequency of series
                          d=None,  # let model determine 'd'
                          seasonal=False,  # No Seasonality
                          start_P=0,
                          D=0,
                          trace=True,
                          error_action='ignore',
                          suppress_warnings=True,
                          stepwise=True)

    # Forecast
    n_periods = hours  # One day
    fc, confint = model.predict(n_periods=n_periods, return_conf_int=True)

    # fc contains the forecasting for the next 24 hours.
    print(fc)
    return fc

def algorithmT(hours):
    df = pd.read_csv('test.csv', header=0)

    model = pm.auto_arima(df["temperature"].fillna(0) , start_p=1, start_q=1,
                          test='adf',  # use adftest to find optimal 'd'
                          max_p=3, max_q=3,  # maximum p and q
                          m=1,  # frequency of series
                          d=None,  # let model determine 'd'
                          seasonal=False,  # No Seasonality
                          start_P=0,
                          D=0,
                          trace=True,
                          error_action='ignore',
                          suppress_warnings=True,
                          stepwise=True)

    # Forecast
    n_periods = hours  # One day
    fc, confint = model.predict(n_periods=n_periods, return_conf_int=True)

    # fc contains the forecasting for the next 24 hours.
    print(fc)
    return fc

def doDict(data_humidity, data_temperature):
    data_dict = []
    for i in range(0, 24):
        data = {}
        data["hour"] =i
        data["temperature"] = data_temperature[i]
        data["humidity"] = data_humidity[i]
        data_dict.append(data)

    return data_dict

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)