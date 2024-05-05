from typing import Dict, List
from graph_of_thoughts import prompter

class SymbolicReasoningPrompter(prompter.Prompter):
    """
    SymbolicReasoningPrompter provides the generation of prompts specific to the
    Symbolic FOLIO example for the language models.

    Inherits from the Prompter class and implements its abstract methods.
    """

    reasoning_prompt = """<Instruction>
Given a problem statement as contexts, the task is to answer a logical reasoning question.
</Instruction>

<Example>
    Context:
    If people perform in school talent shows often, then they attend and are very engaged with school events. People either perform in school talent shows often or are inactive and disinterested members of their community. If people chaperone high school dances, then they are not students who attend the school. All people who are inactive and disinterested members of their community chaperone high school dances. All young children and teenagers who wish to further their academic careers and educational opportunities are students who attend the school. Bonnie either both attends and is very engaged with school events and is a student who attends the school, or she neither attends and is very engaged with school events nor is a student who attends the school.",
    Question: Based on the above information, is the following statement true, false, or uncertain? Bonnie performs in school talent shows often.

    Predicates:\nPerform(x) ::: x performs in school talent shows often.\nAttend(x) ::: x attends school events.\nEngaged(x) ::: x is very engaged with school events.\nInactive(x) ::: x is an inactive and disinterested member of their community.\nChaperone(x) ::: x chaperones high school dances.\nStudent(x) ::: x is a student who attends the school.\nChild(x) ::: x is a young child.\nTeenager(x) ::: x is a teenager.\nWish(x) ::: x wishes to further their academic careers and educational opportunities.\nPremises:\n∀x (Perform(x) → (Attend(x) ∧ Engaged(x))) ::: If people perform in school talent shows often, then they attend and are very engaged with school events.\n∀x (Perform(x) ⊕ Inactive(x)) ::: People either perform in school talent shows often or are inactive and disinterested members of their community.\n∀x (Chaperone(x) → ¬Student(x)) ::: If people chaperone high school dances, then they are not students who attend the school.\n∀x (Inactive(x) → Chaperone(x)) ::: All people who are inactive and disinterested members of their community chaperone high school dances.\n∀x ((Child(x) ∨ Teenager(x)) ∧ Wish(x) → Student(x)) ::: All young children and teenagers who wish to further their academic careers and educational opportunities are students who attend the school.\n(Attend(bonnie) ∧ Engaged(bonnie) ∧ Student(bonnie)) ⊕ ¬(Attend(bonnie) ∨ Engaged(bonnie) ∨ Student(bonnie)) ::: Bonnie either both attends and is very engaged with school events and is a student who attends the school, or she neither attends and is very engaged with school events nor is a student who attends the school.\nConclusion:\n¬Perform(bonnie) ::: Bonnie performs in school talent shows often.

    Options:
    A) True
    B) False
    C) Uncertain

    The correct option is: C
</Example>
-----
Context:
[[Context]]

Predictates: [[Predicates]]

Options:
[[Options]]

The correct option is:
"""

    got_split_prompt = """<Instruction>
Split the following context into individual stentences. Output each sentence in the following format without any additional text or thoughts:
{{
    Sentence 1: Some sentence text...
    Sentence 2: Some sentence text...
    Sentence 3: Some sentence text...
    ...
}}
</Instruction>

<Example>
Problem:
All people who regularly drink coffee are dependent on caffeine. People either regularly drink coffee or joke about being addicted to caffeine. No one who jokes about being addicted to caffeine is unaware that caffeine is a drug. Rina is either a student and unaware that caffeine is a drug, or neither a student nor unaware that caffeine is a drug. If Rina is not a person dependent on caffeine and a student, then Rina is either a person dependent on caffeine and a student, or neither a person dependent on caffeine nor a student.

Output:
{{
    Sentence 1: All People who regulary drink coffee are dependent on caffeine.
    Sentence 2: People either regularly drink coffee or joke about beign addicted to caffeine.
    Sentence 3: No one who jokes about being addicted to caffeine is unaware that caffeine is a drug.
    Sentence 4: Rina is either a student and unaware that caffeine is a drug, or neither a student nor unaware that caffeine is a drug.
    Sentence 5: If Rina is not a person dependent on caffeine and a student, then Rina is either a person dependent on caffeine and a student, or neither a person dependent on caffeine nor a student.
}}
</Example>
-----
Problem:
[[Problem]]

Output:
"""

    def generate_prompt(self, num_branches: int, original: str, current: str, method:str, **kwargs) -> str:
        """
        Generate a generate prompt for the language model.

        :param num_branches: The number of responses the prompt should ask the LM to generate.
        :type num_branches: int
        :param original: Input text.
        :type original: str
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
        if current is None or current == "":
            input = original
        else:
            input = current
        
        self.got_split_prompt.format(input=input)
        
        if kwargs["phase"] == 1:
            return self.reasoning_prompt.format(input=kwargs["sub_text"])
        
        if (
            "sub_text" in kwargs
            and kwargs["sub_text"] != ""
            and len(kwargs["sub_text"]) < len(original) * 0.75
        ):
            original = kwargs["sub_text"]
            
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
        """
        pass