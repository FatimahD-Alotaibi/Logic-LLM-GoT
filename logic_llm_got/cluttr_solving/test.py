import json

output = """
Output:
{{
    "Initial Fact 1": "isRelationOf(ben, son, alice) ::: [Alice] celebrated her birthday with her son [Ben].",
    "Initial Fact 2": "isRelationOf(chris, brother, alice) ::: [Chris] visited his sister [Alice] and her family.",
    "Initial Fact 3": "isRelationOf(david, cousin, ben) ::: [David] played soccer with his cousin [Ben].",
    "Initial Fact 4": "isRelationOf(david, grandson, eve) ::: [Eve] baked a cake for her grandson [David]."
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
    
    # Replace double braces with single braces
    text = text.replace("{{", "{").replace("}}", "}")
    
    # find the last "{" and "}" and only keep the text in between including the brackets
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        return "{}"
    text = text[start : end + 1]
    
    try:
        json.loads(text)
        return text
    except Exception as e:
        print("JSON parsing error:", e)
        return "{}"

# Call the function with the input string
result = strip_answer_json(output)

# Print the result
print("Final result:", result)