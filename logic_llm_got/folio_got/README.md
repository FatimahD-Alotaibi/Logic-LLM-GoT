# Graph Of Thoughts for Logical Reasoning Problems

## To use the Graph of Thoughts (GoT) method to answer a logical reasoning problem with the given structure, you can follow these steps:

1. **Represent the problem context, question, and options as a graph**
   - Each element (context, question, options) can be a node in the graph.
2. **Apply thought transformations to the graph to reason about the problem**
   - This could involve:
     - Aggregating relevant parts of the context to answer the question
     - Refining the question based on the context
     - Generating arguments for each option based on the question and context
3. **Score each option based on the reasoning process**
   - The score should reflect how well the option answers the question given the context.
4. **Select the option with the highest score as the answer**

   - If multiple options have similar high scores, select "Uncertain".
   - For example, if the problem is:
     Context: "All mammals have fur. Dogs are mammals."
     Question: "Do all dogs have fur?"
     Options: ["A) true, B) false, C) Uncertain"]

     The graph would have nodes for the context, question, and options. Thought transformations could:
     Aggregate the context facts to conclude that since dogs are mammals, and all mammals have fur, dogs must have fur.
     Refine the question to ask if the previous conclusion is always true.
     Generate arguments for each option based on the reasoning.
     Scoring the options would likely give the highest score to "A) true", as the reasoning supports that conclusion. The other options would have lower scores.

## The Prompter and Parser Classes

**Prompter:**

- The prompter is responsible for preparing the messages or prompts that are sent to the language model (LLM)
- The prompt is expected to contain an encoding of the graph structure, representing the relationships between the different "thoughts" or reasoning steps
- The prompter ensures effective communication between the GoT framework and the LLM.

**Parser:**

- The parser extracts the relevant information from the LLM's responses, such as the generated thoughts and their relationships, and updates the graph structure accordingly
- The parser is responsible for interpreting the LLM's output and mapping it back to the graph representation used by the GoT framework.
- The parser enables the GoT framework to understand and reason about the LLM's thought process, which is represented as a graph.
