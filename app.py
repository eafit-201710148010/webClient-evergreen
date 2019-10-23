from flask import Flask,jsonify, request, render_template
from flask_cors import CORS
from datetime import datetime
import requests


app = Flask(__name__, template_folder='templates')
CORS(app)

mediciones_list = [
    {'fecha': '10/09/2019', 'origen': 'Sensor en terreno', 'valor':85,
    'codigoSensor':'70ZH', 'observacion': 'en servicio' },
    {'fecha': '11/09/2019', 'origen': 'Dato derivado', 'valor':35,
    'codigoSensor':'300DK', 'observacion': 'resultado positivo' }
]


origenes_list = ['Sensor en terreno', 'Imagen satelital', 'Imagen dron', 'Dato derivado']

medicionesV = []

@app.route("/")
def get():
    
    return jsonify(mediciones_list)

@app.route('/crearMedicion', methods=['GET'])
def crearMedicion():
    return render_template('crearMedicion.html', origenes=origenes_list)

@app.route("/crearMedicion",methods=['POST'])
def crearMedicionr():
    
    fecha = str(request.form['txtFecha'])
    origen = str(request.form['origen'])
    valor = str(request.form['txtValor'])
    codigoSensor = str(request.form['txtCodigoSensor'])
    observacion = str(request.form['txtObservacion'])

    mediciones = {'Fecha': fecha, 'Origen': origen, 'Valor': valor,
            'CodigoSensor': codigoSensor, 'Observacion': observacion}

    requests.post('https://apy-evergreenscastri.azurewebsites.net', json=mediciones)

    #medicionesV.append(mediciones)
    #mediciones_list.append(mediciones)
    #return jsonify(medicionesV)

    return listarMediciones()

@app.route('/listarMediciones', methods=['GET'])
def listarMediciones():
    mediciones_list = requests.get('https://apy-evergreenscastri.azurewebsites.net').json()
    return render_template('listarMediciones.html', mediciones=mediciones_list)

@app.route('/guardarMedicion', methods=['POST'])
def guardarMedicion():
    medicion = dict(request.values)
    
    medicion['valor'] = int(medicion['precio'])
    mediciones_list.append(medicion)
    requests.post('https://apy-evergreenscastri.azurewebsites.net',json=medicion)
  
    #return(mediciones())
    return render_template('listarMediciones.html', mediciones=mediciones_list)


