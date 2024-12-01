from chatgpt_client import ChatGPTClient


QUERY_DECOMPOSER_SYSTEM_PROMPT = """
You are a helpful medical assistant.
You will be provided with the medical history about a patient and a query. The query may be ill-formed and describes the symptoms of a patient.
Your task is to generate multiple smaller decompositions of the query that can be used to provide a response to the patient's symptoms.
Use the information in patient history to augment the subqueries. More relevant information in the subqueries, the better it is.
These decompositions will be used in a RAG setting to get relevant context and each of these queries and the RAG generated response will be shown to the patient.

Give your answer in the format below:
Subquery 1: <subquery>
Subquery 2: <subquery>
Subquery 3: <subquery>
...

You may use as many subqueries as you need.
"""

QUERY_REFORMULATOR_SYSTEM_PROMPT = """
You are a helpful medical assistant.
You will be provided with the medical history about a patient and a query. The query may be ill-formed and describes the symptoms of a patient.
Your task is to generate a reformulated query that can be used to provide a response to the patient's symptoms. 
Use the information in patient history to augment the query. More relevant information in the query, the better it is.
This reformulated query will be used to do a retrieval augmented generation to provide a final response to the patient.

Give your answer in the format below:
Subquery: <query>

You may use one and only one subquery.
"""


client = ChatGPTClient()
client.set_system_prompt(QUERY_REFORMULATOR_SYSTEM_PROMPT)


def get_patient_history(patient_id):
    with open("../patient_persona/patient_{}.txt".format(patient_id), "r") as f:
        patient_history = f.read()

    return patient_history


def construct_user_query(patient_history, query):
    return f"""
        Patient History: {patient_history}
        Question: {query}
    """


def extract_subqueries_from_response(response):
    subqueries = []
    for line in response.split('\n'):
        if line.lower().startswith('subquery'):
            subqueries.append(line.split(':')[1].strip())
    return subqueries


def decompose_user_query(patient_idx, user_query_text):
    patient_history = get_patient_history(patient_idx)
    user_query = construct_user_query(patient_history, user_query_text)

    response = client.get_response(user_query)
    subqueries = extract_subqueries_from_response(response)

    return subqueries


def main():
    """
    Main function that can be used for testing
    """
    user_query_text = """
    I am facing shortness of breath and chest pain. I also have high blood pressure and I feel nauseated. Can I take aspirin?
    """
    subqueries = decompose_user_query(1, user_query_text)
    print(subqueries)


if __name__ == '__main__':
    main()
