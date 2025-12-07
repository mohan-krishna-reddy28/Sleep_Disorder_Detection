from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import logout
import os
import numpy as np

from model_loader import get_model, predict_tflite, IS_WINDOWS


# --------------------------------------------------
# LOGIN
# --------------------------------------------------

def login_user(request):
    if request.method == "POST":
        name = request.POST.get("name").strip()
        password = request.POST.get("password").strip()

        account_file = settings.BASE_DIR.parent / "BACKEND" / "account.txt"

        users = []
        with open(account_file, "r") as file:
            for line in file:
                u, p = line.strip().split()
                users.append((u.lower(), p.strip()))

        for user, pwd in users:
            if user == name and pwd == password:
                return redirect("home")

        return render(request, "loginpage.html", {"error": "Invalid credentials"})

    return render(request, "loginpage.html")


def logout_user(request):
    logout(request)
    return redirect("login")


# --------------------------------------------------
# STATIC PAGES
# --------------------------------------------------

def home_page(request):
    return render(request, "home.html")

def input_page(request):
    return render(request, "inputpage.html")

def about_page(request):
    return render(request, "aboutpage.html")


# --------------------------------------------------
# PREDICT OUTPUT
# --------------------------------------------------

def predict_output(request):
    if request.method == "POST":

        # ----------- Read Inputs --------------
        age = float(request.POST.get("Age"))
        gender = request.POST.get("Gender")
        occ = request.POST.get("Occupation")
        sleep_dur = float(request.POST.get("SleepDuration"))
        quality = float(request.POST.get("QualitySleep"))
        activity = float(request.POST.get("Activity"))
        stress = float(request.POST.get("Stress"))
        bmi = request.POST.get("BMI")
        systolic = float(request.POST.get("Systolic"))
        diastolic = float(request.POST.get("Diastolic"))
        hr = float(request.POST.get("HeartRate"))
        steps = float(request.POST.get("Steps"))
        model_type = request.POST.get("ModelType")

        # ----------- Value Mapping (if needed) --------------

        # If dropdown uses numbers, uncomment and update mappings
        # Example:
        # OCC_MAP = {
        #     "0": "Software Engineer", "1": "Doctor", ...
        # }
        # occ = OCC_MAP.get(occ, occ)

        # BMI_MAP = {
        #     "0": "Underweight", "1": "Normal", "2": "Overweight", "3": "Obese"
        # }
        # bmi = BMI_MAP.get(bmi, bmi)

        # ----------- Load Encoders --------------
        scaler = get_model("scaler")
        occ_encoder = get_model("occ")
        bmi_encoder = get_model("bmi")
        target_encoder = get_model("target")

        gender_encoded = 1 if gender == "Male" else 0
        occ_encoded = occ_encoder.transform([occ])[0]
        bmi_encoded = bmi_encoder.transform([bmi])[0]

        # ----------- Create Input Vector (12 features) ------
        input_data = np.array([[
            age, gender_encoded, occ_encoded,
            sleep_dur, quality, activity, stress,
            bmi_encoded, systolic, diastolic,
            hr, steps
        ]])

        # Scale
        input_scaled = scaler.transform(input_data)

        # --------------------------------------------------------
        # MODEL PREDICTION (Handles Local H5 + Render TFLite)
        # --------------------------------------------------------

        # ---------- Random Forest ----------
        if model_type == "RF":
            model = get_model("rf")
            pred = model.predict(input_scaled)[0]
            model_used = "Random Forest"

        # ---------- CNN ----------
        elif model_type == "CNN":
            model = get_model("cnn")

            if IS_WINDOWS:
                # H5 model: input shape (1, 12, 1)
                x = input_scaled.reshape(1, 12, 1)
                pred = np.argmax(model.predict(x), axis=1)[0]
                model_used = "CNN"
            else:
                # TFLite CNN: input shape (1, 12, 1, 1)
                x = input_scaled.reshape(1, 12, 1, 1).astype(np.float32)
                pred = predict_tflite(model, x)
                model_used = "CNN"

        # ---------- LSTM ----------
        else:
            model = get_model("lstm")

            if IS_WINDOWS:
                # H5 model: input shape (1, 12, 1)
                x = input_scaled.reshape(1, 12, 1)
                pred = np.argmax(model.predict(x), axis=1)[0]
                model_used = "LSTM"
            else:
                # TFLite LSTM: input shape (1, 12, 1)
                x = input_scaled.reshape(1, 12, 1).astype(np.float32)
                pred = predict_tflite(model, x)
                model_used = "LSTM"


        # ----------- Decode Output Label --------------
        disorder = target_encoder.inverse_transform([pred])[0]

        # ----------- Precautions ------------------------
        precautions = {
            "Insomnia": [
                "Maintain a consistent sleep schedule.",
                "Avoid caffeine after evening.",
                "Limit screen usage before bed.",
                "Practice meditation or relaxation techniques."
            ],
            "Sleep Apnea": [
                "Avoid sleeping on your back.",
                "Lose weight if overweight.",
                "Consult a sleep specialist.",
                "Avoid alcohol before bedtime."
            ],
            "None": [
                "Continue maintaining healthy sleep habits.",
                "Exercise regularly.",
                "Reduce stress with mindfulness.",
                "Avoid heavy meals before sleeping."
            ]
        }

        tips = precautions.get(disorder, [])

        return render(request, "outputpage.html", {
            "disorder": disorder,
            "model_used": model_used,
            "tips": tips
        })

    return render(request, "outputpage.html")
