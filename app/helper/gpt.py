from openai import OpenAI
import os
from flask import jsonify

api_key = "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"
client = OpenAI(api_key=api_key)

def get_chat_completion(prompt):
    
   messages = [{"role": "user", "content": prompt}]
   try:
  
        # Calling the ChatCompletion API
        chat_completion = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    temperature=0.5,
                    top_p=0.5
                )

        # Returning the extracted response
        
        return chat_completion.choices[0].message.content
   
   except Exception as e:
       print(e)
       return jsonify({'error': 'OpenAI API error', 'details': str(e)})