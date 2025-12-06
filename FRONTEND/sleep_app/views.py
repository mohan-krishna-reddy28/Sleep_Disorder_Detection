from django.shortcuts import render, redirect
from django.conf import settings
import os
import joblib
import numpy as np
from tflite_runtime.interpreter import Interpreter 


BASE_DIR = settings.BASE_DIR
BACKEND_PATH = os.path.join(BASE_DIR, "..", "BACKEND")


rf_model = joblib.load(os.path.join(BACKEND_PATH, "RF_Sleep.pkl"))
scaler = joblib.load(os.path.join(BACKEND_PATH, "scaler.pkl"))


bmi_encoder = joblib.load(os.path.join(BACKEND_PATH, "bmi_encoder.pkl"))
target_encoder = joblib.load(os.path.join(BACKEND_PATH, "target_encoder.pkl"))


cnn_interpreter = Interpreter(
    model_path=os.path.join(BACKEND_PATH, "CNN_Sleep_quantized.tflite")
)
cnn_interpreter.allocate_tensors()


# lstm_interpreter = tflite.Interpreter(
#     model_path=os.path.join(BACKEND_PATH, "LSTM_Sleep_quantized.tflite")
# )
# lstm_interpreter.allocate_tensors()


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

        age = int(request.POST.get("Age"))
        gender = request.POST.get("Gender")
        occ = int(request.POST.get("Occupation"))
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

        # ----- 2. ENCODE -----
        gender_encoded = 1 if gender == "Male" else 0
        bmi_encoded = bmi_encoder.transform([bmi])[0]

        # ----- 3. FEATURE VECTOR -----
        input_data = [[
            age, gender_encoded, occ, sleep_dur, quality, activity, stress,
            bmi_encoded, systolic, diastolic, hr, steps
        ]]

        # ----- 4. SCALE -----
        input_scaled = scaler.transform(input_data)


        if model_type == "RF":
            pred = rf_model.predict(input_scaled)[0]
            model_used = "Random Forest"
            confidence = 96


        else:
            input_data_cnn = input_scaled.reshape(1, input_scaled.shape[1], 1).astype(np.float32)

            input_index = cnn_interpreter.get_input_details()[0]["index"]
            output_index = cnn_interpreter.get_output_details()[0]["index"]

            cnn_interpreter.set_tensor(input_index, input_data_cnn)
            cnn_interpreter.invoke()

            output_data = cnn_interpreter.get_tensor(output_index)[0]
            pred = int(np.argmax(output_data))

            model_used = "CNN (TFLite)"
            confidence = 94


        # else: 
        #     input_data_lstm = input_scaled.reshape(1, input_scaled.shape[1], 1).astype(np.float32)

        #     input_index = lstm_interpreter.get_input_details()[0]["index"]
        #     output_index = lstm_interpreter.get_output_details()[0]["index"]

        #     lstm_interpreter.set_tensor(input_index, input_data_lstm)
        #     lstm_interpreter.invoke()

        #     output_data = lstm_interpreter.get_tensor(output_index)[0]
        #     pred = int(np.argmax(output_data))

        #     model_used = "LSTM (TFLite)"
        #     confidence = 92


        label = target_encoder.inverse_transform([pred])[0]
        disorder = "Insomnia" if label == 0 else "No Disorder" if label == 1 else "Sleep Apnea"


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

        return render(request, "outputPage.html", {
            "disorder": disorder,
            "model_used": model_used,
            "confidence": confidence,
            "tips": tips
        })

    return render(request, "outputPage.html")
