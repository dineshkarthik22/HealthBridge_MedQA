from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from flask_cors import CORS  # import CORS
import os
import json

from response_generator import generate_response_for_subquery, generate_subqueries, evaluate_response
from scraper_and_chunker import process_cleveland_clinic_page

app = Flask(__name__)
CORS(app)  # Use CORS
api = Api(app, version='1.0', title='Patient Query API',
          description='A simple API to handle patient queries')

# Set query model
query_model = api.model('QueryModel', {
    'patient_id': fields.Integer(required=True, description='The ID of the patient'),
    'query': fields.String(required=True, description='The query text')
})

# Set URL model
url_model = api.model('UrlModel', {
    'database_url': fields.String(required=True, description='The URL to process')
})

# Set Patient Persona model
patient_persona_model = api.model('PatientPersonaModel', {
    'name': fields.String(required=True, description='Patient name'),
    'data': fields.Raw(required=True, description='Patient data')
})

# API for user query
@api.route('/query')
class UserQuery(Resource):
    @api.expect(query_model)
    def post(self):
        data = request.json
        patient_idx = data.get('patient_id')
        user_query_text = data.get('query', '')

        if patient_idx is None or user_query_text == '':
            return {'message': 'Both patient_id and query are required'}, 400
        
        subqueries = generate_subqueries(patient_idx, user_query_text)
        responses = []
        for subquery in subqueries:
            response = generate_response_for_subquery(subquery)
            evaluation = evaluate_response(response)
            responses.append({'subquery': subquery, 'response': response, 'evaluation': evaluation})

        return {'message': responses}, 200

# API for processing URL
@api.route('/process-url')
class UrlProcessor(Resource):
    @api.expect(url_model)
    def post(self):
        data = request.json
        url = data.get('database_url')

        if url is None or url == '':
            return {'message': 'URL is required'}, 400

        # Here you would perform operations with the URL
        try:
            output_file = process_cleveland_clinic_page(url)
            return {'message': 'Successfully processed page.'}, 200
        except Exception as e:
            return {'message': 'Error processing page: ' + str(e)}, 500

# API for saving patient persona
'''
@api.route('/save-patient-persona')
class SavePatientPersona(Resource):
    @api.expect(patient_persona_model)
    def post(self):
        data = request.json
        name = data.get('name')
        patient_data = data.get('data')

        if not name or not patient_data:
            return {'message': 'Name and patient data are required'}, 400

        persona_folder = '../patient_persona'

        if not os.path.exists(persona_folder):
            os.makedirs(persona_folder)

        files = os.listdir(persona_folder)
        n = len(files) + 1  
        file_name = f'patient_{n}.txt'
        file_path = os.path.join(persona_folder, file_name)

        with open(file_path, 'w') as file:
            json.dump({'name': name, 'data': patient_data}, file, indent=2)

        return {'message': 'Patient persona saved successfully!', 'file_path': file_path}, 200
'''
# API for saving patient persona
@api.route('/save-patient-persona')
class SavePatientPersona(Resource):
    @api.expect(patient_persona_model)
    def post(self):
        data = request.json
        name = data.get('name')
        patient_data = data.get('data')

        if not name or not patient_data:
            return {'message': 'Name and patient data are required'}, 400

        persona_folder = '../patient_persona'

        if not os.path.exists(persona_folder):
            os.makedirs(persona_folder)

        files = os.listdir(persona_folder)
        n = len(files) + 1  
        file_name = f'patient_{n}.txt'
        file_path = os.path.join(persona_folder, file_name)

        # 生成所需的格式化字符串
        content = f"1. Basic Demographics:\n"
        content += f"- Age: {patient_data['demographics'].get('age', 'N/A')}\n"
        content += f"- Sex: {patient_data['demographics'].get('sex', 'N/A')}\n"
        content += f"- Weight: {patient_data['demographics'].get('weight', 'N/A')}\n"
        content += f"- Height: {patient_data['demographics'].get('height', 'N/A')}\n"
        content += f"- Ethnicity: {patient_data['demographics'].get('ethnicity', 'N/A')}\n"
        content += f"- Occupation: {patient_data['demographics'].get('occupation', 'N/A')}\n\n"

        content += f"2. Medical History:\n"
        content += f"- Chronic conditions: {patient_data['medicalHistory'].get('chronicConditions', 'N/A')}\n"
        content += f"- Previous surgeries: {patient_data['medicalHistory'].get('previousSurgeries', 'N/A')}\n"
        content += f"- Hospitalizations: {patient_data['medicalHistory'].get('hospitalizations', 'N/A')}\n"
        content += f"- Injuries: {patient_data['medicalHistory'].get('injuries', 'N/A')}\n"
        content += f"- Allergies: {patient_data['medicalHistory'].get('allergies', 'N/A')}\n"
        content += f"- Mental health conditions: {patient_data['medicalHistory'].get('mentalHealthConditions', 'N/A')}\n\n"

        content += f"3. Medication Details:\n"
        content += f"- Current medications: {patient_data['medications'].get('current', 'N/A')}\n"
        content += f"- Dosages and frequency: {patient_data['medications'].get('dosages', 'N/A')}\n"
        content += f"- Past medications: {patient_data['medications'].get('past', 'N/A')}\n"
        content += f"- Drug interactions or known sensitivities: {patient_data['medications'].get('interactions', 'N/A')}\n\n"

        content += f"4. Lifestyle Factors:\n"
        content += f"- Dietary habits: {patient_data['lifestyle'].get('diet', 'N/A')}\n"
        content += f"- Exercise routine: {patient_data['lifestyle'].get('exercise', 'N/A')}\n"
        content += f"- Sleep patterns: {patient_data['lifestyle'].get('sleep', 'N/A')}\n"
        content += f"- Alcohol use: {patient_data['lifestyle'].get('alcohol', 'N/A')}\n"
        content += f"- Tobacco use: {patient_data['lifestyle'].get('tobacco', 'N/A')}\n"
        content += f"- Recreational drug use: {patient_data['lifestyle'].get('drugs', 'N/A')}\n\n"

        content += f"5. Family Medical History:\n"
        content += f"- Genetic conditions: {patient_data['familyHistory'].get('genetic', 'N/A')}\n"
        content += f"- Family history of chronic illnesses: {patient_data['familyHistory'].get('chronic', 'N/A')}\n\n"

        content += f"6. Immunization Status:\n"
        content += f"- Vaccination history: {patient_data['immunization'].get('history', 'N/A')}\n"
        content += f"- Recent vaccinations: {patient_data['immunization'].get('recent', 'N/A')}\n"
        content += f"- Travel history and vaccines related to travel: {patient_data['immunization'].get('travel', 'N/A')}\n\n"

        content += f"7. Symptoms/Presenting Concerns:\n"
        content += f"- Primary complaint: {patient_data['symptoms'].get('primary', 'N/A')}\n"
        content += f"- Duration of symptoms: {patient_data['symptoms'].get('duration', 'N/A')}\n"
        content += f"- Severity of symptoms: {patient_data['symptoms'].get('severity', 'N/A')}\n"
        content += f"- Associated symptoms: {patient_data['symptoms'].get('associated', 'N/A')}\n"
        content += f"- Pain level: {patient_data['symptoms'].get('painLevel', 'N/A')}\n\n"

        content += f"8. Vital Signs:\n"
        content += f"- Blood pressure: {patient_data['vitals'].get('bloodPressure', 'N/A')}\n"
        content += f"- Heart rate: {patient_data['vitals'].get('heartRate', 'N/A')}\n"
        content += f"- Body temperature: {patient_data['vitals'].get('temperature', 'N/A')}\n"
        content += f"- Respiratory rate: {patient_data['vitals'].get('respiratoryRate', 'N/A')}\n\n"

        content += f"9. Test Results:\n"
        content += f"- Recent blood tests: {patient_data['testResults'].get('blood', 'N/A')}\n"
        content += f"- Imaging results: {patient_data['testResults'].get('imaging', 'N/A')}\n"
        content += f"- Urine/stool analysis: {patient_data['testResults'].get('urineStool', 'N/A')}\n"
        content += f"- Other diagnostic results: {patient_data['testResults'].get('other', 'N/A')}\n\n"

        content += f"10. Allergies/Sensitivities:\n"
        content += f"- Food allergies: {patient_data['allergiesSensitivities'].get('food', 'N/A')}\n"
        content += f"- Environmental allergens: {patient_data['allergiesSensitivities'].get('environmental', 'N/A')}\n"
        content += f"- Drug allergies: {patient_data['allergiesSensitivities'].get('drug', 'N/A')}\n\n"

        content += f"11. Reproductive Health (if relevant):\n"
        content += f"- Pregnancy status: {patient_data['reproductive'].get('pregnancy', 'N/A')}\n"
        content += f"- Menstrual cycle details: {patient_data['reproductive'].get('menstrual', 'N/A')}\n"
        content += f"- Contraception use: {patient_data['reproductive'].get('contraception', 'N/A')}\n"
        content += f"- Fertility concerns: {patient_data['reproductive'].get('fertility', 'N/A')}\n\n"

        content += f"12. Mental and Cognitive Health:\n"
        content += f"- Mood changes: {patient_data['mentalHealth'].get('mood', 'N/A')}\n"
        content += f"- Memory issues: {patient_data['mentalHealth'].get('memory', 'N/A')}\n"
        content += f"- Cognitive impairments: {patient_data['mentalHealth'].get('cognitive', 'N/A')}\n"
        content += f"- Stress and anxiety levels: {patient_data['mentalHealth'].get('stress', 'N/A')}\n\n"

        content += f"13. Social and Environmental Factors:\n"
        content += f"- Living conditions: {patient_data['social'].get('living', 'N/A')}\n"
        content += f"- Work environment: {patient_data['social'].get('work', 'N/A')}\n"
        content += f"- Pets: {patient_data['social'].get('pets', 'N/A')}\n\n"

        content += f"14. Insurance and Healthcare Preferences:\n"
        content += f"- Insurance status: {patient_data['insurance'].get('status', 'N/A')}\n"
        content += f"- Preferred healthcare facilities: {patient_data['insurance'].get('facilities', 'N/A')}\n"
        content += f"- Past interactions with healthcare systems: {patient_data['insurance'].get('interactions', 'N/A')}\n"

        # 将格式化的内容写入文件
        with open(file_path, 'w') as file:
            file.write(content)

        return {'message': 'Patient persona saved successfully!', 'file_path': file_path}, 200
if __name__ == '__main__':
    app.run(debug=True)
