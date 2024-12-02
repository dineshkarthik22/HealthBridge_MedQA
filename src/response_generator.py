from chatgpt_client import ChatGPTClient
from query_decomposer import decompose_user_query
from query_server import similarity_search


SYSTEM_PROMPT = """
You are a helpful medical assistant that provides accurate and informative responses to medical questions.
You will be provided a question and some relevant context, and you will answer that question. It is your choice whether to use the context or not.
You will also be provided a source for each context chunk, and if you use the context, you will cite the source for each line from context in your response.

Give your answer in the format below:
Answer: <answer>
Sources: <sources>

Finally, you have to make a decision about the patient. Do not recommend going to the doctor, as the patient already knows. If the patient's fears are irrational, then provide some nice words that can help the patient to calm down. If there could be something serious, list down a comprehensive set of measurements (i.e. lab work) you will need to further diagnose the patient.
Only recommend a doctor visit if you believe the patient's life is in danger.
"""


client = ChatGPTClient()
client.set_system_prompt(SYSTEM_PROMPT)

evaluation_client = ChatGPTClient()
evaluation_prompt = """
You are an expert evaluator of AI-generated medical responses. Your task is to evaluate the given response based on the following criteria: correctness, precision, readability, comprehensiveness, and consistency. Provide a score for each criterion on a scale from 1 to 5, along with a brief explanation for each score.

Response: <response>

Evaluation:
- Correctness: <score> - <explanation>
- Precision: <score> - <explanation>
- Readability: <score> - <explanation>
- Comprehensiveness: <score> - <explanation>
- Consistency: <score> - <explanation>
"""

def evaluate_response(response):
    evaluation_client.set_system_prompt(evaluation_prompt)
    evaluation_query = f"Response: {response}"
    evaluation = evaluation_client.get_response(evaluation_query)
    return evaluation


TOP_K = 8

def generate_subqueries(patient_idx, user_query_text):
    subqueries = decompose_user_query(patient_idx, user_query_text)
    return subqueries


def get_retrieved_context(subquery):
    retrieved_contexts = similarity_search(subquery, TOP_K)
    return retrieved_contexts


def construct_query(subquery, contexts):
    query = f"Question: {subquery}\n\n"
    for context in contexts:
        query += f"Possible helpful information: {context['text']}\n"
        query += f"Source: {context['source_url']}\n\n\n"
    return query


def generate_response_for_subquery(subquery):
    retrieved_contexts = get_retrieved_context(subquery)
    query = construct_query(subquery, retrieved_contexts)
    response = client.get_response(query)
    return response


def main():
    patient_idx = 1
    user_query_text = """
    Can I take paracetamol?
    """
    subqueries = generate_subqueries(patient_idx, user_query_text)
    for subquery in subqueries:
        response = generate_response_for_subquery(subquery)
        evaluation = evaluate_response(response)
        print("Subquery:", subquery)
        print(response)
        # print("Evaluation:")
        print(evaluation)
        print("\n\n\n")
    

if __name__ == "__main__":
    main()
