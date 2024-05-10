from typing import Dict, List
from prompts import reasoning_prompt, reasoning_prompt_cot, improve_response_prompt, symbolic_logic_prompt
from graph_of_thoughts import prompter

class LogicalReasoningPrompter(prompter.Prompter):
    """
    SymbolicReasoningPrompter provides the generation of prompts specific to the
    Symbolic FOLIO example for the language models.

    Inherits from the Prompter class and implements its abstract methods.
    """

    reasoning_prompt=reasoning_prompt
    reasoning_prompt_cot=reasoning_prompt_cot
    improve_response_prompt=improve_response_prompt
    symbolic_logic_prompt=symbolic_logic_prompt

    def aggregation_prompt(self, state_dicts: List[Dict], **kwargs) -> str:
        """
        Generate an aggregation prompt for the language model.

        :param state_dicts: The thought states that should be aggregated.
        :type state_dicts: List[Dict]
        :param kwargs: Additional keyword arguments.
        :return: The aggregation prompt.
        :rtype: str
        :raise AssertionError: If more than two thought states are provided.
        """
        pass

    def generate_prompt(self, num_branches: int, reasoning_problem: str, current: str, raw_logic_programs: str, method:str, **kwargs) -> str:
        """
        Generate a generate prompt for the language model.

        :param num_branches: The number of responses the prompt should ask the LM to generate.
        :type num_branches: int
        :param reasoning_problem: The logical reasoning problem to be solved.
        :type reasoning_problem: str
        :param current: Intermediate solution.
        :type current: str
        :param method: Method for which the generate prompt is generated.
        :type method: str
        :param kwargs: Additional keyword arguments.
        :return: The generate prompt.
        :rtype: str
        :raise AssertionError: If the requested number of branches is not one.
        """
        assert num_branches == 1, "Branchig should be done via multiple requests."

        if method.startswith("io"):
            return self.reasoning_prompt.format(input=reasoning_problem)
        elif method.startswith("cot"):
            return self.reasoning_prompt_cot.format(input=reasoning_problem)
        elif method.startswith("tot"):
            return self.reasoning_prompt_cot.format(input=reasoning_problem)
        elif method.startswith("got"):
            return self.symbolic_logic_prompt.format(input=reasoning_problem, raw_logic_programs=raw_logic_programs)
        
        
    def improve_prompt(self, current: str, aggr1: str, aggr2: str, **kwargs) -> str:
        """
        Generate an improve prompt for the language model.

        :param current: Intermediate solution.
        :type current: str
        :param aggr1: Partially solution 1 before aggregation.
        :type aggr1: str
        :param aggr2: Partially solution 2 before aggregation.
        :type aggr2: str
        :param kwargs: Additional keyword arguments.
        :return: The improve prompt.
        :rtype: str
        """
        pass
            
    def validation_prompt(self, **kwargs) -> str:
        """
        Generate a validation prompt for the language model.

        :param kwargs: Additional keyword arguments.
        :return: The validation prompt.
        :rtype: str
        """
        pass

    def score_prompt(self, state_dicts: List[Dict], **kwargs) -> str:
        """
        Generate a score prompt for the language model.

        :param state_dicts: The thought states that should be scored,
                            if more than one, they should be scored together.
        :type state_dicts: List[Dict]
        :param kwargs: Additional keyword arguments.
        :return: The score prompt.
        :rtype: str
        :raise AssertionError: If more than one thought state is supplied.
        """
        pass