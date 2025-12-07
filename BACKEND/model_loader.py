import os
import joblib
from django.conf import settings
import numpy as np
import platform

# Detect OS
IS_WINDOWS = platform.system() == "Windows"

# Backend path
BACKEND_DIR = settings.BASE_DIR.parent / "BACKEND"

# Cache models
_models = {
    "rf": None,
    "scaler": None,
    "occ": None,
    "bmi": None,
    "target": None,
    "cnn": None,
    "lstm": None,
    "cnn_tflite": None,
    "lstm_tflite": None,
}

# ------------------ TFLITE LOADING ---------------------

def load_tflite_model(path):
    import tflite_runtime.interpreter as tflite
    interpreter = tflite.Interpreter(model_path=str(path))
    interpreter.allocate_tensors()
    return interpreter

def predict_tflite(interpreter, input_array):
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    interpreter.set_tensor(input_details[0]["index"], input_array.astype(np.float32))
    interpreter.invoke()
    output = interpreter.get_tensor(output_details[0]["index"])
    return np.argmax(output, axis=1)[0]


# ------------------ GET MODEL --------------------------

def get_model(name):
    global _models

    # ---------- RANDOM FOREST ----------
    if name == "rf":
        if _models["rf"] is None:
            _models["rf"] = joblib.load(BACKEND_DIR / "RF_Sleep.pkl")
        return _models["rf"]

    # ---------- SCALER / ENCODERS ----------
    if name in ["scaler", "occ", "bmi", "target"]:
        if _models[name] is None:
            filename = "scaler.pkl" if name == "scaler" else f"{name}_encoder.pkl"
            _models[name] = joblib.load(BACKEND_DIR / filename)
        return _models[name]

    # ---------- CNN MODEL ----------
    if name == "cnn":
        if IS_WINDOWS:
            # Load Keras H5 model locally
            from tensorflow.keras.models import load_model
            if _models["cnn"] is None:
                _models["cnn"] = load_model(BACKEND_DIR / "CNN_Sleep.h5")
            return _models["cnn"]
        else:
            # Load TFLite model on Render
            if _models["cnn_tflite"] is None:
                _models["cnn_tflite"] = load_tflite_model(BACKEND_DIR / "CNN_Sleep_quantized.tflite")
            return _models["cnn_tflite"]

    # ---------- LSTM MODEL ----------
    if name == "lstm":
        if IS_WINDOWS:
            from tensorflow.keras.models import load_model
            if _models["lstm"] is None:
                _models["lstm"] = load_model(BACKEND_DIR / "LSTM_Sleep.h5")
            return _models["lstm"]
        else:
            if _models["lstm_tflite"] is None:
                _models["lstm_tflite"] = load_tflite_model(BACKEND_DIR / "LSTM_Sleep_quantized.tflite")
            return _models["lstm_tflite"]

    return None
