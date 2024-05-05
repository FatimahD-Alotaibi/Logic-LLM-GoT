from graph_of_thoughts import operations

def gotx() -> operations.GraphOfOperations:
    """
    Generates the Graph of Operations for the GoTx method, where each sentence
    is considered a different passage.

    :return: Graph of Operations
    :rtype: GraphOfOperations
    """
    # Initialize a new GraphOfOperations object
    operations_graph = operations.GraphOfOperations()

    # Generate a sublist of sentences (sub_texts)
    sub_texts = operations.Generate(1, 1)
    operations_graph.append_operation(sub_texts)  # generate the sublists
    
    # Initialize an empty list to store sub_paragraphs
    sub_paragraphs = []

    # Iterate over each sentence (32 in total)
    for i in range(1, 33):
        # Create a unique paragraph_id for each sentence
        paragraph_id = f"Sentence {i}"
        
        # Select the thoughts (data) corresponding to the current sentence
        sub_text = operations.Selector(
            lambda thoughts, list_id=paragraph_id: [
                thought for thought in thoughts if thought.state["part"] == list_id
            ]
        )
        sub_text.add_predecessor(sub_texts)  # Add dependency on sub_texts
        operations_graph.add_operation(sub_text)  # Add Selector operation
        
        # Generate new text based on the selected sentence
        count_sub_text = operations.Generate(1, 10)
        count_sub_text.add_predecessor(sub_text)  # Add dependency on sub_text
        operations_graph.add_operation(count_sub_text)  # Add Generate operation
        
        # Score the generated text
        score_sub_text = operations.Score(1, False)
        score_sub_text.add_predecessor(count_sub_text)  # Add dependency on count_sub_text
        operations_graph.add_operation(score_sub_text)  # Add Score operation
        
        # Keep the best scored text among the generated ones
        keep_best_sub_text = operations.KeepBestN(1, False)
        keep_best_sub_text.add_predecessor(score_sub_text)  # Add dependency on score_sub_text
        operations_graph.add_operation(keep_best_sub_text)  # Add KeepBestN operation
        
        # Add the KeepBestN operation to the list of sub_paragraphs
        sub_paragraphs.append(keep_best_sub_text)

    # Iterate until only one sub_paragraph remains
    while len(sub_paragraphs) > 1:
        new_sub_paragraphs = []
        # Aggregate sub_paragraphs pairwise
        for i in range(0, len(sub_paragraphs), 2):
            # Aggregate two sub_paragraphs
            aggregate = operations.Aggregate(3)
            aggregate.add_predecessor(sub_paragraphs[i])
            aggregate.add_predecessor(sub_paragraphs[i + 1])
            operations_graph.add_operation(aggregate)  # Add Aggregate operation
            
            # Validate and improve the aggregated text
            val_im_aggregate = operations.ValidateAndImprove(1, True, 3)
            val_im_aggregate.add_predecessor(aggregate)  # Add dependency on aggregate
            operations_graph.add_operation(val_im_aggregate)  # Add ValidateAndImprove operation
            
            # Score the aggregated text
            score_aggregate = operations.Score(1, False)
            score_aggregate.add_predecessor(val_im_aggregate)  # Add dependency on val_im_aggregate
            operations_graph.add_operation(score_aggregate)  # Add Score operation
            
            # Keep the best scored text among the aggregated ones
            keep_best_aggregate = operations.KeepBestN(1, False)
            keep_best_aggregate.add_predecessor(score_aggregate)  # Add dependency on score_aggregate
            operations_graph.add_operation(keep_best_aggregate)  # Add KeepBestN operation
            
            # Add the KeepBestN operation to the list of new_sub_paragraphs
            new_sub_paragraphs.append(keep_best_aggregate)
        sub_paragraphs = new_sub_paragraphs

    # Return the completed Graph of Operations
    return operations_graph