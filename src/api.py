from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from flask_cors import CORS  # import CORS
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
        
        # Simulate URL processing
        try:
            output_file = process_cleveland_clinic_page(url)
            return {'message': 'Successfully processed page.'}, 200
        except Exception as e:
            return {'message': 'Error processing page: '+ str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True)