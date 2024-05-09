from typing import Dict

def answer_score(state: Dict) -> float:
    """
    Funtion to assign a float that serves as a score.

    :param state: Tought state to be scored.
    :type state: Dict
    :return: Score
    :rtype: float
    """
    try: 
        predicted_answer = state["current"] # The answer given by the LLM
        correct_answer = state["ground_truth"] # the actual answer
        if predicted_answer == correct_answer:
            return float(1.0) # Like most multiple choice problems, the grade point for answering correctly is 1
        elif predicted_answer != correct_answer:
            return float(0.0)
    except:
        return float(0.0)


def test_response(state: str) -> bool:
    """
    Function to test whether the final solution matches ground truth.

    :param state: Thought state that represents the final solution.
    :type state: str
    :return: Returns whether the solution matches the ground truth.
    :rtype: bool
    """

    try:
        ground_truth = state["ground_truth"] # The actual answer
        predicted_response = state["current"] # The answer given by the LLM
        # Check if values are the same
        if ground_truth != predicted_response:
            return False
        return True
    except:
        return False