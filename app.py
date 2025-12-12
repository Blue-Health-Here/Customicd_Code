
######################## with description suggestion ##################################################################################


from flask import Flask, render_template, request, jsonify
import json
import csv
from pathlib import Path


app = Flask(__name__)

with open("medication_dict_icd_description.json", encoding="utf-8") as f:
    med_to_icd = json.load(f)



# Load ICD-10 CSV ("icd_code_formated.csv")
ICD10_ROWS = []
ICD10_PATH = Path("icd10_diagnosis_codes_formatted.csv")

def _normalize_icd_code(code):
    return "".join(c for c in code.upper() if c.isalnum())

if ICD10_PATH.exists():
    with ICD10_PATH.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        # Accept flexible column names
        code_col = next((h for h in reader.fieldnames if "code" in h.lower()), "Formatted ICD-10 Code")
        dx_col   = next((h for h in reader.fieldnames if "diagnosis" in h.lower()), "Diagnosis")
        for row in reader:
            code = (row.get(code_col) or "").strip()
            dx   = (row.get(dx_col) or "").strip()
            if code and dx:
                ICD10_ROWS.append({"code": code, "diagnosis": dx})



@app.route("/")
def form():
    return "I am flaying!!!!!!!!!"

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


##############  logic for custom ICD code and Dignosis ##########




@app.route("/icd_suggest")
def icd_suggest():
    q = (request.args.get("diagnosis") or "").strip()
    try:
        limit = int(request.args.get("limit", 30))
    except ValueError:
        limit = 30

    norm_q = _normalize_icd_code(q)
    q_lower = q.lower()

    exact_match = []
    other_matches = []
    seen_codes = set()

    for row in ICD10_ROWS:
        code = row.get("code", "")
        dx = row.get("diagnosis", "")
        norm_code = _normalize_icd_code(code)

        # Match either code startswith or diagnosis contains
        match_code = norm_q and norm_code.startswith(norm_q)
        match_dx = q_lower and q_lower in dx.lower()

        if match_code or match_dx:
            result = {"code": code, "diagnosis": dx}

            # Prioritize exact code match
            if norm_q == norm_code and code not in seen_codes:
                exact_match.append(result)
                seen_codes.add(code)
            elif code not in seen_codes:
                other_matches.append(result)
                seen_codes.add(code)

        if len(exact_match) + len(other_matches) >= limit:
            break

    out = exact_match + other_matches
    return jsonify(out[:limit])



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


# # Agar file me save karna ho
# with open("medication_dict_icd_description.json", "w", encoding="utf-8") as json_file:
#     json.dump(med_dict, json_file, indent=4, ensure_ascii=False)
