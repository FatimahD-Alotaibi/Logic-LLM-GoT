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
    operations_graph.append_operation(operations.Score(1, False))
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

    operations_graph.append_operation(operations.Generate(1, 5))
    operations_graph.append_operation(operations.Score(1, False, utils.answer_score))
    keep_best = operations.KeepBestN(1, True) # Keep true because high scores are better
    operations_graph.append_operation(keep_best)
    operations_graph.append_operation(operations.Score(1, False, utils.answer_score))
    keep_best_2 = operations.KeepBestN(1, True)
    keep_best_2.add_predecessor(keep_best)
    operations_graph.append_operation(keep_best_2)
    operations_graph.append_operation(operations.Generate(1, 10))
    operations_graph.append_operation(operations.Score(1, False, utils.answer_score))
    keep_best_3 = operations.KeepBestN(1, True)
    keep_best_3.add_predecessor(keep_best_2)
    operations_graph.append_operation(keep_best_3)


    operations_graph.append_operation(operations.GroundTruth(utils.test_response))

    return operations_graph

def got_fg() -> operations.GraphOfOperations:
    """
    Generates the Graph of Operations for the GoT method with forward chaining

    :return: Graph of Operations
    :rtype: GraphOfOperations
    """

    operations_graph = operations.GraphOfOperations()

    operations_graph.append_operation(operations.Generate(1, 5))
    operations_graph.append_operation(operations.Score(1, False, utils.answer_score))
    keep_best = operations.KeepBestN(1, True) # Keep true because high scores are better
    operations_graph.append_operation(keep_best)
    operations_graph.append_operation(operations.ForwardChaining(5))
    operations_graph.append_operation(operations.Score(1, False, utils.answer_score))
    keep_best_2 = operations.KeepBestN(1, True)
    keep_best_2.add_predecessor(keep_best)
    operations_graph.append_operation(keep_best_2)
    operations_graph.append_operation(operations.Generate(1, 10))
    operations_graph.append_operation(operations.Score(1, False, utils.answer_score))
    keep_best_3 = operations.KeepBestN(1, True)
    keep_best_3.add_predecessor(keep_best_2)
    operations_graph.append_operation(keep_best_3)


    operations_graph.append_operation(operations.GroundTruth(utils.test_response))

    return operations_graph