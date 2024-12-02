from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from flask_cors import CORS  # import CORS
from response_generator import generate_response_for_subquery, generate_subqueries, evaluate_response
import os

app = Flask(__name__)
CORS(app)  #use CORS
api = Api(app, version='1.0', title='Patient Query API',
          description='A simple API to handle patient queries')

# set query model
query_model = api.model('QueryModel', {
    'patient_id': fields.Integer(required=True, description='The ID of the patient'),
    'query': fields.String(required=True, description='The query text')
})

# set persona model
persona_model = api.model('PersonaModel', {
    'name': fields.String(required=True, description='Patient name'),
    'data': fields.Raw(required=True, description='Patient persona data')
})

# api for user query
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
            responses.append({'subquery': subquery, 'response': response, 'evaluation':  evaluation})
    

        #responses = "succeed"  # sample
        return {'message': responses}, 200

# api for patient persona
@api.route('/api/save-persona')
class PatientPersona(Resource):
    @api.expect(persona_model)
    def post(self):
        try:
            data = request.json
            patient_name = data.get('name')
            persona_data = data.get('data')
            
            if not patient_name or not persona_data:
                return {'error': 'Missing required data'}, 400

            # Create the formatted content
            content = []
            content.append("1. Basic Demographics:")
            content.append(f"- Age: {persona_data['demographics']['age']}")
            content.append(f"- Sex: {persona_data['demographics']['sex']}")
            content.append(f"- Weight: {persona_data['demographics']['weight']}")
            content.append(f"- Height: {persona_data['demographics']['height']}")
            content.append(f"- Ethnicity: {persona_data['demographics']['ethnicity']}")
            content.append(f"- Occupation: {persona_data['demographics']['occupation']}")
            content.append("")

            content.append("2. Medical History:")
            content.append(f"- Chronic conditions: {persona_data['medicalHistory']['chronicConditions']}")
            content.append(f"- Previous surgeries: {persona_data['medicalHistory']['previousSurgeries']}")
            content.append(f"- Hospitalizations: {persona_data['medicalHistory']['hospitalizations']}")
            content.append(f"- Injuries: {persona_data['medicalHistory']['injuries']}")
            content.append(f"- Allergies: {persona_data['medicalHistory']['allergies']}")
            content.append(f"- Mental health conditions: {persona_data['medicalHistory']['mentalHealthConditions']}")
            content.append("")

            content.append("3. Medication Details:")
            content.append(f"- Current medications: {persona_data['medications']['current']}")
            content.append(f"- Dosages and frequency: {persona_data['medications']['dosages']}")
            content.append(f"- Past medications: {persona_data['medications']['past']}")
            content.append(f"- Drug interactions or known sensitivities: {persona_data['medications']['interactions']}")
            content.append("")

            content.append("4. Lifestyle Factors:")
            content.append(f"- Dietary habits: {persona_data['lifestyle']['diet']}")
            content.append(f"- Exercise routine: {persona_data['lifestyle']['exercise']}")
            content.append(f"- Sleep patterns: {persona_data['lifestyle']['sleep']}")
            content.append(f"- Alcohol use: {persona_data['lifestyle']['alcohol']}")
            content.append(f"- Tobacco use: {persona_data['lifestyle']['tobacco']}")
            content.append(f"- Recreational drug use: {persona_data['lifestyle']['drugs']}")
            content.append("")

            content.append("5. Family Medical History:")
            content.append(f"- Genetic conditions: {persona_data['familyHistory']['genetic']}")
            content.append(f"- Family history of chronic illnesses: {persona_data['familyHistory']['chronic']}")
            content.append("")

            content.append("6. Immunization Status:")
            content.append(f"- Vaccination history: {persona_data['immunization']['history']}")
            content.append(f"- Recent vaccinations: {persona_data['immunization']['recent']}")
            content.append(f"- Travel history and vaccines related to travel: {persona_data['immunization']['travel']}")
            content.append("")

            content.append("7. Symptoms/Presenting Concerns:")
            content.append(f"- Primary complaint: {persona_data['symptoms']['primary']}")
            content.append(f"- Duration of symptoms: {persona_data['symptoms']['duration']}")
            content.append(f"- Severity of symptoms: {persona_data['symptoms']['severity']}")
            content.append(f"- Associated symptoms: {persona_data['symptoms']['associated']}")
            content.append(f"- Pain level: {persona_data['symptoms']['painLevel']}")
            content.append("")

            content.append("8. Vital Signs:")
            content.append(f"- Blood pressure: {persona_data['vitals']['bloodPressure']}")
            content.append(f"- Heart rate: {persona_data['vitals']['heartRate']}")
            content.append(f"- Body temperature: {persona_data['vitals']['temperature']}")
            content.append(f"- Respiratory rate: {persona_data['vitals']['respiratoryRate']}")
            content.append("")

            content.append("9. Test Results:")
            content.append(f"- Recent blood tests: {persona_data['testResults']['blood']}")
            content.append(f"- Imaging results: {persona_data['testResults']['imaging']}")
            content.append(f"- Urine/stool analysis: {persona_data['testResults']['urineStool']}")
            content.append(f"- Other diagnostic results: {persona_data['testResults']['other']}")
            content.append("")

            content.append("10. Allergies/Sensitivities:")
            content.append(f"- Food allergies: {persona_data['allergiesSensitivities']['food']}")
            content.append(f"- Environmental allergens: {persona_data['allergiesSensitivities']['environmental']}")
            content.append(f"- Drug allergies: {persona_data['allergiesSensitivities']['drug']}")
            content.append("")

            content.append("11. Reproductive Health:")
            content.append(f"- Pregnancy status: {persona_data['reproductive']['pregnancy']}")
            content.append(f"- Menstrual cycle details: {persona_data['reproductive']['menstrual']}")
            content.append(f"- Contraception use: {persona_data['reproductive']['contraception']}")
            content.append(f"- Fertility concerns: {persona_data['reproductive']['fertility']}")
            content.append("")

            content.append("12. Mental and Cognitive Health:")
            content.append(f"- Mood changes: {persona_data['mentalHealth']['mood']}")
            content.append(f"- Memory issues: {persona_data['mentalHealth']['memory']}")
            content.append(f"- Cognitive impairments: {persona_data['mentalHealth']['cognitive']}")
            content.append(f"- Stress and anxiety levels: {persona_data['mentalHealth']['stress']}")
            content.append("")

            content.append("13. Social and Environmental Factors:")
            content.append(f"- Living conditions: {persona_data['social']['living']}")
            content.append(f"- Work environment: {persona_data['social']['work']}")
            content.append(f"- Pets: {persona_data['social']['pets']}")
            content.append("")

            content.append("14. Insurance and Healthcare Preferences:")
            content.append(f"- Insurance status: {persona_data['insurance']['status']}")
            content.append(f"- Preferred healthcare facilities: {persona_data['insurance']['facilities']}")
            content.append(f"- Past interactions with healthcare systems: {persona_data['insurance']['interactions']}")

            # Save to file
            os.makedirs('patient_persona', exist_ok=True)
            file_path = os.path.join('patient_persona', f'patient_{patient_name}.txt')
            
            with open(file_path, 'w') as f:
                f.write('\n'.join(content))
            
            return {'message': 'Patient persona saved successfully', 'file_path': file_path}, 200
            
        except Exception as e:
            return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True)