import ollama
import json
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

model = "llama3.1"
question = '''What the IDF did on September 28, 2024?'''
response = ollama.chat(model=model,
                  messages=[{"role":"system", "content":""},
                            {"role":"user", "content":question}])
print(response)

@tool("tool_browser")
def tool_browser(q: str) -> str:
    """Search on DuckDuckGo browser by passing the input `q`"""
    return DuckDuckGoSearchRun().run(q)

# test
print(tool_browser(question))

@tool("final_answer")
def final_answer(text:str) -> str:
    """Returns a natural language response to the user by passing the input `text`.
    You should provide as much context as possible and specify the source of the information.
    """
    return text

prompt = """
You know everything, you must answer every question from the user, you can use the list of tools provided to you.
Your goal is to provide the user with the best possible answer, including key information about the sources and tools used.

Note, when using a tool, you provide the tool name and the arguments to use in JSON format. 
For each call, you MUST ONLY use one tool AND the response format must ALWAYS be in the pattern:
```json
{"name":"", "parameters": {"":}}
```
Remember, do NOT use any tool with the same query more than once.
Remember, if the user doesn't ask a specific question, you MUST use the `final_answer` tool directly.

Every time the user asks a question, you take note of some keywords in the memory.
Every time you find some information related to the user's question, you take note of some keywords in the memory.

You should aim to collect information from a diverse range of sources before providing the answer to the user. 
Once you have collected plenty of information to answer the user's question use the `final_answer` tool.
"""

dic_tools = {"tool_browser": tool_browser,
             "final_answer":final_answer}

str_tools = "\n".join([str(n+1)+". `"+str(v.name)+"`: "+str(v.description) for n,v in enumerate(dic_tools.values())])
prompt_tools = f"You can use the following tools:\n{str_tools}"
print(prompt_tools)

response = ollama.chat(
    model=model,
    messages=[{"role":"system", "content":prompt+"\n"+prompt_tools},
              {"role":"user", "content":"hello"}
             ], format="json")

print(response)

response = ollama.chat(
    model=model,
    messages=[{"role":"system", "content":prompt+"\n"+prompt_tools},
              {"role":"user", "content":question}
             ], format="json")

print(response["message"]["content"])

tool_input = json.loads(response["message"]["content"])["parameters"]["q"]

context = tool_browser(tool_input)
print("tool output:\n", context)

response = ollama.chat(
    model=model,
    messages=[{"role":"system", "content":"Give the most accurate answer using the folling information:\n"+context},
              {"role":"user", "content":question}
             ])

print("\nllm output:\n", response["message"]["content"])