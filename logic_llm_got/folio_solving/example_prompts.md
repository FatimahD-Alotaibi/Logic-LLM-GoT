# Logical Reasoning Solver - Prompts and Examples

## Prompt Templates

### GENERATE: reasoning_prompt_io

Replace `{context}` with the narrative to the logical reasoning problem.
Replace `{question}` with the question that needs to be answered.
Replace `{options}` with the multiple choice answers.
Replace `{raw_logic_programs}` with the symbolic logic programs of the logical reasoning problem.

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

{context}

{question}

{options}

{raw_logic_programs}

Output:
```

### GENERATE: reasoning_prompt_cot

Replace `{context}` with the narrative to the logical reasoning problem.
Replace `{question}` with the question that needs to be answered.
Replace `{options}` with the multiple choice answers.
Replace `{raw_logic_programs}` with the symbolic logic programs of the logical reasoning problem.

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

{context}

{question}

{options}

{raw_logic_programs}

Output:
```

### Split: got_split_prompt

Replace `{raw_logic_programs}` with the symbolic logic programs of the reasoning problem.

```
<Instructions>
Split the following Predicates from the input text into individual sentences. Output each sentence in the following format without additional text or thoughts. DO NOT Premises or Conclusion!!!
{{
    "Initial Fact 1": "Predicate 1... ::: description text...",
    "Initial Fact 2": "Predicate 2... ::: description text...",
    "Initial Fact 3": "Predicate 3... ::: description text...",
    ...
}}
</Instructions>

<Example>
Input:
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

Output:
{{
    "Initial Fact 1": "Dependent(x) ::: x is a person dependent on caffeine.",
    "Initial Fact 2": "Drinks(x) ::: x regularly drinks coffee.",
    "Initial Fact 3": "Jokes(x) ::: x jokes about being addicted to caffeine.",
    "Initial Fact 4": "Unaware(x) ::: x is unaware that caffeine is a drug.",
    "Initial Fact 5": "Student(x) ::: x is a student."
}}
</Example>

Input:
{raw_logic_programs}

Output:
```

### Infer facts: apply_rules_prompt

Replace `{initial_fact}` with the initial fact that will derive new facts based on a set of rules.
Replace `{rules}` with a set of rules.

```
<Instructions>
Given an initial fact and a set of logical rules, derive all possible inferred facts. Apply each rule iteratively until no more new conclusions can be drawn. Provide the inferred facts in logical format, along with their descriptions.
</Instructions>

<Approach>
1. Start with the initial fact.
2. Apply each rule to the current set of facts.
3. If a new fact is derived, add it to the set of known facts.
4. Repeat the process until no new facts can be derived.
5 Present the final set of inferred facts in logical format with descriptions.
<Approach>

<Example>
Initial Fact:
Dependent(x) ::: x is a person dependent on caffeine.

Rules:
∀x (Drinks(x) → Dependent(x)) ::: All people who regularly drink coffee are dependent on caffeine.
∀x (Drinks(x) ⊕ Jokes(x)) ::: People either regularly drink coffee or joke about being addicted to caffeine.
∀x (Jokes(x) → ¬Unaware(x)) ::: No one who jokes about being addicted to caffeine is unaware that caffeine is a drug.
(Student(rina) ∧ Unaware(rina)) ⊕ ¬(Student(rina) ∨ Unaware(rina)) ::: Rina is either a student and unaware that caffeine is a drug, or neither a student nor unaware that caffeine is a drug.
¬(Dependent(rina) ∧ Student(rina)) → (Dependent(rina) ∧ Student(rina)) ⊕ ¬(Dependent(rina) ∨ Student(rina)) ::: If Rina is not a person dependent on caffeine and a student, then Rina is either a person dependent on caffeine and a student, or neither a person dependent on caffeine nor a student.

Output: Dependent(rina) ::: Rina is a person dependent on caffeine.\nDrinks(rina) ⊕ Jokes(rina) ::: Rina either regularly drinks coffee or jokes about being addicted to caffeine.\nJokes(rina) → ¬Unaware(rina) ::: If Rina jokes about being addicted to caffeine, then she is not unaware that caffeine is a drug."
</Example>

Initial Fact:
{initial_fact}

Rules:
{rules}

Output:
```

### Resolution refutation: resolution_refutation_score_prompt

Replace `{facts}` with a string of inferred facts.
Replace `{rules}` with a set of rules.

```
<Instructions>
Conduct resolution refutation on the follwoing set of inferred facts and rules.
Please score the resolution refutation in terms of how consistent the inferred facts are with the given rules.
A score of 10 implies that each inferred fact is consistent with the given rules, while a score of 0 implies that at least half of the inferred facts are consistent with the given rules.
You may provide reasoning for your scoring, but the final score for consistency should be between the tags <Consistency> and </Consitency>, without any additional text within the tag.
</Instructions>

<Approach>
Step 1: Negate the Inferred Facts
Step 2: Convert All Statements into CNF
Step 3: Apply Resolution
Step 4: Derive Contradiction
</Appraoch>

<Example>
Inferred Facts:
Dependent(rina) ::: Rina is a person dependent on caffeine.
Drinks(rina) ⊕ Jokes(rina) ::: Rina either regularly drinks coffee or jokes about being addicted to caffeine.
Jokes(rina) → ¬Unaware(rina) ::: If Rina jokes about being addicted to caffeine, then she is not unaware that caffeine is a drug.

Rules:
∀x (Drinks(x) → Dependent(x)) ::: All people who regularly drink coffee are dependent on caffeine.
∀x (Drinks(x) ⊕ Jokes(x)) ::: People either regularly drink coffee or joke about being addicted to caffeine.
∀x (Jokes(x) → ¬Unaware(x)) ::: No one who jokes about being addicted to caffeine is unaware that caffeine is a drug.
(Student(rina) ∧ Unaware(rina)) ⊕ ¬(Student(rina) ∨ Unaware(rina)) ::: Rina is either a student and unaware that caffeine is a drug, or neither a student nor unaware that caffeine is a drug.
¬(Dependent(rina) ∧ Student(rina)) → (Dependent(rina) ∧ Student(rina)) ⊕ ¬(Dependent(rina) ∨ Student(rina)) ::: If Rina is not a person dependent on caffeine and a student, then Rina is either a person dependent on caffeine and a student, or neither a person dependent on caffeine nor a student.

Reoslution Refutation:
Negate these inferred facts (Step 1):
1. ¬Dependent(rina)
2. ¬(Drinks(rina) ⊕ Jokes(rina))
3. ¬(Jokes(rina) → ¬Unaware(rina))

Convert all statements into Conjunctive Normal Form (CNF)(Step 2):
1. ∀x (Drinks(x) → Dependent(x))
    - ¬Drinks(x) ∨ Dependent(x)

2. ∀x (Drinks(x) ⊕ Jokes(x))
    - (Drinks(x) ∨ Jokes(x)) ∧ (¬Drinks(x) ∨ ¬Jokes(x))

3. ∀x (Jokes(x) → ¬Unaware(x))
    - ¬Jokes(x) ∨ ¬Unaware(x)

4. (Student(rina) ∧ Unaware(rina)) ⊕ ¬(Student(rina) ∨ Unaware(rina))
    - (Student(rina) ∧ Unaware(rina)) ⊕ (¬Student(rina) ∧ ¬Unaware(rina))

5. ¬(Dependent(rina) ∧ Student(rina)) → (Dependent(rina) ∧ Student(rina)) ⊕ ¬(Dependent(rina) ∨ Student(rina))
    - (¬Dependent(rina) ∨ ¬Student(rina)) ∨ ((Dependent(rina) ∧ Student(rina)) ⊕ (¬Dependent(rina) ∧ ¬Student(rina)))

Nefate Inferred Facts in CNF:
1. ¬Dependent(rina)
2. (¬Drinks(rina) ∧ ¬Jokes(rina)) ∨ (Drinks(rina) ∧ Jokes(rina))
3. Jokes(rina) ∧ Unaware(rina)

Apply resolution (Step 3):
Now, use these clauses to attempt to derive a contradiction.

Given ¬Dependent(rina) and the rule ¬Drinks(rina) ∨ Dependent(rina), we can't directly resolve.

Given the negation of Drinks(rina) ⊕ Jokes(rina):
    - (¬Drinks(rina) ∧ ¬Jokes(rina)) ∨ (Drinks(rina) ∧ Jokes(rina))
This means either (¬Drinks(rina) ∧ ¬Jokes(rina)) or (Drinks(rina) ∧ Jokes(rina)).

Given Jokes(rina) ∧ Unaware(rina) (from the negation of the third inferred fact).

From the original rules:

¬Jokes(rina) ∨ ¬Unaware(rina)

We can resolve Jokes(rina) ∧ Unaware(rina) with ¬Jokes(rina) ∨ ¬Unaware(rina) to derive a contradiction. Specifically:

Jokes(rina)
Unaware(rina)
¬Jokes(rina) ∨ ¬Unaware(rina)
Resolving these, we get both Unaware(rina) and ¬Unaware(rina), which is a contradiction.

Conslusion (Step 4):
We have derived a contradiction from the negation of the inferred facts along with the given rules. This means the original inferred facts are consistent with the given rules. Thus, the original inferred facts Dependent(rina), Drinks(rina) ⊕ Jokes(rina), and Jokes(rina) → ¬Unaware(rina) are true given the rules and the initial fact Dependent(x).

Output: Since each inferred fact is consistent with the given rules, the inferred facts get the highest score. <Consistency>10</Consistency>
</Example>

Facts:
{facts}

Rules:
{rules}

Output:
```

### Aggregate: aggregate_prompt

Replace `{input1}` with the inferred facts of the first thought.
Replace `{input2}` with the inferred facts of the second thought.

```
<Instructions>
Combine the following 2 strings, each containing a logic program and description, into a single string.

The format of the string should be:
Some logic program ::: Some description text.
Some logic program ::: Some description text.
Some logic program ::: Some description text.
...
<Instructions>

Combine the following strings into a single string:
{input1}

{input2}

Combined Output:
```
