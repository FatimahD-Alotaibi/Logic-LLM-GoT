import os
import logging
import datetime
import json
import csv
from collections import Counter
from functools import partial
from typing import Dict, List, Callable, Union
from graph_of_thoughts import controller, language_models, operations, prompter, parser

class LogicalReasoningPrompter(prompter.Prompter):
    """
    FolioPrompter provides the generation of prompts specific to the
    folio example for the language models.

    Inherits from the Prompter class and implements its abstract methods.
    """

    logical_reasoning_prompt = """<Instruction>
Given a problem statement as contexts, the task is to answer a logical reasoning question. 
</Instruction>

<Example>
Context:
All people who regularly drink coffee are dependent on caffeine. People either regularly drink coffee or joke about being addicted to caffeine. No one who jokes about being addicted to caffeine is unaware that caffeine is a drug. Rina is either a student and unaware that caffeine is a drug, or neither a student nor unaware that caffeine is a drug. If Rina is not a person dependent on caffeine and a student, then Rina is either a person dependent on caffeine and a student, or neither a person dependent on caffeine nor a student.

Question: Based on the above information, is the following statement true, false, or uncertain? Rina is a person who jokes about being addicted to caffeine or unaware that caffeine is a drug.

Options:
A) True
B) False
C) Uncertain

The correct option is: A

</Example>
------
Context:
[[CONTEXT]]

Question: [[QUESTION]]

Options:
[[OPTIONS]]

The correct option is:
"""

    logical_reasoning_prompt_cot = """<Instruction>
Given a problem statement as contexts, the task is to answer a logical reasoning question.
</Instruction>

<Example>
Context:
The Green Leaf Café is a popular vegetarian restaurant known for its organic ingredients and sustainable practices. The Green Leaf Café opened its doors in 2010. The Silver Birch Bistro is a cozy eatery situated in the heart of a bustling city. The Silver Birch Bistro has been serving customers since 1995. The Silver Birch Bistro is another name for the Green Leaf Café. Sarah often dines at the Silver Birch Bistro.

Question: Based on the above information, is the following statement true, false, or uncertain? The Green Leaf Café serves meat dishes on its menu.

Options:
A) True
B) False
C) Uncertain

Reasoning:
The Silver Birch Bistro is another name for the Green Leaf Café. Since Sarah often dines at the Silver Birch Bistro, it implies that she frequents the Green Leaf Café. The Green Leaf Café is renowned for its vegetarian offerings and sustainable practices. Therefore, it is highly unlikely that the Green Leaf Café serves meat dishes on its menu.

The correct option is: B

</Example>
"""

    tot_improve_prompt = """<Instruction>
The following presents an original input text and an answer intended to respond to the question within the input text. However, the provided answer is incorrect and may not accurately address the question. Change the answer to one of the options provided so that it accurately answers the question.</Instruction>

<Approach>
To fix the incorrect answer follow these steps:
1. Carefully reevaluate the question and the chosen answer to pinpoint where the mistake might have occurred. Look for any misinterpretations, assumptions, or overlooked details.
2. Go back to the provided context and carefully reread the information given. Pay close attention to any relevant details or clues that might affect your answer.
3. Assess the other answer options and evaluate whether any of them might be more appropriate given the context provided. Look for evidence or reasoning that supports or contradicts each option.
4. Compare the new answer with the response provided in the Incorrect Answer and update the Incorrect Answer if they are different.
</Approach>

<Examples>
Input:

Context: Sophia Adams is a renowned artist who specializes in abstract paintings. She recently held an exhibition at the Tate Modern gallery in London. The Tate Modern is one of the most famous art galleries in the United Kingdom. Sophia Adams studied fine arts at the Sorbonne University in Paris. All graduates of the Sorbonne University are proficient in French.

Question: Based on the above information, is the following statement true, false, or uncertain? Sophia Adams speaks fluent French.

Options:
A) True
B) False
C) Uncertain

Incorrect Answer: {B}

Reason: Option B is incorrect because there is no direct evidence or information provided in the context that explicitly states that Sophia Adams does not speak fluent French. The information provided only mentions that she studied fine arts at the Sorbonne University in Paris, where all graduates are proficient in French. Since there is no contradictory information or indication that she does not speak French, it is uncertain whether Sophia Adams speaks fluent French. Therefore, the correct answer is "Uncertain" (Option C).

Output: {C}
----
Input:

Context: Emily Johnson is a scientist who conducts research in marine biology. She completed her undergraduate studies at Stanford University, which is located in California. Stanford University is renowned for its programs in environmental science. Emily Johnson is currently conducting research on coral reef ecosystems in Australia.

Question: Based on the above information, is the following statement true, false, or uncertain? Emily Johnson received her undergraduate degree from a university known for its programs in marine biology.

Options:
A) True
B) False
C) Uncertain

Incorrect Answer: {A}

Reason: The answer is B (False) because the context specifically states that Emily Johnson completed her undergraduate studies at Stanford University, which is renowned for its programs in environmental science, not marine biology. While Stanford University may offer courses and research opportunities related to marine biology, the context does not explicitly mention that it is known specifically for its programs in marine biology. Therefore, it would be inaccurate to conclude that Emily Johnson received her undergraduate degree from a university known for its programs in marine biology (Option A). Additionally, since the context provides clear information about the university and its reputation in environmental science, there is no uncertainty regarding this fact, making Option C (Uncertain) incorrect. Therefore, the correct answer is indeed B (False).

Output: {B}
</Examples>

Input: 
{input}
Incorrect Answer: 
{incorrect_answer}
"""
    sentence_improve_prompt = """"""

    generate_logical_reasoning = """<Instruction>
Given a problem statement as contexts, the task is to answer a logical reasoning question. Based on the provided context, generate a reasoned response to the following logical reasoning question. Only output the reasoning response.
</Instruction>

<Example>
Context:
The Blake McFall Company Building is a commercial warehouse listed on the National Register of Historic Places. The Blake McFall Company Building was added to the National Register of Historic Places in 1990. The Emmet Building is a five-story building in Portland, Oregon. The Emmet Building was built in 1915. The Emmet Building is another name for the Blake McFall Company Building. John works at the Emmet Building.

Question: Based on the above information, is the following statement true, false, or uncertain? The Blake McFall Company Building is located in Portland, Oregon.

Options:
A) True
B) False
C) Uncertain

Reasoning:
The Blake McFall Company Building is another name for the Emmet Building. The Emmet Building is located in Portland, Oregon. Therefore, the Blake McFall Company Building is located in Portland, Oregon.

</Example>

Context:
[[CONTEXT]]

Question: [[QUESTION]]

Options:
[[OPTIONS]]

Reasoning:
"""

    generate_improved_reasoning = """<Instruction>
Given a problem statement as contexts, the task is to answer a logical reasoning question. The reasoning prompt should be enhanced to facilitate a more effective inferred logical deduction from the context, aiding in selecting the best option to answer the question. Only output the enchanced reasoning response.
</Instruction>

<Example>
Context:
People eat meat regularly or are vegetation. If people eat meat regularly, then they enjoy eating hamburgers and steaks. All people who are vegetarian are conscious of the environment or their health. If people are conscious about the environment or their health, then they do not go to fast food places often. If people have busy schedules without time to cook, then they go to fast food places often. If Jeremy does not both go to fast food places often and is conscious about the environment or their health, then he goes to fast food places often.

Question: Based on the above information, is the following statement true, false, or uncertain? If Jeremy has a busy schedule without time to cook, then Jeremy does not enjoy eating hamburgers and steaks.

Options:
A) True
B) False
C) Uncertain

Reasoning:
If Jeremy has a busy schedule without time to cook or enjoy eating hamburgers and steaks, then Jeremy goes to fast food places often. If people are conscious about the environment or their health, then they do not go to fast food places often. This means that Jeremy is not conscious about the environment or his health. All people who are vegetarian are conscious of the environment or their health. Therefore, Jeremy is not vegetarian. People eat meat regularly or are vegetation. Therefore, Jeremy eats meat regularly. If people eat meat regularly, then they enjoy eating hamburgers and steaks. Therefore, Jeremy enjoys eating hamburgers and steaks.
</Example>

<Output>
If Jeremy has a busy schedule without time to cook or enjoy eating hamburgers and steaks, then Jeremy goes to fast food places often. If people are conscious about the environment or their health, then they do not go to fast food places often. This means that Jeremy is not conscious about the environment or his health, which eliminates option C. All people who are vegetarian are conscious of the environment or their health. Therefore, Jeremy is not vegetarian. People eat meat regularly or are vegetarian. Therefore, Jeremy eats meat regularly. If people eat meat regularly, then they enjoy eating hamburgers and steaks. Therefore, Jeremy enjoys eating hamburgers and steaks. Option A is false because if Jeremy has a busy schedule without time to cook, he still enjoys eating hamburgers and steaks, as indicated by the provided logic. Option C is also incorrect because we've deduced that Jeremy is not conscious about the environment or his health, which makes the statement uncertain. The correct option is B because Jeremy does enjoy eating hamburgers and steaks, even if he has a busy schedule without time to cook, as inferred from the logical deductions.
</Output>
"""
    got_split_prompt = ""
    got_split_prompt2 = ""
    got_split_prompt3 = ""

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
        if method.startswith("io"):
            return self.logical_reasoning_prompt.format(input=input)
        elif method.startswith("cot"):
            return self.logical_reasoning_prompt_cot.format(input=input)
        elif method.startswith("tot"):
            if current is None or current == "":
                return self.logical_reasoning_prompt_cot.format(input=input)
            return self.tot_improve_prompt.format(input=original, incorrect_answer=current)
        elif method.startswith("got"):
            if (current is None or current == "") and kwargs["phase"] == 0:
                if method == "got8":
                    return self.got_split_prompt2.format(input=input)
                if method == "gotx":
                    return self.got_split_prompt3.format(input=input)
                return self.got_split_prompt.format(input=input)
            
            if kwargs["phase"] == 1:
                if method == "gotx":
                    return self.count_prompt_sentence.format(input=kwargs["sub_text"])
                return self.count_prompt_cot.format(input=kwargs["sub_text"])

            if (
                "sub_text" in kwargs
                and kwargs["sub_text"] != ""
                and len(kwargs["sub_text"]) < len(original) * 0.75
            ):
                original = kwargs["sub_text"]
            if method == "gotx":
                return self.sentence_improve_prompt.format(
                    input=original, incorrect_dict=current
                )
            return self.tot_improve_prompt.format(
                input=original, incorrect_dict=current
            )
            
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