from src.genimi.llm import llm 

def gemini(question):
  response = llm.invoke(question)
  return response.content