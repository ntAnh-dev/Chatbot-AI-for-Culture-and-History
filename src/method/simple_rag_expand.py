from src.chatbot.chain import simple_rag_chain 
import json

def simple_rag_expand(prompt):
  response = simple_rag_chain.invoke({ "input": prompt })
  json_data = json.loads(response['answer'][8:-4])
  return json_data['answer']