import os
import logging
import datetime
import json
import csv
from collections import Counter
from functools import partial
from typing import Dict, List, Callable, Union
from graph_of_thoughts import controller, language_models, operations, prompter, parser

class KeywordCountingParser(parser.Parser):
    """
    KeywordCountingParser provides the parsing of language model reponses
    specific to the keyword counting example.

    Inherits from the Parser class and implements its abstract methods.
    """

    def __init__(self) -> None:
        """
        Inits the response cache.
        """
        self.cache = {}

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

    def parse_aggregation_answer(
        self, states: List[Dict], texts: List[str]
    ) -> Union[Dict, List[Dict]]:
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
                {"current": "{}", "sub_text": ""},
                {"current": "{}", "sub_text": ""},
            ]
        elif len(states) == 1:
            states.append({"current": "{}", "sub_text": ""})
        new_states = []
        for text in texts:
            answer = self.strip_answer_json(text)
            new_state = states[0].copy()
            new_state["sub_text"] = (
                states[0]["sub_text"] if "sub_text" in states[0] else ""
            ) + (states[1]["sub_text"] if "sub_text" in states[1] else "")
            new_state["current"] = answer
            new_state["aggr1"] = states[0]["current"]
            new_state["aggr2"] = states[1]["current"]
            new_states.append(new_state)
        return new_states

    def parse_improve_answer(self, state: Dict, texts: List[str]) -> Dict:
        """
        Parse the response from the language model for an improve prompt.

        :param state: The thought state used to generate the prompt.
        :type state: Dict
        :param texts: The responses to the prompt from the language model.
        :type texts: List[str]
        :return: The new thought state after parsing the responses from the language model.
        :rtype: Dict
        :raise AssertionError: If there is not exactly one response text.
        """

        assert len(texts) == 1, "Expected 1 text for improve answer."
        text = texts[0]
        answer = self.strip_answer_json(text)
        new_state = state.copy()
        new_state["current"] = answer
        return new_state

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
                    answer = self.strip_answer_json(text)
                    json_dict = json.loads(answer)
                    if len(json_dict.keys()) != 4 or len(json_dict.keys()) != 8:
                        logging.warning(
                            f"Expected 4 or 8 paragraphs in json, but found {len(json_dict.keys())}."
                        )
                    for key, value in json_dict.items():
                        if "Paragraph" not in key and "Sentence" not in key:
                            logging.warning(
                                f"Expected key to contain 'Paragraph' or 'Sentence', but found {key}."
                            )
                            continue
                        new_state = state.copy()
                        new_state["current"] = ""
                        new_state["sub_text"] = value
                        new_state["phase"] = 1
                        new_state["part"] = key
                        new_states.append(new_state)
                else:
                    answer = self.strip_answer_json(text)
                    new_state = state.copy()
                    new_state["current"] = answer
                    new_state["phase"] = 2
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
        """
        pass