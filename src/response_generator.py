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
"""


client = ChatGPTClient()
client.set_system_prompt(SYSTEM_PROMPT)

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
    I did exercise and I am now facing chest pain. It is towards the middle of my chest. I also do not feel like eating anything, and feel nauseated if I eat.
    I do not know what is happening to me, and I feel scared.
    """
    subqueries = generate_subqueries(patient_idx, user_query_text)
    for subquery in subqueries:
        response = generate_response_for_subquery(subquery)
        print("Subquery:", subquery)
        print(response)
        print("\n\n\n")
    

if __name__ == "__main__":
    main()

