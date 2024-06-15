import json
import logging
from typing import Dict, List, Union
from graph_of_thoughts import parser
import re
from statistics import fmean

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

    def extract_rules(self, text: str) -> str:
        match = re.search(r"Rules:\n(.*?)(?:\nQuery:|\Z)", text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return ""
        
    def strip_answer_helper(self, text: str, tag: str = "") -> str:
        """
        Helper function to remove tags from a text.

        :param text: The input text.
        :type text: str
        :param tag: The tag to be stripped. Defaults to "".
        :type tag: str
        :return: The stripped text.
        :rtype: str
        """

        text = text.strip()
        if "Output:" in text:
            text = text[text.index("Output:") + len("Output:") :].strip()
        if tag != "":
            start = text.rfind(f"<{tag}>")
            end = text.rfind(f"</{tag}>")
            if start != -1 and end != -1:
                text = text[start + len(f"<{tag}>") : end].strip()
            elif start != -1:
                logging.warning(
                    f"Only found the start tag <{tag}> in answer: {text}. Returning everything after the tag."
                )
                text = text[start + len(f"<{tag}>") :].strip()
            elif end != -1:
                logging.warning(
                    f"Only found the end tag </{tag}> in answer: {text}. Returning everything before the tag."
                )
                text = text[:end].strip()
            else:
                logging.warning(
                    f"Could not find any tag {tag} in answer: {text}. Returning the full answer."
                )
        return text
        

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
        
    def strip_answer_string(self, text: str) -> str:
        """
        Helper function to retrieve a text an LLM response

        :param text: Input string
        :type text: str
        :return: Retrieved text.
        :rtype: str
        """

        # Strip leading and trailing whitespace
        text = text.strip()

        # Check if "Output:" is in the text and extract the text following it
        if "Output:" in text:
            text = text[text.index("Output:") + len("Output:") :].strip()

        try:
            return text
        except:
            return ""
    
    def strip_aggregated_facts(self, text: str) -> str:
        """
        Helper function to retrieve a text from an LLM response. Specific to retrieving aggregated facts.

        :param text: Input string
        :type text: str
        :return: Retrieved text.
        :rtype: str
        """
        text = text.strip()
        if "New set:" in text:
            text = text[text.index("New set:") + len("New set:") :].strip()
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
        assert len(states) <= 2, "Expected 2 states for aggregation answer."
        if len(states) == 0:
            states = [
                {"inferred_facts": "", "sub_text": ""},
                {"inferred_facts": "", "sub_text": ""},
            ]
        elif len(states) == 1:
            states.append({"inferred_facts": "", "sub_text": ""})
        new_states = []
        for text in texts:
            answer = self.strip_aggregated_facts(text) # strip the response from the LLM
            new_state = states[0].copy()
            new_state["sub_text"] = (
                states[0]["sub_text"] if "sub_text" in states[0] else ""
            ) + (states[1]["sub_text"] if "sub_text" in states[1] else "")
            new_state["aggregated_facts"] = answer
            new_state["aggr1"] = states[0]["inferred_facts"]
            new_state["aggr2"] = states[1]["inferred_facts"]
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
                    # Phase 0: Parse the response assuming it's a JSON string containing initial facts.
                    rules = self.extract_rules(state["raw_logic_programs"][0]) # Parse the rules from the 'raw_logic_programs'
                    answer = self.strip_answer_json(text)
                    json_dict = json.loads(answer)
                    for key, value in json_dict.items():
                        if "Initial Fact" not in key:
                            logging.warning(
                                f"Expected key to contain 'Initial Fact', but found {key}."
                            )
                            continue
                        new_state = state.copy() # copy the state dictionary
                        new_state["current"] = "" 
                        new_state["rules"] = rules
                        new_state["sub_text"] = value # initialize the initial fact
                        new_state["phase"] = 1 # change phase
                        new_state["part"] = key 
                        new_states.append(new_state) # append the state dictionary to the list
                elif (
                    state["method"].startswith("got")
                    and state["current"] == ""
                    and state["phase"] == 1
                ):
                    # Phase 1: Parse the response assuming it's a plain string containing inferred facts.
                    answer = self.strip_answer_string(text)
                    new_state = state.copy()
                    new_state["inferred_facts"] = answer # initialize the inferred facts
                    new_state["phase"] = 2 # change phase
                    new_states.append(new_state) # append the state dictionary to the list
                elif (
                    state["method"].startswith("got")
                    and state["current"] == ""
                    and state["phase"] == 2
                ):
                    # Phase 2: Parse the response assuming it's a plain string containing the reasoning response
                    answer = self.strip_answer_string(text)
                    new_state = state.copy()
                    new_state["current"] = answer # initialize the answer response
                    new_states.append(new_state) # append the state dictionary to the list
                else:
                    # Default case: Parse the response as a plain string and move to phase 3.
                    answer = self.strip_answer_string(text)
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
        assert len(states) == 1, "Only one state is allowed for scoring."
        if len(states) == 1:
            #individual scoring
            consistency_scores = []
            for text in texts:
                answer = self.strip_answer_helper(text, "Consistency")
                res = re.findall(r"\d+\.?\d*", answer)
                if len(res) == 1:
                    consistency_scores.append(float(res[0]))
                elif len(res) > 1:
                    logging.warning(
                        f"Found multiple consistency scores in answer: {text}. Returning the last one."
                    )
                    consistency_scores.append(float(res[-1]))
                else:
                    logging.warning(
                        f"Could not find any consistency score in answer: {text}. Ignore this answer."
                    )
            if len(consistency_scores) == 0:
                logging.warning(
                    f"Could not find any valid score in any answer. Returning 0.0"
                )
                return [0.0]
            mean_consistancy = fmean(consistency_scores)
            return [mean_consistancy]