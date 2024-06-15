abductive_prompt_io = """<Instructions>
Given the following narrative and goal statement, determine if the goal statement is True or False. Use the program to help you determine if the goal is True or False.
</Instructions>

<Example>
Narrative: [Alice] celebrated her birthday with her son [Ben]. [Chris] visited his sister [Alice] and her family. [David] played soccer with his cousin [Ben]. [Eve] baked a cake for her grandson [David].

Program:
statement: isRelationOf(ben, son, alice).
description: [Alice] celebrated her birthday with her son [Ben].
statement: isRelationOf(chris, brother, alice).
description: [Chris] visited his sister [Alice] and her family.
statement: isRelationOf(david, cousin, ben)
description: [David] played soccer with his cousin [Ben].
statement: isRelationOf(david, grandson, eve).
description: [Eve] baked a cake for her grandson [David].

Goal: relation(chris, uncle, david)

Answer: True
.....
Narrative: [Olivia] went to a concert with her son [Liam]. [Emma] had lunch with her brother [Liam] and their cousin [Noah]. [Mason] played chess with his uncle [Noah]. [Sophia] received a gift from her granddaughter [Emma].

Program:
statement: isRelationOf(liam, son, olivia).
description: [Olivia] went to a concert with her son [Liam].
statement: isRelationOf(emma, sister, liam).
description: [Emma] had lunch with her brother [Liam] and their cousin [Noah].
statement: isRelationOf(noah, cousin, emma).
description: [Emma] had lunch with her brother [Liam] and their cousin [Noah].
statement: isRelationOf(mason, nephew, noah).
description: [Mason] played chess with his uncle [Noah].
statement: isRelationOf(emma, granddaughter, sophia).
description: [Sophia] received a gift from her granddaughter [Emma].

Goal: relation(mason, nephew, emma)

Answer: True
.....
Narrative: [Ava] went on a picnic with her son [Ethan]. [Lucas] took his sister [Mia] to the movies. [Ethan] played video games with his cousin [Lucas]. [Sophia] enjoyed a dinner prepared by her granddaughter [Mia].

Program:
statement: isRelationOf(ethan, son, ava).
description: [Ava] went on a picnic with her son [Ethan].
statement: isRelationOf(lucas, brother, mia).
description: [Lucas] took his sister [Mia] to the movies.
statement: isRelationOf(lucas, cousin, ethan).
description: [Ethan] played video games with his cousin [Lucas].
statement: isRelationOf(mia, granddaughter, sophia).
description: [Sophia] enjoyed a dinner prepared by her granddaughter [Mia].

Goal: relation(ethan, brother, sophia)

Answer: False
</Example>

Narrative: {body_text}

Program:
{program}

Goal: {goal}

Answer: 
"""

abductive_prompt_cot = """<Instructions>
Given the following narrative and goal statement, determine if the goal statement is True or False. Use the program to help you determine if the goal is True or False. Explain your inference.
</Instructions>

<Approach>
When printing your response, you should follow the EXACT same format as the examples provided. DO NOT USE ANY OTHER FORMAT!!!
</Approach>

<Example>
Narrative: [Alice] celebrated her birthday with her son [Ben]. [Chris] visited his sister [Alice] and her family. [David] played soccer with his cousin [Ben]. [Eve] baked a cake for her grandson [David].

Program:
statement: isRelationOf(ben, son, alice).
description: [Alice] celebrated her birthday with her son [Ben].
statement: isRelationOf(chris, brother, alice).
description: [Chris] visited his sister [Alice] and her family.
statement: isRelationOf(david, cousin, ben).
description: [David] played soccer with his cousin [Ben].
statement: isRelationOf(david, grandson, eve).
description: [Eve] baked a cake for her grandson [David].

Goal: relation(chris, uncle, david)

Inference: From the program, we know that Ben is Alice's son. Chris is Alice's brother, which makes Chris Ben's uncle. David is Ben's cousin. This implies that David's parent is a sibling of Ben's parent (Alice). Since Chris is Alice's brother, Chris is also the uncle of David because the uncle relationship extends to the children of siblings. Therefore, the goal statement relation(chris, uncle, david) is True. Answer: True
.....
Narrative: [Ava] went on a picnic with her son [Ethan]. [Lucas] took his sister [Mia] to the movies. [Ethan] played video games with his cousin [Lucas]. [Sophia] enjoyed a dinner prepared by her granddaughter [Mia].

Program:
statement: isRelationOf(ethan, son, ava).
description: [Ava] went on a picnic with her son [Ethan].
statement: isRelationOf(lucas, brother, mia).
description: [Lucas] took his sister [Mia] to the movies.
statement: isRelationOf(lucas, cousin, ethan).
description: [Ethan] played video games with his cousin [Lucas].
statement: isRelationOf(mia, granddaughter, sophia).
description: [Sophia] enjoyed a dinner prepared by her granddaughter [Mia].

Goal: relation(ethan, brother, sophia)

Inference: From the program, we know that Ethan is Ava's son. Lucas is Mia's brother. Ethan and Lucas are cousins, which implies that one of Ethan's parents is a sibling of one of Lucas's parents. Mia is Sophia's granddaughter. For Ethan to be Sophia's brother, Ethan would need to be a child of Sophia's parents. However, Ethan is a child of Ava, and there is no information suggesting that Ava is Sophia's mother or that Ethan and Sophia share the same parents. Therefore, the goal statement relation(ethan, brother, sophia) is False. Answer: False
.....
Narrative: [Olivia] spent the weekend with her daughter [Emma]. [Noah] played chess with his niece [Sophia]. [Emma] went to a concert with her cousin [Liam]. [Sophia] received a birthday card from her grandmother [Isabella].

Program:
statement: isRelationOf(emma, daughter, olivia).
description: [Olivia] spent the weekend with her daughter [Emma].
statement: isRelationOf(sophia, niece, noah).
description: [Noah] played chess with his niece [Sophia].
statement: isRelationOf(liam, cousin, emma).
description: [Emma] went to a concert with her cousin [Liam].
statement: isRelationOf(sophia, granddaughter, isabella).
description: [Sophia] received a birthday card from her grandmother [Isabella].

Goal: relation(noah, brother, emma)

Inference: From the program, we know that Emma is Olivia's daughter. Sophia is Noah's niece, indicating that Noah has a sibling who is Sophia's parent. Liam is Emma's cousin, which implies that one of Emma's parents is a sibling of one of Liam's parents. Sophia is Isabella's granddaughter, indicating that Isabella is the mother of one of Sophia's parents. For Noah to be Emma's brother, Noah would need to share a parent with Emma. There is no information suggesting that Noah and Emma share the same parents or that Olivia is Noah's mother. Therefore, the goal statement relation(noah, brother, emma) is False. Answer: False
</Example>

Narrative: {body_text}

Program:
{program}

Goal: {goal}

Reasoning: 
"""

got_split_prompt = """<Instructions>
Split the following Predicates from the input text into individual sentences. Output each sentence in the following format without additional text or thoughts. DO NOT Premises or Conclusion!!!
{{
    "Initial Fact 1": "Predicate 1... ::: description text...",
    "Initial Fact 2": "Predicate 2... ::: description text...",
    "Initial Fact 3": "Predicate 3... ::: description text...",
    ...
}}
</Instructions>

<Example>
Predicates:
Kind(x): x is kind
Thin(x): x is thin
Huge(x): x is huge
Bad(x): x is bad
Poor(x): x is poor
Dull(x): x is dull
Nice(x): x is nice
Smart(x): x is smart
Quiet(x): x is quiet
Strong(x): x is strong
Small(x): x is small
Little(x): x is little
Short(x): x is short
Heavy(x): x is heavy
Tiny(x): x is tiny
Imperfect(x): x is imperfect
Sad(x): x is sad
High(x): x is high
Big(x): x is big
NotShort(x): x is not short

Facts:
Kind(Bob)
Thin(Harry)
Huge(Fiona)
Tiny(Harry)
Strong(Fiona)
Small(Harry)
Imperfect(Charlie)
Sad(Charlie)
Big(Fiona)
Nice(Bob)
Poor(Charlie)
NotShort(Harry)

Rules:
∀x(Huge(x) ∧ Bad(x) ∧ Poor(x) → Dull(x))
∀x(Nice(x) ∧ Smart(x) ∧ Kind(x) → Quiet(x))
∀x(Nice(x) ∧ Small(x) ∧ Little(x) → Short(x))
∀x(Small(x) ∧ Nice(x) ∧ Bad(x) → Heavy(x))
∀x(Little(x) ∧ Tiny(x) ∧ Small(x) → Short(x))
∀x(High(x) ∧ Tiny(x) ∧ Strong(x) → Heavy(x))
∀x(Tiny(x) ∧ Smart(x) ∧ Strong(x) → Dull(x))
∀x(High(x) ∧ Sad(x) ∧ Kind(x) → Short(x))
∀x(Poor(x) ∧ Bad(x) ∧ Sad(x) → Dull(x))
∀x(Huge(x) ∧ Strong(x) ∧ High(x) → Heavy(x))
∀x(Kind(x) ∧ Sad(x) ∧ Smart(x) → Quiet(x))
∀x(Little(x) ∧ Huge(x) ∧ Poor(x) → Quiet(x))

Query:
NotShort(Harry)"

Output:
{{
    "Initial Fact 1": "Kind(Bob) ::: Bob is kind.",
    "Initial Fact 2": "Thin(Harry) ::: Harry is thin.",
    "Initial Fact 3": "Huge(Fiona) ::: Fiona is Huge.",
    "Initial Fact 4": "Tiny(Harry) ::: Harry is Tiny.",
    "Initial Fact 5": "Strong(Fiona) ::: Fiona is Strong.",
    "Initial Fact 6": "Small(Harry) ::: Harry is Small.",
    "Initial Fact 7": "Imperfect(Charlie) ::: Charlie is Imperfect.",
    "Initial Fact 8": "Sad(Charlie) ::: Charlie is Sad.",
    "Initial Fact 9": "Big(Fiona) ::: Fiona is Big.",
    "Initial Fact 10": "Nice(Bob) ::: Bob is Nice.",
    "Initial Fact 11": "Poor(Charlie) ::: Charlie is Poor.",
    "Initial Fact 12": "NotShort(Harry) ::: Harry is Not Short."
}}
</Example>
Input:
{raw_logic_programs}

Output:
"""

infer_facts_prompt = """<Instructions>
Given a context prompt, an initial fact and a set of logical rules, derive all possible inferred facts. Apply each rule iteratively until no more new conclusions can be drawn. Provide the inferred facts in logical format, along with their descriptions.
</Instructions>

<Approach>
1. Start with the initial fact and the context prompt.
2. Apply each rule to the current set of facts.
3. If a new fact is derived, add it to the set of known facts.
4. Repeat the process until no new facts can be derived.
5. Present the final set of inferred facts in logical format with descriptions.
<Approach>

<Rules>
∀x(Huge(x) ∧ Bad(x) ∧ Poor(x) → Dull(x))
∀x(Nice(x) ∧ Smart(x) ∧ Kind(x) → Quiet(x))
∀x(Nice(x) ∧ Small(x) ∧ Little(x) → Short(x))
∀x(Small(x) ∧ Nice(x) ∧ Bad(x) → Heavy(x))
∀x(Little(x) ∧ Tiny(x) ∧ Small(x) → Short(x))
∀x(High(x) ∧ Tiny(x) ∧ Strong(x) → Heavy(x))
∀x(Tiny(x) ∧ Smart(x) ∧ Strong(x) → Dull(x))
∀x(High(x) ∧ Sad(x) ∧ Kind(x) → Short(x))
∀x(Poor(x) ∧ Bad(x) ∧ Sad(x) → Dull(x))
∀x(Huge(x) ∧ Strong(x) ∧ High(x) → Heavy(x))
∀x(Kind(x) ∧ Sad(x) ∧ Smart(x) → Quiet(x))
∀x(Little(x) ∧ Huge(x) ∧ Poor(x) → Quiet(x))
</Rules>

<Example>
Context: Bob is kind. Harry is thin. All people that are huge, are bad, and are poor, are also dull. All people that are nice, are smart, and are kind, are quiet. Fiona is huge. Harry is tiny. Fiona is strong. People that are nice, are small, and are little, are short. If a person is small, is nice, and is bad, that person is also heavy. Harry is small. Charlie is imperfect. Charlie is sad. If a person is little, is tiny, and is small, that person is also short. Fiona is big. If something is high, is tiny, and is strong, it is heavy. If a person is tiny, is smart, and is strong, that person is dull. If a person is high, is sad, and is kind, that person is also short. Bob is nice. If something is poor, is bad, and is sad, then it is also dull. Charlie is poor. All things that are huge, are strong, and are high, are heavy. If a person is kind, is sad, and is smart, that person is also quiet. If something is little, is huge, and is poor, it is quiet.

Initial Fact:
Kind(Bob) ::: Bob is kind.

Output:
Kind(Bob) ::: Bob is kind.
Nice(Bob) ::: Bob is nice.
Huge(Fiona) ::: Fiona is huge.
Tiny(Harry) ::: Harry is tiny.
Strong(Fiona) ::: Fiona is strong.
Small(Harry) ::: Harry is small.
Sad(Charlie) ::: Charlie is sad.
Poor(Charlie) ::: Charlie is poor.
Short(Harry) ::: Harry is short.
Dull(Charlie) ::: Charlie is dull.
</Example>

Input:
Rules:
{rules}

Context: {context}

Initial Fact:
{initial_fact}

Output:
"""

resolution_refutation_score_prompt="""<Instructions>
Conduct resolution refutation on the following set of inferred facts and context prompt.
Please score the resolution refutation in terms of how consistent the inferred facts are with the given context prompt. 
A score of 10 implies that each inferred fact is consistent with the given rules, while a score of 0 implies that at least half of the inferred facts are consistent with the given narrative. 
You may provide reasoning for your scoring, but the final score for consistency should be between the tags <Consistency> and </Consitency>, without any additional text within the tag.
</Instructions>

<Approach>
Step 1: Negate the Inferred Facts
Step 2: Convert All Statements into CNF
Step 3: Apply Resolution
Step 4: Derive Contradiction
</Appraoch>

<Example>
Facts:
Kind(Bob) ::: Bob is kind.
Nice(Bob) ::: Bob is nice.
Huge(Fiona) ::: Fiona is huge.
Tiny(Harry) ::: Harry is tiny.
Strong(Fiona) ::: Fiona is strong.
Small(Harry) ::: Harry is small.
Sad(Charlie) ::: Charlie is sad.
Poor(Charlie) ::: Charlie is poor.
Short(Harry) ::: Harry is short.
Dull(Charlie) ::: Charlie is dull.

Context: Bob is kind. Harry is thin. All people that are huge, are bad, and are poor, are also dull. All people that are nice, are smart, and are kind, are quiet. Fiona is huge. Harry is tiny. Fiona is strong. People that are nice, are small, and are little, are short. If a person is small, is nice, and is bad, that person is also heavy. Harry is small. Charlie is imperfect. Charlie is sad. If a person is little, is tiny, and is small, that person is also short. Fiona is big. If something is high, is tiny, and is strong, it is heavy. If a person is tiny, is smart, and is strong, that person is dull. If a person is high, is sad, and is kind, that person is also short. Bob is nice. If something is poor, is bad, and is sad, then it is also dull. Charlie is poor. All things that are huge, are strong, and are high, are heavy. If a person is kind, is sad, and is smart, that person is also quiet. If something is little, is huge, and is poor, it is quiet.

Step 1: Negate the Inferred Facts
1. ¬Kind(Bob)
2. ¬Nice(Bob)
3. ¬Huge(Fiona)
4. ¬Tiny(Harry)
5. ¬Strong(Fiona)
6. ¬Small(Harry)
7. ¬Sad(Charlie)
8. ¬Poor(Charlie)
9. ¬Short(Harry)
10. ¬Dull(Charlie)

Step 2: Convert All Statements into CNF
1. ¬Huge(x) ∨ ¬Bad(x) ∨ ¬Poor(x) ∨ Dull(x)
2. ¬Nice(x) ∨ ¬Smart(x) ∨ ¬Kind(x) ∨ Quiet(x)
3. ¬Nice(x) ∨ ¬Small(x) ∨ ¬Little(x) ∨ Short(x)
4. ¬Small(x) ∨ ¬Nice(x) ∨ ¬Bad(x) ∨ Heavy(x)
5. ¬Little(x) ∨ ¬Tiny(x) ∨ ¬Small(x) ∨ Short(x)
6. ¬High(x) ∨ ¬Tiny(x) ∨ ¬Strong(x) ∨ Heavy(x)
7. ¬Tiny(x) ∨ ¬Smart(x) ∨ ¬Strong(x) ∨ Dull(x)
8. ¬High(x) ∨ ¬Sad(x) ∨ ¬Kind(x) ∨ Short(x)
9. ¬Poor(x) ∨ ¬Bad(x) ∨ ¬Sad(x) ∨ Dull(x)
10. ¬Huge(x) ∨ ¬Strong(x) ∨ ¬High(x) ∨ Heavy(x)
11. ¬Kind(x) ∨ ¬Sad(x) ∨ ¬Smart(x) ∨ Quiet(x)
12. ¬Little(x) ∨ ¬Huge(x) ∨ ¬Poor(x) ∨ Quiet(x)

Step 3: Apply Resolution
1. ¬Kind(Bob):
        - Kind(Bob) (given fact)
        - Contradiction: Kind(Bob) ∧ ¬Kind(Bob)
2. ¬Nice(Bob):
        - Nice(Bob) (given fact)
        - Contradiction: Nice(Bob) ∧ ¬Nice(Bob)
3. Huge(Fiona):
        - Huge(Fiona) (given fact)
        - Contradiction: Huge(Fiona) ∧ ¬Huge(Fiona)
4. ¬Tiny(Harry):
        - Tiny(Harry) (given fact)
        - Contradiction: Tiny(Harry) ∧ ¬Tiny(Harry)
5. ¬Strong(Fiona):
        - Strong(Fiona) (given fact)
        - Contradiction: Strong(Fiona) ∧ ¬Strong(Fiona)
6. ¬Small(Harry):
        - Small(Harry) (given fact)
        - Contradiction: Small(Harry) ∧ ¬Small(Harry)
7. ¬Sad(Charlie):
        - Sad(Charlie) (given fact)
        - Contradiction: Sad(Charlie) ∧ ¬Sad(Charlie)
8. ¬Poor(Charlie):
        - Poor(Charlie) (given fact)
        - Contradiction: Poor(Charlie) ∧ ¬Poor(Charlie)
9. ¬Short(Harry):
        - From Little(x) ∧ Tiny(x) ∧ Small(x) → Short(x)
        - Harry is small, tiny (given facts)
        - ¬Little(Harry) or ¬Short(Harry)
        - No direct contradiction.
10. ¬Dull(Charlie):
        - From Poor(x) ∧ Bad(x) ∧ Sad(x) → Dull(x)
        - Charlie is poor and sad (given facts)
        - ¬Bad(Charlie) or ¬Dull(Charlie)
        - No direct contradiction.

Step 4: Derive Contradiction
We have identified direct contradictions for most inferred facts except for "Short(Harry)" and "Dull(Charlie)". These exceptions are due to the lack of additional facts to trigger the respective rules. Since most of the inferred facts directly contradict the given context and facts, the consistency score is high.

Output: <Consistency>9</Consistency>
</Example>

Facts: 
{facts}

Context: {context}
"""

aggregate_prompt = """<Instructions>
Perform aggregation on the two sets of facts to generate a new set of facts.

The format of the string should be: 
Some logic program ::: Some description text.
Some logic program ::: Some description text.
Some logic program ::: Some description text.
...
<Instructions>

Combine the following strings into a single string:
Set 1:
{input1}

Set 2:
{input2}

New set:
"""

abductive_prompt_got = """<Instructions>
Given the following narrative and goal statement, determine if the goal statement is True or False. Use the program to help you determine if the goal is True or False. REMEMBER True == 0 and False == 0_0.
</Instructions.

<Approach>
To accurately answer the question, follow these steps:
1. Carefully read and understand the given context prompt. Identify key relationships with the subjects mentioned.
2. Pay attention to any terms that are defined or explained within the context prompt itself.
3. Use the inferred facts to help draw out your conclusion. The inferred facts should give you clues about the subjects's relationships.
</Approach>

<Example>
Context: Bob is kind. Harry is thin. All people that are huge, are bad, and are poor, are also dull. All people that are nice, are smart, and are kind, are quiet. Fiona is huge. Harry is tiny. Fiona is strong. People that are nice, are small, and are little, are short. If a person is small, is nice, and is bad, that person is also heavy. Harry is small. Charlie is imperfect. Charlie is sad. If a person is little, is tiny, and is small, that person is also short. Fiona is big. If something is high, is tiny, and is strong, it is heavy. If a person is tiny, is smart, and is strong, that person is dull. If a person is high, is sad, and is kind, that person is also short. Bob is nice. If something is poor, is bad, and is sad, then it is also dull. Charlie is poor. All things that are huge, are strong, and are high, are heavy. If a person is kind, is sad, and is smart, that person is also quiet. If something is little, is huge, and is poor, it is quiet.

Raw Logic Programs:
Predicates:
Kind(x): x is kind
Thin(x): x is thin
Huge(x): x is huge
Bad(x): x is bad
Poor(x): x is poor
Dull(x): x is dull
Nice(x): x is nice
Smart(x): x is smart
Quiet(x): x is quiet
Strong(x): x is strong
Small(x): x is small
Little(x): x is little
Short(x): x is short
Heavy(x): x is heavy
Tiny(x): x is tiny
Imperfect(x): x is imperfect
Sad(x): x is sad
High(x): x is high
Big(x): x is big
NotShort(x): x is not short

Facts:
Kind(Bob)
Thin(Harry)
Huge(Fiona)
Tiny(Harry)
Strong(Fiona)
Small(Harry)
Imperfect(Charlie)
Sad(Charlie)
Big(Fiona)
Nice(Bob)
Poor(Charlie)
NotShort(Harry)

Rules:
∀x(Huge(x) ∧ Bad(x) ∧ Poor(x) → Dull(x))
∀x(Nice(x) ∧ Smart(x) ∧ Kind(x) → Quiet(x))
∀x(Nice(x) ∧ Small(x) ∧ Little(x) → Short(x))
∀x(Small(x) ∧ Nice(x) ∧ Bad(x) → Heavy(x))
∀x(Little(x) ∧ Tiny(x) ∧ Small(x) → Short(x))
∀x(High(x) ∧ Tiny(x) ∧ Strong(x) → Heavy(x))
∀x(Tiny(x) ∧ Smart(x) ∧ Strong(x) → Dull(x))
∀x(High(x) ∧ Sad(x) ∧ Kind(x) → Short(x))
∀x(Poor(x) ∧ Bad(x) ∧ Sad(x) → Dull(x))
∀x(Huge(x) ∧ Strong(x) ∧ High(x) → Heavy(x))
∀x(Kind(x) ∧ Sad(x) ∧ Smart(x) → Quiet(x))
∀x(Little(x) ∧ Huge(x) ∧ Poor(x) → Quiet(x))

Inferred Facts:
Kind(Bob) ::: Bob is kind.
Nice(Bob) ::: Bob is nice.
Huge(Fiona) ::: Fiona is huge.
Tiny(Harry) ::: Harry is tiny.
Strong(Fiona) ::: Fiona is strong.
Small(Harry) ::: Harry is small.
Sad(Charlie) ::: Charlie is sad.
Poor(Charlie) ::: Charlie is poor.
Short(Harry) ::: Harry is short.
Dull(Charlie) ::: Charlie is dull.

Goal: Harry is not short.

Output: 0_0
</Example>

Context: {context}

Raw Logic Programs:
{raw_logic_programs}

Inferred Facts:
{aggregated_facts}

Goal: {goal}

Output:
"""