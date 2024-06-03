from typing import Dict, List
from prompts import cluttr_io_prompt, cluttr_cot_prompt, cluttr_fg_prompt, got_split_prompt, apply_rules_prompt
from graph_of_thoughts import prompter

class LogicalReasoningPrompter(prompter.Prompter):
    """
    SymbolicReasoningPrompter provides the generation of prompts specific to the
    Symbolic FOLIO example for the language models.

    Inherits from the Prompter class and implements its abstract methods.
    """

    cluttr_io_prompt=cluttr_io_prompt
    cluttr_cot_prompt=cluttr_cot_prompt
    cluttr_fg_prompt=cluttr_fg_prompt
    got_split_prompt=got_split_prompt
    apply_rules_prompt=apply_rules_prompt

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
    
    def forward_chaining_prompt(self, state_dicts: List[Dict], **kwargs) -> str:
        """
        Generate a forward chaining prompt for the language model.

        :param state_dicts: The thought states.
        :type state_dicts: List[Dict]
        :param kwargs: Additional keyword arguments.
        :return: The forward chaining prompt.
        :rtype: str
        """
        prompt = self.cluttr_fg_prompt.format(body_text=state_dicts[0]["body_text"], program=state_dicts[0]["program"], goal=state_dicts[0]["goal"])
        
        return prompt

    def generate_prompt(self, num_branches: int, body_text: str, program: str, goal: str, current: str, method: str, **kwargs) -> str:
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
            return self.cluttr_io_prompt.format(body_text=body_text, program=program, goal=goal)
        elif method.startswith("cot"):
            return self.cluttr_cot_prompt.format(body_text=body_text, program=program, goal=goal)
        elif method.startswith("got"):
            if (current is None or current == "") and kwargs["phase"] == 0:
                return self.got_split_prompt.format(program=program)
            
            if kwargs["phase"] == 1:
                return self.apply_rules_prompt.format(input=kwargs["sub_text"])
        
        
        
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