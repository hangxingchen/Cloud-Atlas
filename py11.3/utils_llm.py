# utils_llm.py
# API calls for large language models (LLM)

print('Importing LLM API modules')

import os
import qianfan

def llm_qianfan(PROMPT='Hello, who are you?'):
    """
    Baidu Qianfan Large Language Model API
    """
    
    # Set ACCESS_KEY and SECRET_KEY
    os.environ["QIANFAN_ACCESS_KEY"] = QIANFAN_ACCESS_KEY
    os.environ["QIANFAN_SECRET_KEY"] = QIANFAN_SECRET_KEY
    
    # Choose the language model
    MODEL = "ERNIE-Bot-4"
    # MODEL = "ERNIE Speed"
    # MODEL = "ERNIE-Lite-8K"
    # MODEL = 'ERNIE-Tiny-8K'

    # Initialize the Qianfan ChatCompletion client
    chat_comp = qianfan.ChatCompletion(model=MODEL)
    
    # Send the input prompt to the model
    resp = chat_comp.do(
        messages=[{"role": "user", "content": PROMPT}], 
        top_p=0.8, 
        temperature=0.3, 
        penalty_score=1.0
    )
    
    # Extract and return the model response
    response = resp["result"]
    return response

import openai
from openai import OpenAI
from API_KEY import *

def llm_yi(PROMPT='Hello, who are you?'):
    """
    LingYiWanWu Large Language Model API
    """
    
    API_BASE = "https://api.lingyiwanwu.com/v1"
    API_KEY = YI_KEY

    MODEL = 'yi-large'
    # MODEL = 'yi-medium'
    # MODEL = 'yi-spark'
    
    # Initialize the OpenAI client with API base URL and key
    client = OpenAI(api_key=API_KEY, base_url=API_BASE)
    
    # Send the input prompt to the model
    completion = client.chat.completions.create(
        model=MODEL, 
        messages=[{"role": "user", "content": PROMPT}]
    )
    
    # Extract and return the model response
    result = completion.choices[0].message.content.strip()
    return result
