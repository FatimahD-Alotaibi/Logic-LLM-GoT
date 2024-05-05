## Symbolic Reasoning Prompter

The SymbolicReasoningPrompter class provides methods for generating prompts specific to a symbolic reasoning example for language models.

Here's what each method does:

1. generate_prompt(self, num_branches: int, original: str, current: str, method:str, \*\*kwargs) -> str: Generates a prompt for the language model. Depending on the method and phase, it generates different types of prompts. If the phase is 1, it generates a reasoning prompt using the provided subtext. Otherwise, it generates a split prompt or uses the provided input. The generated prompt is returned as a string.
2. validation_prompt(self, \*\*kwargs) -> str: Generates a validation prompt for the language model. This method is currently not implemented (pass statement).
3. score_prompt(self, state_dicts: List[Dict], \*\*kwargs) -> str: Generates a score prompt for the language model. This method is currently not implemented (pass statement).

## Symbolic Reasoning Parser

The SymbolicReasoningParser class provides methods for parsing responses from a language model for different types of prompts, like improve, generate, validation, and score prompts.

Here's a breakdown of what each method does:

1. **init**(self): Initializes the response cache.
2. strip_answer_json(self, text: str) -> str: Helper function to extract text from a JSON string. It removes any text before the "Output:" keyword and returns the JSON text if it's valid, otherwise, it returns an empty JSON object.
3. parse_improve_answer(self, state: Dict, texts: List[str]) -> Dict: Parses the response from the language model for an "improve" prompt. It expects exactly one response text. It strips the JSON answer, updates the current state, and returns the new thought state.
4. parse_generate_answer(self, state: Dict, texts: List[str]) -> List[Dict]: Parses the response from the language model for a "generate" prompt. It can handle multiple response texts. Depending on the state's method, current value, and phase, it updates the state and generates new states.
5. parse_validation_answer(self, state: Dict, texts: List[str]) -> bool: Parses the response from the language model for a "validation" prompt. This method is currently not implemented (pass statement).
6. parse_score_answer(self, states: List[Dict], texts: List[str]) -> List[float]: Parses the response from the language model for a "score" prompt. This method is currently not implemented (pass statement).
