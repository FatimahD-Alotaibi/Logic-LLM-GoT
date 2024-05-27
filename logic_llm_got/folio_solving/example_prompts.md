# Logical Reasoning Solver - Prompts and Examples

## Prompt Templates

### GENERATE: reasoning_prompt

Replace `{input_text}` with a logical reasoning problem.

```
<Instruction>
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

Output:
```

### GENERATE: reasoning_prompt_cot

Replace `{input_text}` with a logical reasoning problem.

```
<Instruction>
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

Output:
```

### GENERATE: symbolic_logic_prompt

Replace `{input}` with a logical reasoning problem and `{raw_logic_programs}` with the symbolic logic associated with the problem.

```
<Instructions>
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

Raw logic programs: Predicates:Dependent(x) ::: x is a person dependent on caffeine.\nDrinks(x) ::: x regularly drinks coffee.\nJokes(x) ::: x jokes about being addicted to caffeine.\nUnaware(x) ::: x is unaware that caffeine is a drug.\nStudent(x) ::: x is a student.\nPremises:∀x (Drinks(x) → Dependent(x)) ::: All people who regularly drink coffee are dependent on caffeine.\n∀x (Drinks(x) ⊕ Jokes(x)) ::: People either regularly drink coffee or joke about being addicted to caffeine.\n∀x (Jokes(x) → ¬Unaware(x)) ::: No one who jokes about being addicted to caffeine is unaware that caffeine is a drug.\n(Student(rina) ∧ Unaware(rina)) ⊕ ¬(Student(rina) ∨ Unaware(rina)) ::: Rina is either a student and unaware that caffeine is a drug, or neither a student nor unaware that caffeine is a drug.\n¬(Dependent(rina) ∧ Student(rina)) → (Dependent(rina) ∧ Student(rina)) ⊕ ¬(Dependent(rina) ∨ Student(rina)) ::: If Rina is not a person dependent on caffeine and a student, then Rina is either a person dependent on caffeine and a student, or neither a person dependent on caffeine nor a student.\nConclusion:Jokes(rina) ⊕ Unaware(rina) ::: Rina is either a person who jokes about being addicted to caffeine or is unaware that caffeine is a drug.\n((Jokes(rina) ∧ Unaware(rina)) ⊕ ¬(Jokes(rina) ∨ Unaware(rina))) → (Jokes(rina) ∧ Drinks(rina)) ::: If Rina is either a person who jokes about being addicted to caffeine and a person who is unaware that caffeine is a drug, or neither a person who jokes about being addicted to caffeine nor a person who is unaware that caffeine is a drug, then Rina jokes about being addicted to caffeine and regularly drinks coffee.

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

{raw_logic_programs}

Output:
```
