import json

def transform_abduction_dataset(input_filepath, output_filepath):
    # Read the input JSON file
    with open(input_filepath, 'r') as infile:
        data = json.load(infile)
    
    # Initialize the list to hold the transformed data
    transformed_data = []
    
    # Iterate over each scenario in the input data
    for scenario in data:
        context = scenario['context']
        questions = scenario['questions']
        
        # Iterate over each question and transform the data
        for question in questions:
            transformed_data.append({
                "id": question["id"],
                "context": context,
                "text": question["text"],
                "label": question["label"],
                "QCat": question["QCat"]
            })
    
    # Write the transformed data to the output JSON file
    with open(output_filepath, 'w') as outfile:
        json.dump(transformed_data, outfile, indent=2)

# Example usage:
input_filepath = './AbductionPerson/original.json'
output_filepath = './AbductionPerson/dev.json'

transform_abduction_dataset(input_filepath, output_filepath)