from utils import test_response
from graph_of_thoughts import operations

"""
The different methods to pass to the GraphOfThoughts Controller Calss
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
    operations_graph.append_operation(operations.Score(3, False))

    return operations_graph

def cot() -> operations.GraphOfOperations:
    """
    Generates the Graph of Operations for the CoT method.

    :return: Graph of Operations
    :rtype: GraphOfOperations
    """
    operations_graph = operations.GraphOfOperations()

    operations_graph.append_operation(operations.Score(3, False))

    return operations_graph

def tot() -> operations.GraphOfOperations:
    """
    Generates the Graph of Operations for the ToT method.

    :return: Graph of Operations
    :rtype: GraphOfOperations
    """
    operations_graph = operations.GraphOfOperations()

    branch_factor = 10 # number of branches for ToT

    operations_graph.append_operation(operations.Generate(1, branch_factor))
    operations_graph.append_operation(operations.Score(3, False))
    keep_best_1 = operations.KeepBestN(1, True)
    operations_graph.append_operation(keep_best_1)

    for _ in range(2):
        operations_graph.append_operation(operations.Generate(1, branch_factor))
        operations_graph.append_operation(operations.Score(3, False))
        keep_best_2 = operations.KeepBestN(1, True)
        keep_best_2.add_predecessor(keep_best_1)
        operations_graph.append_operation(keep_best_2)
        keep_best_1 = keep_best_2
    
    return operations_graph

def got() -> operations.GraphOfOperations:
    """
    Generates the Graph of Operations for the GoT method

    :return: Graph of Operations
    :rtype: GraphOfOperations
    """

    operations_graph = operations.GraphOfOperations()

    operations_graph.append_operation(operations.Generate(1, 5))
    operations_graph.append_operation(operations.Score(3, False))
    keep_best = operations.KeepBestN(3, True)
    operations_graph.add_operation(keep_best)
    operations_graph.append_operation(operations.Aggregate(5))
    operations_graph.append_operation(operations.Score(3, False))
    keep_best2 = operations.KeepBestN(1, True)
    keep_best2.add_predecessor(keep_best)
    operations_graph.append_operation(keep_best2)
    operations_graph.append_operation(operations.Generate(1, 10))
    operations_graph.append_operation(operations.Score(3, False))
    keep_best3 = operations.KeepBestN(1, True)
    keep_best3.add_predecessor(keep_best2)
    operations_graph.append_operation(keep_best3)

    operations_graph.append_operation(operations.GroundTruth(test_response))

    return operations_graph