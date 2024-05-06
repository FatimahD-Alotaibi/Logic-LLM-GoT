import os
import logging
import datetime
import json
from typing import List, Callable
from graph_of_thoughts import operations, language_models, controller
from methods import io, cot, tot, got # Import the methods

def run(
    data_ids: List[int],
    methods: List[Callable[[], operations.GraphOfOperations]],
    budget: float,
    lm_name: str,
) -> float:
    """
    Controller function that executes each specified method for each specified
    sample while the budget is not exhausted.

    :param data_ids: Indices of the sample to be run.
    :type data_ids: List[int]
    :param methods: List of functions to generate Graphs of Operations.
    :type methods: Each function generates a Graph of Operation.
    :param budget: Language model budget for the execution in dollars.
    :type budget: float
    :param lm_name: Name of the language model to be used.
    :type lm_name: str
    :return: Spent budget in dollars.
    :rtype: float
    """
    # Store the original budget
    orig_budget = budget

    data = []

    # Read the JSON file containing the desired dataset
    with open(os.path.join('./logic_programs/FOLIO_dev_gpt-4.json'), 'r', encoding="utf8") as file:
        raw_data = json.load(file)

    # Iterate and process data into desired format
    for item in raw_data:
        # Construct the desired format
        data.append([
            item['id'],
            item['context'],
            item['question'],
            item['options'][0],
            item['options'][1],
            item['options'][2],
            item['raw_logic_programs'][0],
            item['answer']
        ])

    # If no data_ids provided or it's None, select all data
    if data_ids is None or len(data_ids) == 0:
        data_ids = list(range(len(data)))
    
    # Select the data based on data_ids
    selected_data = [data[i] for i in data_ids]

    # Create a directory to store results
    results_dir = os.path.join(os.path.dirname(__file__), "results")
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    # Create a timestap for the folder name
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    extra_info = f"{lm_name}_{'-'.join([method.__name__ for method in methods])}"
    folder_name = f"{extra_info}_{timestamp}"
    results_folder = os.path.join(results_dir, folder_name)
    os.makedirs(results_folder)

    # Store configuration information
    config = {
        "data": selected_data,
        "methods": [method.__name__ for method in methods],
        "lm": lm_name,
        "budget": budget
    }

    # Write config to a JSON file
    with open(os.path.join(results_folder, "config.json", "w", encoding="utf8")) as f:
        json.dump(config, f)

    # Setup logging
    logging.basicConfig(
        filename=os.path.join(results_folder, "log.log"),
        filemode="w",
        format="%(name)s - %(level)s - %(message)s",
        level=logging.DEBUG
    )

    # Create a results directory for each method
    for method in methods:
        # create a results directory for the method
        os.makedirs(os.path.join(results_folder, method.__name__))

    # Loop through each data sample
    for data in selected_data:
        logging.info(f"Running data {data[0]}: {data[1]}")
        if budget <= 0.0:
            logging.error(
                f"Budget has been depleted, stopping. Data {data[0]} has not been run."
            )
            break
        # Loop through each method
        for method in methods:
            logging.info(f"Running method {method.__name__}")
            logging.info(f"Budget left: {budget}")
            if budget <= 0.0:
                logging.error(
                    f"Budget has been depleted, stopping. Method {method.__name__} has not been run."
                )
                break
            # Initialize language model
            lm = language_models.ChatGPT(
                os.path.join(
                    os.path.dirname(__file__),
                    "../../graph_of_thoughts/language_models/config.json"
                ),
                model_name=lm_name,
                cache=True,
            )
            # Get operations graph using the method
            operations_graph = method()
            # Initialize controller for executing operations
            executor = controller.Controller(
                lm,
                operations_graph,
                {
                    "context": data[1], # The context for the logical reasoning problem
                    "question": data[2], # The question that needs to be answered
                    "option_1": data[3], # Option A) True
                    "option_2": data[4], # Option B) False
                    "option_3": data[5], # Option C) Uncertain
                    "raw_logic_programs": data[6], #The raw logic 
                    "ground_truth": data[7], # The correct response
                    "current": "", # The predicted response
                    "phase": 0,
                    "method": method.__name__
                },
            )
            try:
                # Execute operations
                executor.run()
            except Exception as e:
                logging.error(f"Exception: {e}")
            # Output graph to a JSON file
            path = os.path.join(
                results_folder,
                method.__name__,
                f"{data[0]}.json"
            )
            executor.output_graph(path)
            budget -= lm.cost

    # Return spent budget
    return orig_budget - budget

if __name__ == "__main__":
    """
    Input (x)   : an unordered list of 32 numbers between 0 and 9 (inclusive)
    Output (y)  : a sorted list of 32 numbers between 0 and 9 (inclusive)
    Correct     : y == sorted(x)
    Input Example:
        [0, 1, 9, 4, 2, 2, 0, 5, 1...]
    Output Example:
        [0, 0, 0, 0, 1, 1, 1, 1, 2...]
    """
    budget = 30
    samples = [item for item in range(0, 204)] # Because there are a 204 
    approaches = [got]

    spent = run(samples, approaches, budget, "chatgpt")

    logging.info(f"Spent {spent} out of {budget} budget.")