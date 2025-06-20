from src.chatbot.chain import eng_rag_chain 
import json

def rag_eng_handmade(prompt):
  response = eng_rag_chain.invoke({ "input": prompt })
  json_data = json.loads(response['answer'][8:-4])
  return json_data['answer']