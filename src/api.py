from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from flask_cors import CORS  # import CORS
from response_generator import generate_response_for_subquery, generate_subqueries
app = Flask(__name__)
CORS(app)  #use CORS
api = Api(app, version='1.0', title='Patient Query API',
          description='A simple API to handle patient queries')

# set query model
query_model = api.model('QueryModel', {
    'patient_id': fields.Integer(required=True, description='The ID of the patient'),
    'query': fields.String(required=True, description='The query text')
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
            responses.append({'subquery': subquery, 'response': response})
    

        #responses = "succeed"  # sample
        return {'message': responses}, 200

if __name__ == '__main__':
    app.run(debug=True)