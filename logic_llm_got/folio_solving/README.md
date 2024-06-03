# Deductive Reasoning

## The purpose of this directory is to test the capabilites of a LLM's deductive reasoning using serveral methods. The dataset i use will be FOLIO

The use case in this directory gives an answer response to a Logical Reasoning Problem from the FOLIO dataset. To further improve logical reasoning, the problem contex is converted to symbolic logic.
We provide implementations of four different approaches:

- IO
- Chain-of-Thought (ToT)
- Tree of Thought (ToT)
- Graph of Thoughts (GoT)

## Data

We provide an input file with 204 samples. Choose either `logic_programs/FOLIO_dev_gpt-3.5-turbo.json` or `logic_programs/FOLIO_dev_gpt-4.json`.

## Execution

The file to execute the use case is called
`folio_solver.py`. In the main body, one can
select the specific samples to be run (variable samples) and the
approaches (variable approaches). It is also possible to set a budget in
dollars (variable budget).

The Python scripts will create the directory `result`, if it is not
already present. In the `result` directory, another directory is created
for each run: `{name of LLM}_{list of approaches}_{day}_{start time}`.
Inside each execution specific directory two files (`config.json`,
`log.log`) and a separate directory for each selected approach are
created. `config.json` contains the configuration of the run: input data,
selected approaches, name of the LLM, and the budget. `log.log` contains
the prompts and responses of the LLM as well as additional debug data.
The approach directories contain a separate json file for every sample
and the file contains the Graph Reasoning State (GRS) for that sample.

## The Prompter and Parser Classes

**Prompter:**

- The prompter is responsible for preparing the messages or prompts that are sent to the language model (LLM)
- The prompt is expected to contain an encoding of the graph structure, representing the relationships between the different "thoughts" or reasoning steps
- The prompter ensures effective communication between the GoT framework and the LLM.

**Parser:**

- The parser extracts the relevant information from the LLM's responses, such as the generated thoughts and their relationships, and updates the graph structure accordingly
- The parser is responsible for interpreting the LLM's output and mapping it back to the graph representation used by the GoT framework.
- The parser enables the GoT framework to understand and reason about the LLM's thought process, which is represented as a graph.
