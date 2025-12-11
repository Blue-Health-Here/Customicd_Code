
# from flask import Flask, render_template, request, jsonify
# import json

# app = Flask(__name__)

# with open("medication_icd10.json") as f:
#     med_to_icd = json.load(f)

# @app.route("/")
# def form():
#     return render_template("form.html")

# @app.route("/get_icd10_codes")
# def get_icd10_codes():
#     medication = request.args.get("medication", "").lower()
#     matches = [codes for med, codes in med_to_icd.items() if medication in med.lower()]
#     icd10_codes = sorted(set(code for sublist in matches for code in sublist))
#     return jsonify(icd10_codes)

# @app.route("/submit", methods=["POST"])
# def submit_form():
#     form_data = {
#         "from": request.form.get("from"),
#         "key": request.form.get("key"),
#         "rejection_claim": request.form.get("rejection_claim"),
#         "medication": request.form.get("medication"),
#         "icd_code": request.form.get("icd_code")
#     }

#     print("📥 Received Form Submission:")
#     print(form_data)

#     return f"<h3>Form Submitted Successfully!</h3><pre>{form_data}</pre>"

# if __name__ == "__main__":
#     app.run(debug=True, host='0.0.0.0', port=5050)







######################## with description suggestion ##################################################################################


from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

with open("medication_dict_icd_description.json", encoding="utf-8") as f:
    med_to_icd = json.load(f)

@app.route("/")
def form():
    return render_template("form.html")

@app.route("/get_icd10_codes")
def get_icd10_codes():
    """
    Returns a list of unique {code, description} for medications matching the query.
    Works whether JSON entries are strings (code only) or dicts with description.
    """
    medication = request.args.get("medication", "").lower()
    results = []
    seen_codes = set()

    for med, entries in med_to_icd.items():
        if medication in med.lower():
            for item in entries:
                # Support both formats:
                # 1) "F20.9"
                # 2) {"ICD_10_Code": "...", "ICD_Description": "..."} or similar
                if isinstance(item, str):
                    code = item.strip().upper()
                    desc = ""
                else:
                    code = (item.get("ICD_10_Code") or item.get("ICD-10 Code") or "").strip().upper()
                    desc = (item.get("ICD_Description") or item.get("ICD description") or "").strip()

                if code and code not in seen_codes:
                    seen_codes.add(code)
                    results.append({"code": code, "description": desc})

    # Sort by code
    results.sort(key=lambda x: x["code"])
    return jsonify(results)

@app.route("/submit", methods=["POST"])
def submit_form():
    form_data = {
        "from": request.form.get("from"),
        "key": request.form.get("key"),
        "rejection_claim": request.form.get("rejection_claim"),
        "medication": request.form.get("medication"),
        "icd_code": request.form.get("icd_code"),
        "icd_description": request.form.get("icd_description")  # optional
    }
    print("📥 Received Form Submission:")
    print(form_data)
    return f"<h3>Form Submitted Successfully!</h3><pre>{form_data}</pre>"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5050)







# import os
# import time
# import pandas as pd
# import google.generativeai as genai

# # Set your Gemini API key
# GEMINI_API_KEY = 'AIzaSyDJmR-IkWoIPbZ1cPpfLa3RfUp-M76HpEA'
# if not GEMINI_API_KEY:
#     raise EnvironmentError("Please set the GEMINI_API_KEY environment variable.")

# # Configure Gemini
# genai.configure(api_key=GEMINI_API_KEY)

# SYSTEM_INSTRUCTION = (
#     "You are a medical coding assistant. "
#     "Given an ICD-10 code, respond with exactly one short sentence: "
#     "'<ICD-10 code> stands for <diagnosis name>.' "
#     "Do not add any other information or explanations."
# )

# USER_PROMPT_TEMPLATE = "ICD-10 code: {icd}\nMedication (context only): {med}"


# def init_model():
#     return genai.GenerativeModel(
#         model_name="gemini-1.5-pro",
#         system_instruction=SYSTEM_INSTRUCTION
#     )

# def call_gemini(model, icd, med, max_retries=5, backoff=1.5):
#     prompt = USER_PROMPT_TEMPLATE.format(icd=icd.strip(), med=med.strip())
#     for attempt in range(1, max_retries + 1):
#         try:
#             resp = model.generate_content(prompt)
#             text = (resp.text or "").strip()
#             if text:
#                 return text
#             raise ValueError("Empty response text")
#         except Exception as e:
#             if attempt == max_retries:
#                 return f"[Generation failed after {max_retries} attempts: {e}]"
#             time.sleep(backoff ** (attempt - 1))

# def main():
#     input_csv = "Medication___ICD-10__Complete_.csv"
#     output_csv = "Medication___ICD-10__Complete_description.csv"

#     df = pd.read_csv(input_csv)
#     if "Medication" not in df.columns or "ICD-10 Code" not in df.columns:
#         raise ValueError("CSV must have columns: 'Medication' and 'ICD-10 Code'")

#     model = init_model()
#     cache = {}
#     descriptions = []

#     for _, row in df.iterrows():
#         med = str(row["Medication"]) if pd.notna(row["Medication"]) else ""
#         icd = str(row["ICD-10 Code"]) if pd.notna(row["ICD-10 Code"]) else ""
#         if not icd.strip():
#             descriptions.append("[No ICD code provided]")
#             continue

#         if icd not in cache:
#             cache[icd] = call_gemini(model, icd, med)
#             print(f'done for: {icd}')
#             time.sleep(0.2)  # adjust if needed

#         descriptions.append(cache[icd])

#     df["ICD description"] = descriptions
#     df.to_csv(output_csv, index=False)
#     print(f"✅ Done. Saved to {output_csv}")

# if __name__ == "__main__":
#     main()



# import csv
# import json

# # CSV file ka path yahan den
# csv_file = "Medication___ICD-10__Complete_description.csv"

# # Medication-based dictionary banane ke liye empty dict
# med_dict = {}

# with open(csv_file, mode='r', encoding='utf-8-sig') as file:
#     reader = csv.DictReader(file)
#     for row in reader:
#         med = row['Medication'].strip()
#         if med not in med_dict:
#             med_dict[med] = []
#         med_dict[med].append({
#             "ICD_10_Code": row['ICD-10 Code'].strip(),
#             "ICD_Description": row['ICD description'].strip()
#         })

# # JSON format me pretty print
# print(json.dumps(med_dict, indent=4, ensure_ascii=False))

# # Agar file me save karna ho
# with open("medication_dict_icd_description.json", "w", encoding="utf-8") as json_file:
#     json.dump(med_dict, json_file, indent=4, ensure_ascii=False)
