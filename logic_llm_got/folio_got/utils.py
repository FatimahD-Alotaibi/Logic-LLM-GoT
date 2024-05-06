def test_response(state: str) -> bool:
    """
    Function to test whether the final solution matches ground truth.

    :param state: Thought state that represents the final solution.
    :type state: str
    :return: Returns whether the solution matches the ground truth.
    :rtype: bool
    """

    try:
        ground_truth = state["ground_truth"]
        predicted_response = state["current"]
        # Check if values are the same
        if ground_truth != predicted_response:
            return False
        return True
    except:
        return False