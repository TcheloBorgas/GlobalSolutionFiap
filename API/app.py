from flask import Flask, request, jsonify
from pycaret.regression import load_model, predict_model
import pandas as pd

app = Flask(__name__)
model = load_model(r'API\modelo_navegacao_otimizado')  # Carregar o modelo treinado

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    df = pd.DataFrame([data])
    predictions = predict_model(model, data=df)
    output = predictions['Label'][0]
    return jsonify({'prediction': output})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)