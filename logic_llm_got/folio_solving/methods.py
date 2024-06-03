from graph_of_thoughts import operations

# This is a hack to also allow execution of this file from the examples directory
try:
    from . import utils
except ImportError:
    import utils

"""
The different methods to pass to the GraphOfThoughts Controller Calss
- IO
- Chain-of-Thought (CoT)
- Tree of Thought (ToT)
- Graph of Thoughts (GoT)
"""

def io() -> operations.GraphOfOperations:
    """
    Generates the Graph of Operations for the IO method.

    :return: Graph of Operations
    :rtype: GraphOfOperations
    """

    operations_graph = operations.GraphOfOperations()

    # Append Generate operation with parameters (1, 1) 
    operations_graph.append_operation(operations.Generate(1, 1))
    operations_graph.append_operation(operations.Score(1, False, scoring_function=utils.answer_score))
    operations_graph.append_operation(operations.GroundTruth(utils.test_response))

    return operations_graph

def cot() -> operations.GraphOfOperations:
    """
    Generates the Graph of Operations for the CoT method.

    :return: Graph of Operations
    :rtype: GraphOfOperations
    """
    operations_graph = operations.GraphOfOperations()

    operations_graph.append_operation(operations.Generate(1, 1))
    operations_graph.append_operation(operations.Score(1, False, scoring_function=utils.answer_score))
    operations_graph.append_operation(operations.GroundTruth(utils.test_response))

    return operations_graph

def tot() -> operations.GraphOfOperations:
    """
    Generates the Graph of Operations for the ToT method.
    ToT uses a wider tree, where on each level there are more branches.

    :return: Graph of Operations
    :rtype: GraphOfOperations
    """
    operations_graph = operations.GraphOfOperations()

    branch_factor = 20

    operations_graph.append_operation(operations.Generate(1, branch_factor))
    operations_graph.append_operation(
        operations.Score(1, False, utils.answer_score)
    )
    keep_best_1 = operations.KeepBestN(1, True)
    operations_graph.append_operation(keep_best_1)

    for _ in range(3):
        operations_graph.append_operation(operations.Generate(1, branch_factor))
        operations_graph.append_operation(
            operations.Score(1, False, utils.answer_score)
        )
        keep_best_2 = operations.KeepBestN(1, True) # Keep true because high scores are better
        keep_best_2.add_predecessor(keep_best_1)
        operations_graph.append_operation(keep_best_2)
        keep_best_1 = keep_best_2

    operations_graph.append_operation(operations.KeepBestN(1, True))
    operations_graph.append_operation(operations.GroundTruth(utils.test_response))

    return operations_graph

def got() -> operations.GraphOfOperations:
    """
    Generates the Graph of Operations for the GoT method

    :return: Graph of Operations
    :rtype: GraphOfOperations
    """

    operations_graph = operations.GraphOfOperations()

    sub_texts = operations.Generate(1, 1)
    operations_graph.append_operation(sub_texts) # generate the sub problems
    sub_problems = []
    for i in range(1, 10):
        initial_fact_id = f"Initial Fact {i}"
        sub_text = operations.Selector(
            lambda thoughts, list_id=initial_fact_id: [
                thought for thought in thoughts if thought.state["part"] == list_id
            ]
        )
        sub_text.add_predecessor(sub_texts)
        operations_graph.add_operation(sub_text)
        infer_sub_text = operations.Generate(1, 10)
        infer_sub_text.add_predecessor(sub_text)
        operations_graph.add_operation(infer_sub_text)
        score_sub_text = operations.Score(1, False)
        score_sub_text.add_predecessor(infer_sub_text)
        operations_graph.add_operation(score_sub_text)
        keep_best_sub_text = operations.KeepBestN(1, True)
        keep_best_sub_text.add_predecessor(score_sub_text)
        operations_graph.add_operation(keep_best_sub_text)

        sub_problems.append(keep_best_sub_text)

    while len(sub_problems) > 1:
        new_sub_problems = []
        for i in range(0, len(sub_problems), 2): # Iterrate through the list of sub_problems containing the inferred facts to perform aggregation
            if i + 1 == len(sub_problems):
                new_sub_problems.append(sub_problems[i])
                continue
            aggregate = operations.Aggregate(3)
            aggregate.add_predecessor(sub_problems[i])
            aggregate.add_predecessor(sub_problems[i + 1])
            operations_graph.add_operation(aggregate)
            score_aggregate = operations.Score(1, False) # Score the inferred facts using resolution refutation
            score_aggregate.add_predecessor(aggregate)
            operations_graph.add_operation(score_aggregate)
            keep_best_aggregate = operations.KeepBestN(1, True) # Keep the thought with the highest score
            keep_best_aggregate.add_predecessor(score_aggregate)
            operations_graph.add_operation(keep_best_aggregate)
            new_sub_problems.append(keep_best_aggregate)
        sub_problems = new_sub_problems

        for i in range(0, len(new_sub_problems)):
            generate_answer = operations.Generate(1, 5)
            generate_answer.add_predecessor(new_sub_problems[i])
            operations_graph.add_operation(generate_answer)
            score_answer = operations.Score(1, False, utils.answer_score) # Score the answer response 
            score_answer.add_predecessor(generate_answer)
            operations_graph.add_operation(score_answer)
            keep_best_answer = operations.KeepBestN(1, True) # Keep the thought with the highest score
            keep_best_answer.add_predecessor(score_answer)
            operations_graph.add_operation(keep_best_answer)

            ground_truth_evaluator = operations.GroundTruth(utils.test_response)
            ground_truth_evaluator.add_predecessor(keep_best_answer)
            operations_graph.add_operation(ground_truth_evaluator)

    return operations_graph