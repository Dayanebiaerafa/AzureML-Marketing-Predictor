import joblib
import pandas as pd
import json
import os

def init():
    global model
    model_path = os.path.join(os.getenv("AZUREML_MODEL_DIR"), "model.pkl")
    print(f"✅ Carregando modelo de: {model_path}")
    model = joblib.load(model_path)

def run(raw_data):
    try:
        data = json.loads(raw_data)
        df = pd.DataFrame(data["input_data"]["data"], columns=data["input_data"]["columns"])
        prediction = model.predict(df)
        return json.dumps({"result": prediction.tolist()})
    except Exception as e:
        return json.dumps({"error": str(e)})
