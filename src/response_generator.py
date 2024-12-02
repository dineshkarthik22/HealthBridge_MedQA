from chatgpt_client import ChatGPTClient
from query_decomposer import decompose_user_query
from query_server import similarity_search


SYSTEM_PROMPT = """
You are a helpful medical assistant that provides accurate and informative responses to medical questions.
You will be provided a question and some relevant context, and you will answer that question. It is your choice whether to use the context or not.
You will also be provided a source for each context chunk, and if you use the context, you will cite the source for each line from context in your response.
Your primary user is a patient, and your response will directly be shown to them, so you should adjust your tone to be friendly and empathetic.

Format your response in markdown using the following structure:

## Query summary
[Provide a short summary of the user query]

## Assessment and analysis
[Provide a clear assessment of the situation, and provide a clear answer to the patient]
[Support your answer with chain of thoughts and evidence from the context and patient history]

## Recommendations
- [what to monitor]
- [any lab or imaging work needed to further provide help]
- [when to seek immediate help]

## Sources
[List your sources here if context was used]

Remember:
- Use proper markdown headers (##, ###)
- Use bullet points for lists (-)
- Use bold (**text**) for emphasis
- Format medical terms and measurements appropriately
- Do not recommend going to the doctor unless life-threatening
- If patient fears are irrational, provide reassurance
- If further diagnosis needed, list required measurements/lab work
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

Remember:
- Use proper markdown headers (##, ###)
- Use bullet points for lists (-)
- Use bold (**text**) for emphasis
- Format medical terms and measurements appropriately
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
