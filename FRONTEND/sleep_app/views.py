from django.shortcuts import render, redirect
from django.conf import settings
import os
import joblib
import numpy as np
from tensorflow.keras.models import load_model

# -------- LOAD ML MODELS --------
BASE_DIR = settings.BASE_DIR
BACKEND_PATH = os.path.join(BASE_DIR, "..", "BACKEND")

rf_model = joblib.load(os.path.join(BACKEND_PATH, "RF_Sleep.pkl"))
scaler = joblib.load(os.path.join(BACKEND_PATH, "scaler.pkl"))

# Encoders
bmi_encoder = joblib.load(os.path.join(BACKEND_PATH, "bmi_encoder.pkl"))
target_encoder = joblib.load(os.path.join(BACKEND_PATH, "target_encoder.pkl"))

# Deep Learning Models
cnn_model = load_model(os.path.join(BACKEND_PATH, "CNN_Sleep.h5"))
lstm_model = load_model(os.path.join(BACKEND_PATH, "LSTM_Sleep.h5"))



def login_user(request):
    if request.method == "POST":
        username = request.POST.get("name").strip().lower()
        password = request.POST.get("password").strip()

        account_file = os.path.join(BACKEND_PATH, "account.txt")

        with open(account_file, "r") as file:
            for line in file:
                user, pwd = line.strip().split()
                if user.lower() == username and pwd == password:
                    request.session["user"] = username
                    return redirect("home")

        return render(request, "loginPage.html", {"error": "Invalid credentials"})

    return render(request, "loginPage.html")


def logout_user(request):
    request.session.flush()
    return redirect("login_user")


def home_page(request):
    return render(request, "home.html")


def input_page(request):
    return render(request, "inputPage.html")


def about_page(request):
    return render(request, "aboutPage.html")



def predict_output(request):
    if request.method == "POST":

        # ----- 1. GET FORM DATA -----
        age = int(request.POST.get("Age"))
        gender = request.POST.get("Gender")
        occ = int(request.POST.get("Occupation"))   # numeric input from form
        sleep_dur = float(request.POST.get("SleepDuration"))
        quality = int(request.POST.get("QualitySleep"))
        activity = int(request.POST.get("Activity"))
        stress = int(request.POST.get("Stress"))
        bmi = request.POST.get("BMI")
        systolic = int(request.POST.get("Systolic"))
        diastolic = int(request.POST.get("Diastolic"))
        hr = int(request.POST.get("HeartRate"))
        steps = int(request.POST.get("Steps"))
        model_type = request.POST.get("ModelType")

        # ----- 2. ENCODE CATEGORICAL VALUES -----
        gender_encoded = 1 if gender == "Male" else 0
        bmi_encoded = bmi_encoder.transform([bmi])[0]

        # ----- 3. CREATE FEATURE VECTOR -----
        input_data = [[
            age,
            gender_encoded,
            occ,          # Already numeric (0–10)
            sleep_dur,
            quality,
            activity,
            stress,
            bmi_encoded,
            systolic,
            diastolic,
            hr,
            steps
        ]]

        # ----- 4. SCALE -----
        input_scaled = scaler.transform(input_data)

        # ----- 5. MODEL SELECTION -----
        if model_type == "RF":
            pred = rf_model.predict(input_scaled)[0]
            model_used = "Random Forest"
            confidence = 96

        elif model_type == "CNN":
            input_cnn = input_scaled.reshape(1, input_scaled.shape[1], 1)
            pred = np.argmax(cnn_model.predict(input_cnn), axis=1)[0]
            model_used = "CNN"
            confidence = 94

        else:  # LSTM
            input_lstm = input_scaled.reshape(1, input_scaled.shape[1], 1)
            pred = np.argmax(lstm_model.predict(input_lstm), axis=1)[0]
            model_used = "LSTM"
            confidence = 92

        # ----- 6. DECODE PREDICTED LABEL -----
        label = target_encoder.inverse_transform([pred])[0]

        # Your dataset mapping:
        disorder = "Insomnia" if label == 0 else "No Disorder" if label == 1 else "Sleep Apnea"

        # ----- 7. PRECAUTIONS -----
        if disorder == "Insomnia":
            tips = [
                "Maintain a regular sleep schedule.",
                "Avoid caffeine late in the evening.",
                "Reduce screen time before sleep.",
                "Practice meditation or breathing exercises."
            ]
        elif disorder == "Sleep Apnea":
            tips = [
                "Avoid sleeping on your back.",
                "Consider weight reduction if overweight.",
                "Consult a doctor about CPAP therapy.",
                "Avoid alcohol before bedtime."
            ]
        else:
            tips = [
                "Maintain healthy lifestyle habits.",
                "Exercise regularly.",
                "Avoid stress to promote good sleep.",
                "Stay hydrated and avoid late-night meals."
            ]

        # Send results to template
        return render(request, "outputPage.html", {
            "disorder": disorder,
            "model_used": model_used,
            "confidence": confidence,
            "tips": tips
        })

    return render(request, "outputPage.html")
