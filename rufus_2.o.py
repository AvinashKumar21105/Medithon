import google.generativeai as genai

genai.configure(api_key="AIzaSyA-UjYFpBvXHa7EEXPgVTKB5DuQF8h9wWs")
model = genai.GenerativeModel("gemini-1.5-flash")
data_str = """Personal Details  
• Full Name: John Doe  
• Age: 45  
• Gender: Male  
• Contact Information: +1 123 456 7890  
• Address: 123 Elm Street, Springfield, IL  
• Patient ID: JD456  
Medical History  
• Past Medical Conditions: Hypertension  
• Surgical History: Appendectomy (2010)  
• Family Medical History: Father had diabetes; mother had hypertension  
• Allergies: Penicillin  
• Current Medications: Losartan 50 mg once daily  
Examination Details  
• Date of Examination: 2024 -12-15 
• Reason for Examination: Persistent chest pain  
• Symptoms Reported: Tightness in chest, shortness of breath  
• Physical Examination Findings: Blood Pressure: 150/95 mmHg, Heart Rate: 88 bpm  
Diagnostic Tests  
• List of Tests Conducted: ECG, Blood Test (CBC), Chest X -Ray 
• Results of Tests:  
o ECG: Sinus tachycardia  
o Blood Test: Slightly elevated WBC count  
o Chest X -Ray: No abnormalities  
• Date of Test Reports: 2024 -12-16 
Diagnosis  
• Primary Diagnosis: Angina  
• Secondary Diagnoses: None  
Treatment Plan  
• Prescribed Medications: Aspirin 75 mg daily, Nitroglycerin as needed  
• Recommended Therapies: Cardiologist consultation for stress test  
• Lifestyle Advice: Low -sodium diet, regular exercise  
• Follow -Up Instructions: Review after 2 weeks  
Doctor’s Details  
• Doctor's Name: Dr. Emily Carter  
• Specialty: Cardiology  
• Contact Information: +1 987 654 3210  • Registration Number: CAR12345  
• Signature and Seal: Dr. Emily Carter  """

data_list = ["personalDetails", "medicalHistory",
             "examinationDetails",
             "diagnosticTests",
             "dateOfTestReports",
             "diagnosis",
             "treatmentPlan",
             "doctorDetails"]

data={
"personalDetails": "",
    "medicalHistory": "",
    "examinationDetails": "",
    "diagnosticTests": "",
    "dateOfTestReports": "",
    "diagnosis": "",
    "treatmentPlan": "",
    "doctorDetails": "",
}

for x in data_list:
    response = model.generate_content(f"{data_str}: from the data find the {x} and give it as a single line text")
    content = response.text
    data[x]=content;
print(data)

