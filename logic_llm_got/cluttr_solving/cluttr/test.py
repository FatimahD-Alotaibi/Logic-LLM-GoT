import json

output = """
Output:
{{
    "Sentence 1": "Journeying westward, she admired the art in Italy and sipped coffee in France. ",
    "Sentence 2": "The music of Spain and the history of Greece deepened her love for Europe. ",
    "Sentence 3": "The Nordic beauty of Norway, Sweden, Finland, and Denmark took her breath away.",
    "Sentence 4": "She danced in Ireland, explored castles in Scotland, and marveled at the architecture in Germany and Russia.",
    "Sentence 5": "Italy, Norway, Sweden and Germany will always stay her favourite destinations to visit.",
}}
"""

def strip_answer_json(text: str) -> str:
    """
    Helper function to retrieve a text from a json string.

    :param text: Input json string.
    :type text: str
    :return: Retrieved text.
    :rtype: str
    """

    text = text.strip()
    if "Output:" in text:
        text = text[text.index("Output:") + len("Output:") :].strip()
    # find the last "{" and "}" and only keep the text in between including the brackets
    start = text.rfind("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        return "{}"
    text = text[start : end + 1]
    try:
        json.loads(text)
        return text
    except:
        return "{}"
    
answer = strip_answer_json(output)
print(answer)