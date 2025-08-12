## Format the output response for experience and skills API
import re

def format_openai_response(response_text,categories):
    sections =  re.split(r"\n(?:\d+\.\s|\-\s)",response_text)
    formatted_response = {"data": []}
    
    current_category = None
    for section in sections:
        found_category = None
        for category in categories:
            if category in section:
                found_category = category
                current_category={
                    "header": found_category,
                    "suggestions": []
                }
                formatted_response['data'].append(current_category)
                break
        if found_category is None and current_category:
            suggestions = re.split(r'\n', section)
            current_category["suggestions"].extend(suggestions)
    
    return formatted_response