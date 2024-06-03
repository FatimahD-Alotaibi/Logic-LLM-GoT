from typing import Dict, List
from prompts import reasoning_prompt_io, reasoning_prompt_cot, got_split_prompt, apply_rules_prompt, resolution_refutation_score_prompt, aggregate_prompt, reasoning_prompt_got
from graph_of_thoughts import prompter

class LogicalReasoningPrompter(prompter.Prompter):
    """
    SymbolicReasoningPrompter provides the generation of prompts specific to the
    Symbolic FOLIO example for the language models.

    Inherits from the Prompter class and implements its abstract methods.
    """

    reasoning_prompt=reasoning_prompt_io # The prompt needed for the IO method
    reasoning_prompt_cot=reasoning_prompt_cot # The prompt needed for the Cot and ToT methods
    got_split_prompt=got_split_prompt # The prompt needed to split the initial facts
    apply_rules_prompt=apply_rules_prompt # The prompt needed to generate inferred facts based on the initial fact and a set of rules
    resolution_refutation_score_prompt=resolution_refutation_score_prompt # The prompt need to conduct resolution refutation
    aggregate_prompt=aggregate_prompt # The prompt needed to perform aggregation on the inferred facts
    reasoning_got_prompt=reasoning_prompt_got # The prompt need for the GoT method

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

        assert len(state_dicts) <= 2, "Expected 2 states for aggregationn prompt."
        if len(state_dicts) == 0:
            state_dicts = [{"inferred_facts": ""}, {"inferred_facts": ""}]
        elif len(state_dicts) == 1:
            state_dicts.append({"inferred_facts": ""})
        return self.aggregate_prompt.format(
            input1=state_dicts[0]["inferred_facts"], input2=state_dicts[1]["inferred_facts"]
        )

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
            if (current is None or current == "") and kwargs["phase"] == 0:
                return self.got_split_prompt.format(raw_logic_programs=raw_logic_programs)
            
            elif (current is None or current == "") and kwargs["phase"] == 1:
                return self.apply_rules_prompt.format(initial_fact=kwargs["sub_text"], rules=kwargs["rules"])
            
            elif (current is None or current == "") and kwargs["phase"] == 2:
                return self.reasoning_got_prompt.format(context=context, question=question, options=options, raw_logic_programs=raw_logic_programs, aggregated_facts=kwargs["aggregated_facts"])
        
        
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

        key_to_check = "aggregated_fact"

        if len(state_dicts) > 1:
            assert False, "Not implemented yet."
        else:
            # perform individual scoring
            if key_to_check not in state_dicts[0]:
                prompt = self.resolution_refutation_score_prompt.format(facts=state_dicts[0]["inferred_facts"], rules=state_dicts[0]["rules"])
                return prompt
            else:
                prompt = self.resolution_refutation_score_prompt.format(facts=state_dicts[0]["aggregated_fact"], rules=state_dicts[0]["rules"])
                return prompt