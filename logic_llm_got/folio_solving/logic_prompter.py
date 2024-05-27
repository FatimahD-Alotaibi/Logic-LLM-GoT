from typing import Dict, List
from prompts import reasoning_prompt, reasoning_prompt_cot, improve_response_prompt, symbolic_logic_prompt, aggregate_FOL_prompt, forward_chaining_FOL_prompt
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
    aggregate_FOL_prompt=aggregate_FOL_prompt
    forward_chaining_FOL_prompt=forward_chaining_FOL_prompt

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

        prompt = self.aggregate_FOL_prompt.format(input=state_dicts[0]["context"], question=state_dicts[0]["question"], options=state_dicts[0]["options"], raw_logic_programs=state_dicts[0]["raw_logic_programs"])
        
        return prompt
    
    def forward_chaining_prompt(self, state_dicts: List[Dict], **kwargs) -> str:
        """
        Generate a forward chaining prompt for the language model.

        :param state_dicts: The thought states.
        :type state_dicts: List[Dict]
        :param kwargs: Additional keyword arguments.
        :return: The forward chaining prompt.
        :rtype: str
        """
        prompt = self.forward_chaining_FOL_prompt.format(input=state_dicts[0]["context"], question=state_dicts[0]["question"], options=state_dicts[0]["options"], raw_logic_programs=state_dicts[0]["raw_logic_programs"])
        
        return prompt

    def generate_prompt(self, num_branches: int, context: str, question: str, options: str, current: str, raw_logic_programs: str, method:str, **kwargs) -> str:
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
            return self.reasoning_prompt.format(input=context, question=question, options=options, raw_logic_programs=raw_logic_programs)
        elif method.startswith("cot"):
            return self.reasoning_prompt_cot.format(input=context, question=question, options=options, raw_logic_programs=raw_logic_programs)
        elif method.startswith("tot"):
            return self.reasoning_prompt_cot.format(input=context, question=question, options=options, raw_logic_programs=raw_logic_programs)
        elif method.startswith("got"):
            return self.symbolic_logic_prompt.format(input=context, question=question, options=options, raw_logic_programs=raw_logic_programs)
        
        
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