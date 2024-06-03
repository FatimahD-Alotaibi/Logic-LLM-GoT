import json
import logging
from typing import Dict, List, Union
from graph_of_thoughts import parser
import re

class LogicalReasoningParser(parser.Parser):
    """
    SymbolicCountingParser provides the parsing of language model reponses
    specific to the keyword counting example.

    Inherits from the Parser class and implements its abstract methods.
    """

    def __init__(self) -> None:
        """
        Inits the response cache.
        """
        self.cache = {}

    def parse_initial_facts(self, text: str) -> List[str]:
        """
        Parses the "Initial Facts" section from a given text.

        Args:
            text (str): The input text containing sections like "Initial Facts", "Rules", etc.

        Returns:
            List[str]: A list of initial facts extracted from the "Initial Facts" section.
        """
        initial_facts_section = False # Flag to indicate if we are in the "Initial Facts" section
        initial_facts = [] # List to store the parsed initial facts

        # Split the input text by lines and iterate through each line
        for line in text.split('\n'):
            stripped_line = line.strip() # Remove leading and trailing whitespace
            if stripped_line.startswith("Initial Facts:"):
                # Mark the start of the "Initial Facts" section
                initial_facts_section = True
                continue
            if initial_facts_section:
                # If we are in the "Initial Facts" section, check for termination conditions"
                if not stripped_line or stripped_line.startswith("Rules:"):
                    # Stop if an empty line or the start of the next section is encountered
                    break
                # Extract the fact after the numbering and store it in the list
                initial_facts.append(stripped_line.split(". ", 1)[1])

        return initial_facts
    
    def parse_rules(self, text: str) -> List[str]:
        """
        Parses the "Rules" section from a given text.

        Args:
            text (str): The input text containing sections like "Initial Facts", "Rules", etc.

        Returns:
            List[str]: A list of rules extracted from the "Rules" section.
        """
        rules_section = False # Flag to indicate if we are in the "Rules" section
        rules = [] # List to store the parsed rules

        # Split the input text by lines and iterate through each line
        for line in text.split('\n'):
            stripped_line = line.strip() # Remove leading and trailing whitespace
            if stripped_line.startswith("Rules:"):
                # Mark the start of the "Rules" section
                rules_section = True
                continue
            if rules_section:
                # If we are in the "Rules" section, check for termination conditions"
                if not stripped_line or stripped_line.startswith("Inference Process:"):
                    # Stop if an empty line or the start of the next section is encountered
                    break
                # Extract the fact after the numbering and store it in the list
                rules.append(stripped_line.split(". ", 1)[1])

        return rules

    def parse_inference_process(self, text: str) -> List[str]:
        """
        Parses the "Inference Process" section from a given text.

        Args:
            text (str): The input text containing sections like "Initial Facts", "Rules", "Inference Process", etc.

        Returns:
            List[str]: A list of steps extracted from the "Inference Process" section.
        """
        inference_process_section = False  # Flag to indicate if we are in the "Inference Process" section
        inference_process = []  # List to store the parsed inference process steps

        # Split the input text by lines and iterate through each line
        for line in text.split('\n'):
            stripped_line = line.strip()  # Remove leading and trailing whitespace
            if stripped_line.startswith("Inference Process:"):
                # Mark the start of the "Inference Process" section
                inference_process_section = True
                continue
            if inference_process_section:
                # If we are in the "Inference Process" section, check for termination conditions
                if stripped_line.startswith("Answer:"):
                    # Stop if an empty line or the start of the next section is encountered
                    break
                # Extract the step and store it in the list
                inference_process.append(stripped_line)

        return inference_process
    
    def extract_premises_content(self, text: str) -> str:
        match = re.search(r"Premises:\n(.*?)(?:\nConclusion:|\Z)", text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return ""

    def extract_boolean(self, text: str) -> str:
        """
        Helper function designed to extract letter a boolean from the LLM response.

        :param text: The LLM response
        :type text: str
        :return: The letter character
        :rtype: str
        """

        # Define the regular expression pattern to find the boolean value
        pattern = r'Answer:\s*(True|False)'

        # Search for the pattern in the prompt
        match = re.search(pattern, text)

        # If a match is found, return the boolean value as a string
        if match:
            return match.group(1)
        else:
            # If no match is found, return "False" as a string
            return "False"
        

    def strip_answer_json(self, text: str) -> str:
        """
        Helper function to retrieve a text from a json string.

        :param text: Input json string.
        :type text: str
        :return: Retrieved text.
        :rtype: str
        """
        text = text.strip()
        if "Output:" in text:
            text = text[text.index("Output:") + len("Output:") :].strip()
        # find the last "{" and "}" and only keep the text in between including the brackets
        start = text.rfind("{")
        end = text.rfind("}")
        if start == -1 or end == -1:
            return "{}"
        text = text[start : end + 1]
        try:
            json.loads(text)
            return text
        except:
            return "{}"
        
    def strip_applied_rules(self, text: str) -> str:
        """
        Helper function to retrieve a text an LLM response

        :param text: Input string
        :type text: str
        :return: Retrieved text.
        :rtype: str
        """
        text = text.strip()
        if "Output:" in text:
            text = text[text.index("Output:") + len("Output:") :].strip()

        return text
    
    def parse_aggregation_answer(self, states: List[Dict], texts: List[str]) -> Union[Dict, List[Dict]]:
        """
        Parse the response from the language model for an aggregation prompt.

        :param states: The thought states used to generate the prompt.
        :type states: List[Dict]
        :param texts: The responses to the prompt from the language model.
        :type texts: List[str]
        :return: The new thought states after parsing the respones from the language model.
        :rtype: Union[Dict, List[Dict]]
        :raise AssertionError: If more than two thought states are provided.
        """
        pass
    
    def parse_forward_chaining_answer(self, states: List[Dict], texts: List[str]) -> Union[Dict, List[Dict]]:
        """
        """
        new_states = []
        for text in texts:
            facts = self.parse_initial_facts(text)
            rules = self.parse_rules(text)
            inference = self.parse_inference_process(text)
            answer = self.extract_boolean(text)
            new_state = states[0].copy()
            new_state["facts"] = facts
            new_state["rules"] = rules
            new_state["inference"] = inference
            new_state["current"] = answer
            new_states.append(new_state)
        return new_states
    
    def parse_improve_answer(self, state: Dict, texts: List[str]) -> Dict:
        """
        Parse the response from the language model for an improve prompt.

        :param state: The thought state used to generate the prompt.
        :type state: str
        :param texts: The responses to the prompt from the language model.
        :type texts: List[str]
        :return: The new thought state after parsing the responses from the language model.
        :rtype: str
        :raise AssertionError: If there is not exactly one response text.
        """
        pass

    def parse_generate_answer(self, state: Dict, texts: List[str]) -> List[Dict]:
        """
        Parse the response from the language model for a generate prompt.

        :param state: The thought state used to generate the prompt.
        :type state: Dict
        :param texts: The responses to the prompt from the language model.
        :type texts: List[str]
        :return: The new thought states after parsing the respones from the language model.
        :rtype: List[Dict]
        """

        new_states = []
        for text in texts:
            try:
                if (
                    state["method"].startswith("got")
                    and state["current"] == ""
                    and state["phase"] == 0
                ):
                    rules = self.extract_premises_content(state["raw_logic_programs"][0])
                    answer = self.strip_answer_json(text)
                    json_dict = json.loads(answer)
                    for key, value in json_dict.items():
                        if "Initial Fact" not in key:
                            logging.warning(
                                f"Expected key to contain 'Paragraph' or 'Sentence', but found {key}."
                            )
                            continue
                        new_state = state.copy()
                        new_state["current"] = ""
                        new_state["sub_text"] = value
                        new_state["rules"] = rules
                        new_state["phase"] = 1
                        new_state["part"] = key
                        new_states.append(new_state)
                elif (
                    state["method"].startswith("got")
                    and state["current"] == ""
                    and state["phase"] == 1
                ):
                    answer = self.strip_applied_rules(text)
                    new_state = state.copy()
                    new_state["phase"] = 2
                    new_state["rule(s)"] = answer
                    new_states.append(new_state)
                else:
                    answer = self.strip_answer_json(text)
                    new_state = state.copy()
                    new_state["current"] = answer
                    new_state["phase"] = 3
                    new_states.append(new_state)
            except Exception as e:
                logging.error(f"Could not parse step answer: {text}. Error: {e}")
        return new_states

    def parse_validation_answer(self, state: Dict, texts: List[str]) -> bool:
        """
        Parse the response from the language model for a validation prompt.

        :param state: The thought state used to generate the prompt.
        :type state: Dict
        :param texts: The responses to the prompt from the language model.
        :type texts: List[str]
        :return: Whether the thought state is valid or not.
        :rtype: bool
        """
        pass

    def parse_score_answer(self, states: List[Dict], texts: List[str]) -> List[float]:
        """
        Parse the response from the language model for a score prompt.

        :param states: The thought states used to generate the prompt.
        :type states: List[Dict]
        :param texts: The responses to the prompt from the language model.
        :type texts: List[str]
        :return: The scores for the thought states.
        :rtype: List[float]
        :raise AsssertionError: If the number of thought states is not one.
        """
        pass