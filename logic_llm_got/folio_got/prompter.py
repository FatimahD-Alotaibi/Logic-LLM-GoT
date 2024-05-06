from typing import Dict, List
from graph_of_thoughts import prompter

class SymbolicReasoningPrompter(prompter.Prompter):
    """
    SymbolicReasoningPrompter provides the generation of prompts specific to the
    Symbolic FOLIO example for the language models.

    Inherits from the Prompter class and implements its abstract methods.
    """

    reasoning_prompt = """<Instruction>
Given a problem statement as contexts, the task is to answer a logical reasoning question. Output only the letter corresponding to the chosen option. 
</Instruction>

<Example>
Context: If people perform in school talent shows often, then they attend and are very engaged with school events. People either perform in school talent shows often or are inactive and disinterested members of their community. If people chaperone high school dances, then they are not students who attend the school. All people who are inactive and disinterested members of their community chaperone high school dances. All young children and teenagers who wish to further their academic careers and educational opportunities are students who attend the school. Bonnie either both attends and is very engaged with school events and is a student who attends the school, or she neither attends and is very engaged with school events nor is a student who attends the school.",
Question: Based on the above information, is the following statement true, false, or uncertain? Bonnie performs in school talent shows often.

Predicates:\nPerform(x) ::: x performs in school talent shows often.\nAttend(x) ::: x attends school events.\nEngaged(x) ::: x is very engaged with school events.\nInactive(x) ::: x is an inactive and disinterested member of their community.\nChaperone(x) ::: x chaperones high school dances.\nStudent(x) ::: x is a student who attends the school.\nChild(x) ::: x is a young child.\nTeenager(x) ::: x is a teenager.\nWish(x) ::: x wishes to further their academic careers and educational opportunities.\nPremises:\n∀x (Perform(x) → (Attend(x) ∧ Engaged(x))) ::: If people perform in school talent shows often, then they attend and are very engaged with school events.\n∀x (Perform(x) ⊕ Inactive(x)) ::: People either perform in school talent shows often or are inactive and disinterested members of their community.\n∀x (Chaperone(x) → ¬Student(x)) ::: If people chaperone high school dances, then they are not students who attend the school.\n∀x (Inactive(x) → Chaperone(x)) ::: All people who are inactive and disinterested members of their community chaperone high school dances.\n∀x ((Child(x) ∨ Teenager(x)) ∧ Wish(x) → Student(x)) ::: All young children and teenagers who wish to further their academic careers and educational opportunities are students who attend the school.\n(Attend(bonnie) ∧ Engaged(bonnie) ∧ Student(bonnie)) ⊕ ¬(Attend(bonnie) ∨ Engaged(bonnie) ∨ Student(bonnie)) ::: Bonnie either both attends and is very engaged with school events and is a student who attends the school, or she neither attends and is very engaged with school events nor is a student who attends the school.\nConclusion:\n¬Perform(bonnie) ::: Bonnie performs in school talent shows often.

Options:
A) True
B) False
C) Uncertain

Output: C
</Example>

Context: {context}
Question: {question}

{raw_logic_programs}

Options:
{option_1}
{option_2}
{option_3}

Output:
"""

    reasoning_prompt_cot = """<Instruction>
Given a problem statement as contexts, the task is to answer a logical reasoning question. Carefully read the context and question, then select the best option to answer. Utilize logical predicates to bolster the reasoning for reaching the conclusion. Construct a logical statement to aid in deducing the appropriate answer option. 
</Instruction>

<Approach>
To accuratly aswer the question follow these steps:
1. Split the contex passage into four paragraphs of similar length.
2. Interate through each paragraph and look for key words that aid in addressing the question.
3. Utilize the provided predicates to systematically analyze the premises and derive a logical conclusion.
4. Formulate a logical statement explaining how you arrived at that conclusion.
</Approach>

<Example>
Context: If people perform in school talent shows often, then they attend and are very engaged with school events. People either perform in school talent shows often or are inactive and disinterested members of their community. If people chaperone high school dances, then they are not students who attend the school. All people who are inactive and disinterested members of their community chaperone high school dances. All young children and teenagers who wish to further their academic careers and educational opportunities are students who attend the school. Bonnie either both attends and is very engaged with school events and is a student who attends the school, or she neither attends and is very engaged with school events nor is a student who attends the school.
Paragraphs:
{
    "Paragraph 1": "If people perform in school talent shows often, then they attend and are very engaged with school events. People either perform in school talent shows often or are inactive and disinterested members of their community.",
    "Paragraph 2": "If people chaperone high school dances, then they are not students who attend the school. All people who are inactive and disinterested members of their community chaperone high school dances.",
    "Paragrpah 3": "All young children and teenagers who wish to further their academic careers and educational opportunities are students who attend the school.",
    "Paragraph 4": "Bonnie either both attends and is very engaged with school events and is a student who attends the school, or she neither attends and is very engaged with school events nor is a student who attends the school."
}

Question: Based on the above information, is the following statement true, false, or uncertain? Bonnie performs in school talent shows often.

Predicates:\nPerform(x) ::: x performs in school talent shows often.\nAttend(x) ::: x attends school events.\nEngaged(x) ::: x is very engaged with school events.\nInactive(x) ::: x is an inactive and disinterested member of their community.\nChaperone(x) ::: x chaperones high school dances.\nStudent(x) ::: x is a student who attends the school.\nChild(x) ::: x is a young child.\nTeenager(x) ::: x is a teenager.\nWish(x) ::: x wishes to further their academic careers and educational opportunities.\nPremises:\n∀x (Perform(x) → (Attend(x) ∧ Engaged(x))) ::: If people perform in school talent shows often, then they attend and are very engaged with school events.\n∀x (Perform(x) ⊕ Inactive(x)) ::: People either perform in school talent shows often or are inactive and disinterested members of their community.\n∀x (Chaperone(x) → ¬Student(x)) ::: If people chaperone high school dances, then they are not students who attend the school.\n∀x (Inactive(x) → Chaperone(x)) ::: All people who are inactive and disinterested members of their community chaperone high school dances.\n∀x ((Child(x) ∨ Teenager(x)) ∧ Wish(x) → Student(x)) ::: All young children and teenagers who wish to further their academic careers and educational opportunities are students who attend the school.\n(Attend(bonnie) ∧ Engaged(bonnie) ∧ Student(bonnie)) ⊕ ¬(Attend(bonnie) ∨ Engaged(bonnie) ∨ Student(bonnie)) ::: Bonnie either both attends and is very engaged with school events and is a student who attends the school, or she neither attends and is very engaged with school events nor is a student who attends the school.\nConclusion:\n¬Perform(bonnie) ::: Bonnie performs in school talent shows often.

Options:
A) True
B) False
C) Uncertain

Reasoning:

Output: C
</Example>

Context: {context}
Question: {question}

{raw_logic_programs}

Options:
{option_1}
{option_2}
{option_3}

Reasoning:

Output: 
"""

    reasoning_prompt_sentence = """<Instruction>
Given a problem statement as contexts, the task is to answer a logical reasoning question. Carefully read the context and question, then select the best option to answer. Utilize logical predicates to bolster the reasoning for reaching the conclusion. 
</Instruction>

<Approach>
To count the frequency for each country follow these steps:
1. Read the question carefully.
2. Iterate through the context and look for key words that aid in addressing the question.
3. Utilize the provided predicates to systematically analyze the premises and derive a logical conclusion.
</Approach>

<Example>
Context: If people perform in school talent shows often, then they attend and are very engaged with school events. People either perform in school talent shows often or are inactive and disinterested members of their community. If people chaperone high school dances, then they are not students who attend the school. All people who are inactive and disinterested members of their community chaperone high school dances. All young children and teenagers who wish to further their academic careers and educational opportunities are students who attend the school. Bonnie either both attends and is very engaged with school events and is a student who attends the school, or she neither attends and is very engaged with school events nor is a student who attends the school.",
Question: Based on the above information, is the following statement true, false, or uncertain? Bonnie performs in school talent shows often.

Predicates:\nPerform(x) ::: x performs in school talent shows often.\nAttend(x) ::: x attends school events.\nEngaged(x) ::: x is very engaged with school events.\nInactive(x) ::: x is an inactive and disinterested member of their community.\nChaperone(x) ::: x chaperones high school dances.\nStudent(x) ::: x is a student who attends the school.\nChild(x) ::: x is a young child.\nTeenager(x) ::: x is a teenager.\nWish(x) ::: x wishes to further their academic careers and educational opportunities.\nPremises:\n∀x (Perform(x) → (Attend(x) ∧ Engaged(x))) ::: If people perform in school talent shows often, then they attend and are very engaged with school events.\n∀x (Perform(x) ⊕ Inactive(x)) ::: People either perform in school talent shows often or are inactive and disinterested members of their community.\n∀x (Chaperone(x) → ¬Student(x)) ::: If people chaperone high school dances, then they are not students who attend the school.\n∀x (Inactive(x) → Chaperone(x)) ::: All people who are inactive and disinterested members of their community chaperone high school dances.\n∀x ((Child(x) ∨ Teenager(x)) ∧ Wish(x) → Student(x)) ::: All young children and teenagers who wish to further their academic careers and educational opportunities are students who attend the school.\n(Attend(bonnie) ∧ Engaged(bonnie) ∧ Student(bonnie)) ⊕ ¬(Attend(bonnie) ∨ Engaged(bonnie) ∨ Student(bonnie)) ::: Bonnie either both attends and is very engaged with school events and is a student who attends the school, or she neither attends and is very engaged with school events nor is a student who attends the school.\nConclusion:\n¬Perform(bonnie) ::: Bonnie performs in school talent shows often.

Options:
A) True
B) False
C) Uncertain

The correct option is: C
</Example>

Context: {context}
Question: {question}

{raw_logic_programs}

Options:
{option_1}
{option_2}
{option_3}

Output:
"""

    tot_improve_prompt = """<Instruction>
The following represents a logical reasoning problem and a response answering the question associated with the context. 
However, the answer provided is incorrect and may not accurately address the question or understand the context. 
To improve the answer, ensure it aligns more closely with the question asked and accurately reflects the context provided.
</Instruction>

<Approach>
To fix the incorrect list of countries follow these steps:
1. Iterate through the context to identify any keywords that aid in addressing the question.
2. Utilize the provided predicates to systematically analyze the premises and derive a logical conclusion.
3. Compare the original answer with the new answer, and update the original answer only if they are different. 
4. Remember: Only output the new answer if it differs from the original answer.
</Approach>

<Examples>
Context: If people perform in school talent shows often, then they attend and are very engaged with school events. People either perform in school talent shows often or are inactive and disinterested members of their community. If people chaperone high school dances, then they are not students who attend the school. All people who are inactive and disinterested members of their community chaperone high school dances. All young children and teenagers who wish to further their academic careers and educational opportunities are students who attend the school. Bonnie either both attends and is very engaged with school events and is a student who attends the school, or she neither attends and is very engaged with school events nor is a student who attends the school.
Question: Based on the above information, is the following statement true, false, or uncertain? Bonnie performs in school talent shows often.

Predicates:\nPerform(x) ::: x performs in school talent shows often.\nAttend(x) ::: x attends school events.\nEngaged(x) ::: x is very engaged with school events.\nInactive(x) ::: x is an inactive and disinterested member of their community.\nChaperone(x) ::: x chaperones high school dances.\nStudent(x) ::: x is a student who attends the school.\nChild(x) ::: x is a young child.\nTeenager(x) ::: x is a teenager.\nWish(x) ::: x wishes to further their academic careers and educational opportunities.\nPremises:\n∀x (Perform(x) → (Attend(x) ∧ Engaged(x))) ::: If people perform in school talent shows often, then they attend and are very engaged with school events.\n∀x (Perform(x) ⊕ Inactive(x)) ::: People either perform in school talent shows often or are inactive and disinterested members of their community.\n∀x (Chaperone(x) → ¬Student(x)) ::: If people chaperone high school dances, then they are not students who attend the school.\n∀x (Inactive(x) → Chaperone(x)) ::: All people who are inactive and disinterested members of their community chaperone high school dances.\n∀x ((Child(x) ∨ Teenager(x)) ∧ Wish(x) → Student(x)) ::: All young children and teenagers who wish to further their academic careers and educational opportunities are students who attend the school.\n(Attend(bonnie) ∧ Engaged(bonnie) ∧ Student(bonnie)) ⊕ ¬(Attend(bonnie) ∨ Engaged(bonnie) ∨ Student(bonnie)) ::: Bonnie either both attends and is very engaged with school events and is a student who attends the school, or she neither attends and is very engaged with school events nor is a student who attends the school.\nConclusion:\n¬Perform(bonnie) ::: Bonnie performs in school talent shows often.

Options:
A) True
B) False
C) Uncertain

Incorrect Response: A

Reason: Options A and B are incorrect because the premises do not provide direct evidence about Bonnie's participation in school talent shows. Option A assumes Bonnie performs often based on her engagement with school events, but this is not explicitly stated. Option B assumes she does not perform often, but this isn't confirmed either. Option C is correct because without explicit information about Bonnie's participation in talent shows, we cannot determine its truth value.

Output: C

-----

Context: If people perform in school talent shows often, then they attend and are very engaged with school events. People either perform in school talent shows often or are inactive and disinterested members of their community. If people chaperone high school dances, then they are not students who attend the school. All people who are inactive and disinterested members of their community chaperone high school dances. All young children and teenagers who wish to further their academic careers and educational opportunities are students who attend the school. Bonnie either both attends and is very engaged with school events and is a student who attends the school, or she neither attends and is very engaged with school events nor is a student who attends the school.
Question: Based on the above information, is the following statement true, false, or uncertain? If Bonnie is either both a young child or teenager who wishes to further her academic career and educational opportunities and chaperones high school dances or neither is a young child nor teenager who wishes to further her academic career and educational opportunities, then Bonnie is either a student who attends the school or is an inactive and disinterested member of the community. 

Predicates:\nPerform(x) ::: x performs in school talent shows often.\nAttend(x) ::: x attends and is very engaged with school events.\nInactive(x) ::: x is an inactive and disinterested member of their community.\nChaperone(x) ::: x chaperones high school dances.\nStudent(x) ::: x is a student who attends the school.\nYoung(x) ::: x is a young child or teenager who wishes to further their academic career and educational opportunities.\nPremises:\n∀x (Perform(x) → Attend(x)) ::: If people perform in school talent shows often, then they attend and are very engaged with school events.\n∀x (Perform(x) ⊕ Inactive(x)) ::: People either perform in school talent shows often or are inactive and disinterested members of their community.\n∀x (Chaperone(x) → ¬Student(x)) ::: If people chaperone high school dances, then they are not students who attend the school.\n∀x (Inactive(x) → Chaperone(x)) ::: All people who are inactive and disinterested members of their community chaperone high school dances.\n∀x (Young(x) → Student(x)) ::: All young children and teenagers who wish to further their academic careers and educational opportunities are students who attend the school.\n(Attend(bonnie) ∧ Student(bonnie)) ⊕ ¬(Attend(bonnie) ∨ Student(bonnie)) ::: Bonnie either both attends and is very engaged with school events and is a student who attends the school, or she neither attends and is very engaged with school events nor is a student who attends the school.\nConclusion:\n((Young(bonnie) ∧ Chaperone(bonnie)) ⊕ ¬(Young(bonnie) ∨ Chaperone(bonnie))) → (Student(bonnie) ⊕ Inactive(bonnie)) ::: If Bonnie is either both a young child or teenager who wishes to further her academic career and educational opportunities and chaperones high school dances or neither is a young child nor teenager who wishes to further her academic career and educational opportunities, then Bonnie is either a student who attends the school or is an inactive and disinterested member of the community.

Options:
A) True
B) False
C) Uncertain

Incorrect Response: B

Reason: Option B is incorrect because the negation of the statement doesn't lead to a definite conclusion, contradicting the given information. Option C is incorrect because the logical reasoning provides sufficient grounds for a definite conclusion, making it either True or False, eliminating the possibility of uncertainty. Option A is correct because the logical reasoning supports the statement's validity, leading to a definite conclusion based on the given information.

Output: A
</Examples>

Context: {context}
Question: {question}

{raw_logic_programs}

Options:
{option_1}
{option_2}
{option_3}

Incorrect response: {incorrect_response}
"""

    got_split_prompt = """<Instruction>
Split the following context paragraph into 4 paragraphs of approximately same length.
Only output the final 4 paragraphs in the following format without any additional text or thoughts:
{
    "Paragraph 1": "Some paragraph text...",
    "Paragraph 2": "Some paragraph text...",
    "Paragrpah 3": "Some paragraph text...",
    "Paragraph 4": "Some paragraph text..."
}
</Instuction>

<Example>
Context: All video applications are software. All YouTube-related applications are video applications. An APP is either related to YouTube or Instagram. All Instagram is entertainment. All software is programmed. All entertainments are interesting. If something is interesting, then it is good. TikTok is not good.

Output:
{
    "Paragraph 1": "All video applications are software. All YouTube-related applications are video applications.",
    "Paragraph 2": "An APP is either related to YouTube or Instagram. All Instagram is entertainment."
    "Paragraph 3": "All software is programmed. All entertainments are interesting."
    "Paragraph 4": "If something is interesting, then it is good. TikTok is not good."
}
</Example>

Context: {context}
"""

    got_split_prompt2 = """<Instruction>
Split the following context paragraph into 8 paragraphs of approximately same length.
Only output the final 8 paragraphs in the following format without any additional text or thoughts:
{
    "Paragraph 1": "Some paragraph text...",
    "Paragraph 2": "Some paragraph text...",
    "Paragrpah 3": "Some paragraph text...",
    "Paragraph 4": "Some paragraph text...",
    "Paragraph 5": "Some paragraph text...",
    "Paragraph 6": "Some paragraph text...",
    "Paragrpah 7": "Some paragraph text...",
    "Paragraph 8": "Some paragraph text..."
    
}
</Instuction>

<Example>
Context: All video applications are software. All YouTube-related applications are video applications. An APP is either related to YouTube or Instagram. All Instagram is entertainment. All software is programmed. All entertainments are interesting. If something is interesting, then it is good. TikTok is not good.

Output:
{
    "Paragraph 1": "All video applications are software.",
    "Paragraph 2": "All YouTube-related applications are video applications.",
    "Paragraph 3": "An APP is either related to YouTube or Instagram.",
    "Paragraph 4": "All Instagram is entertainment.",
    "Paragraph 5": "All software is programmed.", 
    "Paragraph 6": "All entertainments are interesting.",
    "Paragraph 7": "If something is interesting, then it is good.", 
    "Paragraph 8": "TikTok is not good.",
}
</Example>

Context: {context}
"""

    got_split_prompt3 = """<Instruction>
Split the following input text into individual sentences.
Output each sentence in the following format without any additional text or thoughts:
{
    "Sentence 1": "Some sentence text ...",
    "Sentence 2": "Some sentence text ...",
    "Sentence 3": "Some sentence text ...",
    ...
}
</Instruction>

<Example>
Context: The Blake McFall Company Building is a commercial warehouse listed on the National Register of Historic Places. The Blake McFall Company Building was added to the National Register of Historic Places in 1990. The Emmet Building is a five-story building in Portland, Oregon. The Emmet Building was built in 1915. The Emmet Building is another name for the Blake McFall Company Building. John works at the Emmet Building.

Output:
{
    "Sentence 1": "The Blake McFall Company Building is a commercial warehouse listed on the National Register of Historic Places.",
    "Sentence 2": "The Blake McFall Company Building was added to the National Register of Historic Places in 1990.",
    "Sentence 3": "The Emmet Building is a five-story building in Portland, Oregon.",
    "Sentence 4": "The Emmet Building was built in 1915.",
    "Sentence 5": "The Emmet Building is another name for the Blake McFall Company Building.",
    "Sentence 6": "John workds at the Emmet Building.
}
</Example>

Context: {context}
"""

    def generate_prompt(
            self, 
            num_branches: int,
            context: str,
            question: str,
            option_1: str,
            option_2: str,
            option_3: str,
            raw_logic_programs: str,  
            current: str, 
            method:str, 
            **kwargs
        ) -> str:
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
        
        if method.startswith("io"):
            return self.reasoning_prompt.format(
                context=context, 
                question=question, 
                option_1=option_1, 
                option_2=option_2, 
                option_3=option_3, 
                raw_logic_programs=raw_logic_programs
            )
        elif method.startswith("cot"):
            return self.reasoning_prompt_cot.format(
                context=context, 
                question=question, 
                option_1=option_1, 
                option_2=option_2, 
                option_3=option_3, 
                raw_logic_programs=raw_logic_programs
            )
        elif method.startswith("tot"):
            if current is None or current == "":
                return self.reasoning_prompt_cot.format(
                    context=context, 
                    question=question, 
                    option_1=option_1, 
                    option_2=option_2, 
                    option_3=option_3, 
                    raw_logic_programs=raw_logic_programs
                )
            return self.tot_improve_prompt.format(
                context=context,
                question=question,
                option_1=option_1,
                option_2=option_2,
                option_3=option_3,
                raw_logic_programs=raw_logic_programs,
                incorrect_response=current
            )
        elif method.startswith("got"):
            if (current is None or current == "") and kwargs["phase"] == 0:
                return self.got_split_prompt3.format(context=context)
            
            if kwargs["phase"] == 1:
                return self.reasoning_prompt_sentence.format(
                    context=kwargs["sub_text"],
                    question=question,
                    option_1=option_1,
                    option_2=option_2,
                    option_3=option_3,
                    raw_logic_programs=raw_logic_programs
                )
            
            if (
                "sub_tex" in kwargs
                and kwargs["sub_text"] != ""
                and len(kwargs["sub_text"]) < len(context) * 0.75
            ):
                context = kwargs["sub_text"]

            return self.tot_improve_prompt.format(
                context=context,
                question=question,
                option_1=option_1,
                option_2=option_2,
                option_3=option_3,
                raw_logic_programs=raw_logic_programs,
                incorrect_response=current
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