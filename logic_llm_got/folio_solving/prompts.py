reasoning_prompt = """<Instruction>
Given a problem statement as contexts, the task is to answer a logical reasoning question. Output only the letter corresponding to the chosen option. 
</Instruction>

<Example>
Context: The Blake McFall Company Building is a commercial warehouse listed on the National Register of Historic Places. The Blake McFall Company Building was added to the National Register of Historic Places in 1990. The Emmet Building is a five-story building in Portland, Oregon. The Emmet Building was built in 1915. The Emmet Building is another name for the Blake McFall Company Building. John works at the Emmet Building.

Question: Based on the above information, is the following statement true, false, or uncertain? The Blake McFall Company Building is located in Portland, Oregon.

Options: A) True, B) False, C) Uncertain

Output: A
------
Context: People eat meat regularly or are vegetation. If people eat meat regularly, then they enjoy eating hamburgers and steaks. All people who are vegetarian are conscious of the environment or their health. If people are conscious about the environment or their health, then they do not go to fast food places often. If people have busy schedules without time to cook, then they go to fast food places often. If Jeremy does not both go to fast food places often and is conscious about the environment or their health, then he goes to fast food places often.

Question: Based on the above information, is the following statement true, false, or uncertain? If Jeremy has a busy schedule without time to cook, then Jeremy does not enjoy eating hamburgers and steaks.

Options: A) True, B) False, C) Uncertain

Output: B
</Example>

{input}

{question}

{options}

{raw_logic_programs}

Output: 
"""

reasoning_prompt_cot = """<Instruction>
Given a problem statement as contexts, the task is to answer a logical reasoning question. Output only the letter corresponding to the chosen option.
<Instruction>

<Approach>
To accurately answer the question, follow these steps:
1. Carefully read and understand the given prompt. Identify the main question or problem that needs to be solved.
2. Identify the key concepts or terms mentioned in the prompt. Pay attention to any terms that are defined or explained within the prompt itself.
3. Draw your final conclusions based on the logical deductions you have made. Your conclusions should logically follow from the information provided in the prompt and your chain of thoughts.
</Approach>

<Example>
Context: The Blake McFall Company Building is a commercial warehouse listed on the National Register of Historic Places. The Blake McFall Company Building was added to the National Register of Historic Places in 1990. The Emmet Building is a five-story building in Portland, Oregon. The Emmet Building was built in 1915. The Emmet Building is another name for the Blake McFall Company Building. John works at the Emmet Building.

Question: Based on the above information, is the following statement true, false, or uncertain? The Blake McFall Company Building is located in Portland, Oregon.

Options: A) True, B) False, C) Uncertain

Final Conclusions: The Blake McFall Company Building is another name for the Emmet Building. The Emmet Building is located in Portland, Oregon. Therefore, the Blake McFall Company Building is located in Portland, Oregon.

Output: A
------
Context: People eat meat regularly or are vegetation. If people eat meat regularly, then they enjoy eating hamburgers and steaks. All people who are vegetarian are conscious of the environment or their health. If people are conscious about the environment or their health, then they do not go to fast food places often. If people have busy schedules without time to cook, then they go to fast food places often. If Jeremy does not both go to fast food places often and is conscious about the environment or their health, then he goes to fast food places often.

Question: Based on the above information, is the following statement true, false, or uncertain? If Jeremy has a busy schedule without time to cook, then Jeremy does not enjoy eating hamburgers and steaks.

Options: A) True, B) False, C) Uncertain

Final Conclusions: If Jeremy has a busy schedule without time to cook or enjoy eating hamburgers and steaks, then Jeremy goes to fast food places often. If people are conscious about the environment or their health, then they do not go to fast food places often. This means that Jeremy is not conscious about the environment or his health. All people who are vegetarian are conscious of the environment or their health. Therefore, Jeremy is not vegetarian. People eat meat regularly or are vegetation. Therefore, Jeremy eats meat regularly. If people eat meat regularly, then they enjoy eating hamburgers and steaks. Therefore, Jeremy enjoys eating hamburgers and steaks. 

Output: B
</Example>

{input}

{question}

{options}

{raw_logic_programs}

Output:
"""

symbolic_logic_prompt = """<Instructions>
Given a problem statement as contexts, the task is to answer a logical reasoning question. Output only the letter corresponding to the chosen option.
</Instructions>

<Approach>
1. Read the question carefully. Iterate through the context and look for key words that may address the question being asked. 
2. Split the raw logic programs into the Symbolic logic context. Place the prompt into the following format without any additional text or thoughts.
<Example>
Symbolic logic context:
Predicates:
Predicate_1 ::: predicate_1 statement.
Predicate_2 ::: predicate_2 statement.
...
Premises:
Premise_1 ::: premise_1 statement.
Premise_2 ::: premise_2 statement.
...
Conclusion:
Conclusion ::: conslution_1 statement.
</Example>
3. Utilize the symbolic logic context to derive possible conclusions based on the provided context and question.
4. Use the conlusions drawn out from the Symbolic logic context to choose the option that answers the question.
</Apprach>

<Example>
Context: All people who regularly drink coffee are dependent on caffeine. People either regularly drink coffee or joke about being addicted to caffeine. No one who jokes about being addicted to caffeine is unaware that caffeine is a drug. Rina is either a student and unaware that caffeine is a drug, or neither a student nor unaware that caffeine is a drug. If Rina is not a person dependent on caffeine and a student, then Rina is either a person dependent on caffeine and a student, or neither a person dependent on caffeine nor a student.

Question: Based on the above information, is the following statement true, false, or uncertain? Rina is either a person who jokes about being addicted to caffeine or is unaware that caffeine is a drug.

Options: A) True, B) False, C) Uncertain

Raw logic programs: Predicates:Dependent(x) ::: x is a person dependent on caffeine.\nDrinks(x) ::: x regularly drinks coffee.\nJokes(x) ::: x jokes about being addicted to caffeine.\nUnaware(x) ::: x is unaware that caffeine is a drug.\nStudent(x) ::: x is a student.\nPremises:∀x (Drinks(x) → Dependent(x)) ::: All people who regularly drink coffee are dependent on caffeine.\n∀x (Drinks(x) ⊕ Jokes(x)) ::: People either regularly drink coffee or joke about being addicted to caffeine.\n∀x (Jokes(x) → ¬Unaware(x)) ::: No one who jokes about being addicted to caffeine is unaware that caffeine is a drug.\n(Student(rina) ∧ Unaware(rina)) ⊕ ¬(Student(rina) ∨ Unaware(rina)) ::: Rina is either a student and unaware that caffeine is a drug, or neither a student nor unaware that caffeine is a drug.\n¬(Dependent(rina) ∧ Student(rina)) → (Dependent(rina) ∧ Student(rina)) ⊕ ¬(Dependent(rina) ∨ Student(rina)) ::: If Rina is not a person dependent on caffeine and a student, then Rina is either a person dependent on caffeine and a student, or neither a person dependent on caffeine nor a student.\nConclusion:Jokes(rina) ⊕ Unaware(rina) ::: Rina is either a person who jokes about being addicted to caffeine or is unaware that caffeine is a drug.

Symbolic logic context:
Predicates:
Dependent(x) ::: x is a person dependent on caffeine.
Drinks(x) ::: x regularly drinks coffee.
Jokes(x) ::: x jokes about being addicted to caffeine.
Unaware(x) ::: x is unaware that caffeine is a drug.
Student(x) ::: x is a student.
Premises:
∀x (Drinks(x) → Dependent(x)) ::: All people who regularly drink coffee are dependent on caffeine.
∀x (Drinks(x) ⊕ Jokes(x)) ::: People either regularly drink coffee or joke about being addicted to caffeine.
∀x (Jokes(x) → ¬Unaware(x)) ::: No one who jokes about being addicted to caffeine is unaware that caffeine is a drug. 
(Student(rina) ∧ Unaware(rina)) ⊕ ¬(Student(rina) ∨ Unaware(rina)) ::: Rina is either a student and unaware that caffeine is a drug, or neither a student nor unaware that caffeine is a drug. 
¬(Dependent(rina) ∧ Student(rina)) → (Dependent(rina) ∧ Student(rina)) ⊕ ¬(Dependent(rina) ∨ Student(rina)) ::: If Rina is not a person dependent on caffeine and a student, then Rina is either a person dependent on caffeine and a student, or neither a person dependent on caffeine nor a student.
Conclusion:
Jokes(rina) ⊕ Unaware(rina) ::: Rina is either a person who jokes about being addicted to caffeine or is unaware that caffeine is a drug.

Conclusion analysis: Option C is correct because the statement "Rina is either a person who jokes about being addicted to caffeine or is unaware that caffeine is a drug" cannot be definitively confirmed or refuted based solely on the information provided. The given information outlines several possibilities regarding Rina's characteristics, such as her coffee consumption habits, student status, and awareness of caffeine as a drug. While we can analyze these possibilities and infer potential scenarios, the lack of specific details about Rina's characteristics prevents us from arriving at a conclusive determination. Option A (True) and Option B (False) are incorrect because they assert certainty without adequate evidence. Without additional information about Rina, uncertainty remains the appropriate conclusion, as the statement cannot be decisively affirmed or denied based solely on the provided information. 

Output: C
</Example>

{input}

{question}

{options}

{raw_logic_programs}

Output:
"""

aggregate_FOL_prompt = """<Instructions>
You are given a logical reasoning problem with several premises and a statement to evaluate. Your task is to use aggregation to analyze the given information and determine the truth value of the statement. Output only the letter corresponding to the chosen conclusion.
</Instructions>

<Approach>
1. Identify Key Conditions:
    - List the key conditions provided in the premises and how they relate to the involved subjects.
2. Simplify and Combine Conditions:
    - Simplify each condition and see how they combine with each other. Use logical operators to connect the different premises.
3. Analyze Logical Implications:
    - Determine the logical implications of each premise on the subject. Consider what each premise implies regarding the subject.
4. Evaluate the Conclusion:
    - Use the aggregated information to evaluate the given conclusion. Determine whether it must be true, false, or if it reamins uncertain based on the premises.
</Approach>

<Example>
Context: All people who regularly drink coffee are dependent on caffeine. People either regularly drink coffee or joke about being addicted to caffeine. No one who jokes about being addicted to caffeine is unaware that caffeine is a drug. Rina is either a student and unaware that caffeine is a drug, or neither a student nor unaware that caffeine is a drug. If Rina is not a person dependent on caffeine and a student, then Rina is either a person dependent on caffeine and a student, or neither a person dependent on caffeine nor a student.

Question: Based on the above information, is the following statement true, false, or uncertain? Rina is either a person who jokes about being addicted to caffeine or is unaware that caffeine is a drug.

Options: A) True, B) False, C) Uncertain

Raw logic programs: Predicates:Dependent(x) ::: x is a person dependent on caffeine.\nDrinks(x) ::: x regularly drinks coffee.\nJokes(x) ::: x jokes about being addicted to caffeine.\nUnaware(x) ::: x is unaware that caffeine is a drug.\nStudent(x) ::: x is a student.\nPremises:∀x (Drinks(x) → Dependent(x)) ::: All people who regularly drink coffee are dependent on caffeine.\n∀x (Drinks(x) ⊕ Jokes(x)) ::: People either regularly drink coffee or joke about being addicted to caffeine.\n∀x (Jokes(x) → ¬Unaware(x)) ::: No one who jokes about being addicted to caffeine is unaware that caffeine is a drug.\n(Student(rina) ∧ Unaware(rina)) ⊕ ¬(Student(rina) ∨ Unaware(rina)) ::: Rina is either a student and unaware that caffeine is a drug, or neither a student nor unaware that caffeine is a drug.\n¬(Dependent(rina) ∧ Student(rina)) → (Dependent(rina) ∧ Student(rina)) ⊕ ¬(Dependent(rina) ∨ Student(rina)) ::: If Rina is not a person dependent on caffeine and a student, then Rina is either a person dependent on caffeine and a student, or neither a person dependent on caffeine nor a student.\nConclusion:Jokes(rina) ⊕ Unaware(rina) ::: Rina is either a person who jokes about being addicted to caffeine or is unaware that caffeine is a drug.

Aggregation Process
1. Identify Key Conditions
    - If Drinks(rina), then Dependent(rina).
    - Drinks(rina) ⊕ Jokes(rina).
    - If Jokes(rina), then ¬Unaware(rina).
    - (Student(rina) ∧ Unaware(rina)) ⊕ (¬Student(rina) ∧ ¬Unaware(rina)).
    - ¬(Dependent(rina) ∧ Student(rina)) → ((Dependent(rina) ∧ Student(rina)) ⊕ (¬Dependent(rina) ∧ ¬Student(rina))).

2. Simplify and Combine Conditions:
    - From (Student(rina) ∧ Unaware(rina)) ⊕ (¬Student(rina) ∧ ¬Unaware(rina)):
        - If Student(rina), then Unaware(rina).
        - If ¬Student(rina), then ¬Unaware(rina).

3. Analyze Logical Implications:
    - From Jokes(rina) → ¬Unaware(rina):
        - If Jokes(rina), then Unaware(rina) must be false.

4. Evaluate the Conclusion:
- If Unaware(rina) is true, Jokes(rina) must be false.
- If Jokes(rina) is true, Unaware(rina) must be false.
- Both scenarios satisfy Jokes(rina) ⊕ Unaware(rina)

Conclusion:
Based on the analysis, the statement "Rina is either a person who jokes about being addicted to caffeine or is unaware that caffeine is a drug" is True.

Output: A
</Example>

{input}

{question}

{options}

{raw_logic_programs}

Output:
"""

forward_chaining_FOL_prompt="""<Instruction>
You are given a logical reasoning problem with a set of premises and a conclusion. Your task is to perform forward chaining to determine if the conclusion is true, false, or uncertain based on the premises.
</Instruction>

<Approach>
1. Identify and List the Premises and Conclusion:
    - Write down all the premises provided.
    - State the conclusion that needs to be evaluated.
2. Initialize Known Facts:
    - Identify any facts that are immediatly known from the premises.
    - Note down these initial facts
3. Apply Forward Chaining:
    - Step 1: Look at each premise and determine if it can be applied with the current known facts
        - If a premise involves a condition (e.g., Predicate(x)), check if you have enough information to determine if that condition is ture or false for any (x).
    - Step 2: Use the premises to infer new facts.
        - When a premise is satisfied, record any new facts that can be derived.
    - Step 3: Repeat this process, using newly derived facts to apply other premises, until no more new facts can be derived.
4. Derive and Evaluate the Conclusion:
    - Compare the derived facts with the conclustion to see it it holds true.
    - Based on the available information, determie if the conclusion is ture, false, or uncertain.
</Approach>

<Example>
Context: All people who regularly drink coffee are dependent on caffeine. People either regularly drink coffee or joke about being addicted to caffeine. No one who jokes about being addicted to caffeine is unaware that caffeine is a drug. Rina is either a student and unaware that caffeine is a drug, or neither a student nor unaware that caffeine is a drug. If Rina is not a person dependent on caffeine and a student, then Rina is either a person dependent on caffeine and a student, or neither a person dependent on caffeine nor a student.

Question: Based on the above information, is the following statement true, false, or uncertain? Rina is either a person who jokes about being addicted to caffeine or is unaware that caffeine is a drug.

Options: A) True, B) False, C) Uncertain

Raw logic programs: Predicates:Dependent(x) ::: x is a person dependent on caffeine.\nDrinks(x) ::: x regularly drinks coffee.\nJokes(x) ::: x jokes about being addicted to caffeine.\nUnaware(x) ::: x is unaware that caffeine is a drug.\nStudent(x) ::: x is a student.\nPremises:∀x (Drinks(x) → Dependent(x)) ::: All people who regularly drink coffee are dependent on caffeine.\n∀x (Drinks(x) ⊕ Jokes(x)) ::: People either regularly drink coffee or joke about being addicted to caffeine.\n∀x (Jokes(x) → ¬Unaware(x)) ::: No one who jokes about being addicted to caffeine is unaware that caffeine is a drug.\n(Student(rina) ∧ Unaware(rina)) ⊕ ¬(Student(rina) ∨ Unaware(rina)) ::: Rina is either a student and unaware that caffeine is a drug, or neither a student nor unaware that caffeine is a drug.\n¬(Dependent(rina) ∧ Student(rina)) → (Dependent(rina) ∧ Student(rina)) ⊕ ¬(Dependent(rina) ∨ Student(rina)) ::: If Rina is not a person dependent on caffeine and a student, then Rina is either a person dependent on caffeine and a student, or neither a person dependent on caffeine nor a student.\nConclusion:Jokes(rina) ⊕ Unaware(rina) ::: Rina is either a person who jokes about being addicted to caffeine or is unaware that caffeine is a drug.

List the Premises and Conclusions:
Premise 1: ∀x (Drinks(x) → Dependent(x))
Premise 2: ∀x (Drinks(x) ⊕ Jokes(x))
Premise 3: ∀x (Jokes(x) → ¬Unaware(x))
Premise 4: (Student(rina) ∧ Unaware(rina)) ⊕ ¬(Student(rina) ∨ Unaware(rina))
Premise 5: ¬(Dependent(rina) ∧ Student(rina)) → (Dependent(rina) ∧ Student(rina)) ⊕ ¬(Dependent(rina) ∨ Student(rina))
Conclusion: Jokes(rina) ⊕ Unaware(rina)

Initialize Known Facts
From Premise 4, we know:
    - Rina is either (a student and unaware that caffeine is a drug) or (neither a student nor unaware that caffeine is a drug).

Step-by-Step Forward Chaining:
Case 1: Student(rina) and Unaware(rina)
    - According to Premise 3: Jokes(rina) → ¬Unaware(rina)
        - Unaware(rina) is true, so Jokes(rina) must be false.
    - Hence, Jokes(rina) is false and Unaware(rina) is true.
    - Evaluate Jokes(rina) ⊕ Unaware(rina):
        - Jokes(rina) is false and Unaware(rina) is true, so the conclusion Jokes(rina) ⊕ Unaware(rina) is true.
Case 2: ¬Student(rina) and ¬Unaware(rina)
    - From Premise 5: ¬(Dependent(rina) ∧ Student(rina)) → ((Dependent(rina) ∧ Student(rina)) ⊕ ¬(Dependent(rina) ∨ Student(rina)))
        - If Student(rina) is flase, then the implication needs to be checked:
            - If Rina is not a student, the dereived fact does not conflict with other premises.
    - According to Premise 2: Drinks(rina) ⊕ Jokes(rina)
        - If Rina does not drink coffee, she must joke about being addicted to caffeine.
        - Since Drinks(rina) is not stated, assume Jokes(rina) is true.
    - Evaluate Jokes(rina) ⊕ Unaware(rina):
        - Jokes(rina) is true and Unaware(rina) is flase, so the conclusion Jokes(rina) ⊕ Unaware(rina) is true.

Conclusion: In both cases derived from the premises, the conclusion Jokes(rina) ⊕ Unaware(rina) holds true. Rina is either a person who jokes about being addicted to caffeine or is unaware that caffeine is a drug, therfore the answer is A) True.

Output: A
</Example>

{input}

{question}

{options}

{raw_logic_programs}

Output:
"""