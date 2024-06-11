cluttr_prompt_io = """<Instructions>
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

cluttr_prompt_cot = """<Instructions>
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
Split the following input text into individual sentences. Output each sentence in the following format without additional text or thoughts.
{{
    "Initial Fact 1": "statement text... ::: description text...",
    "Initial Fact 2": "statement text... ::: description text...",
    "Initial Fact 3": "statement text... ::: description text...",
    ...
}}
</Instructions>

<Example>
Input:
statement: isRelationOf(ben, son, alice).
description: [Alice] celebrated her birthday with her son [Ben].
statement: isRelationOf(chris, brother, alice).
description: [Chris] visited his sister [Alice] and her family.
statement: isRelationOf(david, cousin, ben)
description: [David] played soccer with his cousin [Ben].
statement: isRelationOf(david, grandson, eve).
description: [Eve] baked a cake for her grandson [David].
Output:
{{
    "Initial Fact 1": "isRelationOf(ben, son, alice) ::: [Alice] celebrated her birthday with her son [Ben].",
    "Initial Fact 2": "isRelationOf(chris, brother, alice) ::: [Chris] visited his sister [Alice] and her family.",
    "Initial Fact 3": "isRelationOf(david, cousin, ben) ::: [David] played soccer with his cousin [Ben].",
    "Initial Fact 4": "isRelationOf(david, grandson, eve) ::: [Eve] baked a cake for her grandson [David]."
}}
</Example>

Input:
{program}

Output:
"""

infer_facts_prompt = """<Instructions>
Given a narrative, an initial fact and a set of logical rules, derive all possible inferred facts. Apply each rule iteratively until no more new conclusions can be drawn. Provide the inferred facts in logical format, along with their descriptions.
</Instructions>

<Approach>
1. Start with the initial fact and the narrative.
2. Apply each rule to the current set of facts.
3. If a new fact is derived, add it to the set of known facts.
4. Repeat the process until no new facts can be derived.
5. Present the final set of inferred facts in logical format with descriptions.
<Approach>

<Rules>
relation(A, R, B) :- isRelationOf(A, R, B) ::: If A is the some_relation of B, then A can be inferred as the some_relation of B.
relation(A, son, B) :- isRelationOf(A, brother, C), relation(C, (son;daughter), B), B != A ::: If A is the brother of C, and C can be inferred as the son or the daughter of B, then A can be inferred as the son of B.
relation(A, daughter, B) :- isRelationOf(A, sister, C), relation(C, (son;daughter), B), B != A ::: If A is the sister of C, and C can be inferred as the son or the daughter of B, then A can be inferred as the daughter of B.
relation(A, son, B) :- isRelationOf(A, son, C), relation(C, (husband;wife), B), B != A ::: If A is the son of C, and C can be inferred as the husband or the wife of B, then A can be inferred as the son of B.
relation(A, daughter, B) :- isRelationOf(A, daughter, C), relation(C, (husband;wife), B), B != A ::: If A is the daughter of C, and C can be inferred as the husband or the wife of B, then A can be inferred as the daughter of B.
relation(A, father, B) :- isRelationOf(A, grandfather, C), relation(C, (son;daughter), B), B != A ::: If A is the grandfather of C, and C can be inferred as the son or the daughter of B, then A can be inferred as the father of B.
relation(A, mother, B) :- isRelationOf(A, grandmother, C), relation(C, (son;daughter), B), B != A ::: If A is the grandmother of C, and C can be inferred as the son or the daughter of B, then A can be inferred as the mother of B.
relation(A, father, B) :- isRelationOf(A, father, C), relation(C, (brother;sister), B), B != A ::: If A is the father of C, and C can be inferred as the brother or the sister of B, then A can be inferred as the father of B.
relation(A, mother, B) :- isRelationOf(A, mother, C), relation(C, (brother;sister), B), B != A ::: If A is the mother of C, and C can be inferred as the brother or the sister of B, then A can be inferred as the mother of B.
relation(A, uncle, B) :- isRelationOf(A, (brother;brother_in_law), C), relation(C, (father;mother), B), B != A ::: If A is the brother or the brother-in-law of C, and C can be inferred as the father or the mother of B, then A can be inferred as the uncle of B.
relation(A, aunt, B) :- isRelationOf(A, (sister;sister_in_law), C), relation(C, (father;mother), B), B != A ::: If A is the sister or the sister-in-law of C, and C can be inferred as the father or the mother of B, then A can be inferred as the aunt of B.
relation(A, nephew, B) :- isRelationOf(A, son, C), relation(C, (brother;sister;brother_in_law;sister_in_law), B), B != A ::: If A is the son of C, and C can be inferred as the brother / sister / brother-in-law / sister-in-law of B, then A can be inferred as the aunt of B.
relation(A, niece, B) :- isRelationOf(A, daughter, C), relation(C, (brother;sister;brother_in_law;sister_in_law), B), B != A ::: If A is the daughter of C, and C can be inferred as the brother / sister / brother-in-law / sister-in-law of B, then A can be inferred as the niece of B.
relation(A, grandfather, B) :- isRelationOf(A, father, C), relation(C, (father;mother), B), B != A ::: If A is the father of C, and C can be inferred as the father or the mother of B, then A can be inferred as the grandfather of B.
relation(A, grandmother, B) :- isRelationOf(A, mother, C), relation(C, (father;mother), B), B != A ::: If A is the mother of C, and C can be inferred as the father or the mother of B, then A can be inferred as the grandmother of B.
relation(A, grandfather, B) :- isRelationOf(A, grandfather, C), relation(C, (brother;sister), B), B != A ::: If A is the grandfather of C, and C can be inferred as the brother or the sister of B, then A can be inferred as the grandfather of B.
relation(A, grandmother, B) :- isRelationOf(A, grandmother, C), relation(C, (brother;sister), B), B != A ::: If A is the grandmother of C, and C can be inferred as the brother or the sister of B, then A can be inferred as the grandmother of B.
relation(A, grandson, B) :- isRelationOf(A, son, C), relation(C, (son;daughter), B), B != A ::: If A is the son of C, and C can be inferred as the son or the daughter of B, then A can be inferred as the grandson of B.
relation(A, granddaughter, B) :- isRelationOf(A, daughter, C), relation(C, (son;daughter), B), B != A ::: If A is the daughter of C, and C can be inferred as the son or the daughter of B, then A can be inferred as the granddaughter of B.
relation(A, grandson, B) :- isRelationOf(A, grandson, C), relation(C, (husband;wife), B), B != A ::: If A is the grandson of C, and C can be inferred as the husband or the wife of B, then A can be inferred as the grandson of B.
relation(A, granddaughter, B) :- isRelationOf(A, granddaughter, C), relation(C, (husband;wife), B), B != A ::: If A is the granddaughter of C, and C can be inferred as the husband or the wife of B, then A can be inferred as the granddaughter of B.
relation(A, grandson, B) :- isRelationOf(A, brother, C), relation(C, (grandson;granddaughter), B), B != A ::: If A is the brother of C, and C can be inferred as the grandson or the granddaughter of B, then A can be inferred as the grandson of B.
relation(A, granddaughter, B) :- isRelationOf(A, sister, C), relation(C, (grandson;granddaughter), B), B != A ::: If A is the sister of C, and C can be inferred as the grandson or the granddaughter of B, then A can be inferred as the granddaughter of B.
relation(A, father_in_law, B) :- isRelationOf(A, father, C), relation(C, (husband;wife), B), B != A ::: If A is the father of C, and C can be inferred as the husband or the wife of B, then A can be inferred as the father-in-law of B.
relation(A, mother_in_law, B) :- isRelationOf(A, mother, C), relation(C, (husband;wife), B), B != A ::: If A is the mother of C, and C can be inferred as the husband or the wife of B, then A can be inferred as the mother-in-law of B.
relation(A, son_in_law, B) :- isRelationOf(A, husband, C), relation(C, daughter, B), B != A ::: If A is the husband of C, and C can be inferred as the daughter of B, then A can be inferred as the son-in-law of B.
relation(A, daughter_in_law, B) :- isRelationOf(A, wife, C), relation(C, son, B), B != A ::: If A is the wife of C, and C can be inferred as the son of B, then A can be inferred as the daughter-in-law of B.
relation(A, brother_in_law, B) :- isRelationOf(A, husband, C), relation(C, sister, B), B != A ::: If A is the husband of C, and C can be inferred as the sister of B, then A can be inferred as the brother-in-law of B.
relation(A, sister_in_law, B) :- isRelationOf(A, wife, C), relation(C, brother, B), B != A ::: If A is the wife of C, and C can be inferred as the brother of B, then A can be inferred as the sister-in-law of B.
relation(A, husband, B) :- isRelationOf(B, wife, A), B != A ::: If A is the wife of B, then A can be inferred as the husband of B.
relation(A, wife, B) :- isRelationOf(B, husband, A), B != A ::: If A is the husband of B, then A can be inferred as the wife of B.
relation(A, husband, B) :- isRelationOf(A, father, C), relation(C, (daughter;son), B), B != A ::: If A is the father of C, and C can be inferred as the daughter or the son of B, then A can be inferred as the husband of B.
relation(A, wife, B) :- isRelationOf(A, mother, C), relation(C, (daughter;son), B), B != A ::: If A is the mother of C, and C can be inferred as the daughter or the son of B, then A can be inferred as the wife of B.
relation(A, brother, B) :- isRelationOf(A, uncle, C), relation(C, (son;daughter), B), B != A ::: If A is the uncle of C, and C can be inferred as the son or the daughter of B, then A can be inferred as the brother of B.
relation(A, sister, B) :- isRelationOf(A, aunt, C), relation(C, (son;daughter), B), B != A ::: If A is the aunt of C, and C can be inferred as the son or the daughter of B, then A can be inferred as the sister of B.
relation(A, brother, B) :- isRelationOf(A, son, C), relation(C, (father;mother), B), B != A ::: If A is the son of C, and C can be inferred as the father or the mother of B, then A can be inferred as the brother of B.
relation(A, sister, B) :- isRelationOf(A, daughter, C), relation(C, (father;mother), B), B != A ::: If A is the daughter of C, and C can be inferred as the father or the mother of B, then A can be inferred as the sister of B.
relation(A, brother, B) :- isRelationOf(A, brother, C), relation(C, (brother;sister), B), B != A ::: If A is the brother of C, and C can be inferred as the brother or the sister of B, then A can be inferred as the brother of B.
relation(A, sister, B) :- isRelationOf(A, sister, C), relation(C, (brother;sister), B), B != A ::: If A is the sister of C, and C can be inferred as the brother or the sister of B, then A can be inferred as the sister of B.
</Rules>

<Example>
Narrative: [Alice] celebrated her birthday with her son [Ben]. [Chris] visited his sister [Alice] and her family. [David] played soccer with his cousin [Ben]. [Eve] baked a cake for her grandson [David].

Initila Fact:
isRelationOf(ben, son, alice) ::: [Alice] celebrated her birthday with her son [Ben].

Output:
isRelationOf(ben, son, alice): Ben is the son of Alice.
isRelationOf(chris, brother, alice): Chris is the brother of Alice.
isRelationOf(chris, son, alice): Chris is the son of Alice.
isRelationOf(david, grandson, alice): David is the grandson of Alice.
isRelationOf(eve, grandmother, ben): Eve is the grandmother of Ben.
isRelationOf(eve, mother, alice): Eve is the mother of Alice.
isRelationOf(eve, grandmother, chris): Eve is the grandmother of Chris.
isRelationOf(david, uncle, ben): David is the uncle of Ben.

</Example>

Input:
Narrative: {narrative}

Initial Fact:
{initial_fact}

Output:
"""

apply_rules_prompt = """<Instructions>
Given a narrative, an initial fact and a set of logical rules, derive all possible inferred facts. Apply each rule iteratively until no more new conclusions can be drawn. Provide the inferred facts in logical format, along with their descriptions.
</Instructions>

<Approach>
1. Start with the initial fact and the narrative.
2. Apply each rule to the current set of facts.
3. If a new fact is derived, add it to the set of known facts.
4. Repeat the process until no new facts can be derived.
5. Present the final set of inferred facts in logical format with descriptions.
<Approach>

<Rules>
relation(A, R, B) :- isRelationOf(A, R, B) ::: If A is the some_relation of B, then A can be inferred as the some_relation of B.
relation(A, son, B) :- isRelationOf(A, brother, C), relation(C, (son;daughter), B), B != A ::: If A is the brother of C, and C can be inferred as the son or the daughter of B, then A can be inferred as the son of B.
relation(A, daughter, B) :- isRelationOf(A, sister, C), relation(C, (son;daughter), B), B != A ::: If A is the sister of C, and C can be inferred as the son or the daughter of B, then A can be inferred as the daughter of B.
relation(A, son, B) :- isRelationOf(A, son, C), relation(C, (husband;wife), B), B != A ::: If A is the son of C, and C can be inferred as the husband or the wife of B, then A can be inferred as the son of B.
relation(A, daughter, B) :- isRelationOf(A, daughter, C), relation(C, (husband;wife), B), B != A ::: If A is the daughter of C, and C can be inferred as the husband or the wife of B, then A can be inferred as the daughter of B.
relation(A, father, B) :- isRelationOf(A, grandfather, C), relation(C, (son;daughter), B), B != A ::: If A is the grandfather of C, and C can be inferred as the son or the daughter of B, then A can be inferred as the father of B.
relation(A, mother, B) :- isRelationOf(A, grandmother, C), relation(C, (son;daughter), B), B != A ::: If A is the grandmother of C, and C can be inferred as the son or the daughter of B, then A can be inferred as the mother of B.
relation(A, father, B) :- isRelationOf(A, father, C), relation(C, (brother;sister), B), B != A ::: If A is the father of C, and C can be inferred as the brother or the sister of B, then A can be inferred as the father of B.
relation(A, mother, B) :- isRelationOf(A, mother, C), relation(C, (brother;sister), B), B != A ::: If A is the mother of C, and C can be inferred as the brother or the sister of B, then A can be inferred as the mother of B.
relation(A, uncle, B) :- isRelationOf(A, (brother;brother_in_law), C), relation(C, (father;mother), B), B != A ::: If A is the brother or the brother-in-law of C, and C can be inferred as the father or the mother of B, then A can be inferred as the uncle of B.
relation(A, aunt, B) :- isRelationOf(A, (sister;sister_in_law), C), relation(C, (father;mother), B), B != A ::: If A is the sister or the sister-in-law of C, and C can be inferred as the father or the mother of B, then A can be inferred as the aunt of B.
relation(A, nephew, B) :- isRelationOf(A, son, C), relation(C, (brother;sister;brother_in_law;sister_in_law), B), B != A ::: If A is the son of C, and C can be inferred as the brother / sister / brother-in-law / sister-in-law of B, then A can be inferred as the aunt of B.
relation(A, niece, B) :- isRelationOf(A, daughter, C), relation(C, (brother;sister;brother_in_law;sister_in_law), B), B != A ::: If A is the daughter of C, and C can be inferred as the brother / sister / brother-in-law / sister-in-law of B, then A can be inferred as the niece of B.
relation(A, grandfather, B) :- isRelationOf(A, father, C), relation(C, (father;mother), B), B != A ::: If A is the father of C, and C can be inferred as the father or the mother of B, then A can be inferred as the grandfather of B.
relation(A, grandmother, B) :- isRelationOf(A, mother, C), relation(C, (father;mother), B), B != A ::: If A is the mother of C, and C can be inferred as the father or the mother of B, then A can be inferred as the grandmother of B.
relation(A, grandfather, B) :- isRelationOf(A, grandfather, C), relation(C, (brother;sister), B), B != A ::: If A is the grandfather of C, and C can be inferred as the brother or the sister of B, then A can be inferred as the grandfather of B.
relation(A, grandmother, B) :- isRelationOf(A, grandmother, C), relation(C, (brother;sister), B), B != A ::: If A is the grandmother of C, and C can be inferred as the brother or the sister of B, then A can be inferred as the grandmother of B.
relation(A, grandson, B) :- isRelationOf(A, son, C), relation(C, (son;daughter), B), B != A ::: If A is the son of C, and C can be inferred as the son or the daughter of B, then A can be inferred as the grandson of B.
relation(A, granddaughter, B) :- isRelationOf(A, daughter, C), relation(C, (son;daughter), B), B != A ::: If A is the daughter of C, and C can be inferred as the son or the daughter of B, then A can be inferred as the granddaughter of B.
relation(A, grandson, B) :- isRelationOf(A, grandson, C), relation(C, (husband;wife), B), B != A ::: If A is the grandson of C, and C can be inferred as the husband or the wife of B, then A can be inferred as the grandson of B.
relation(A, granddaughter, B) :- isRelationOf(A, granddaughter, C), relation(C, (husband;wife), B), B != A ::: If A is the granddaughter of C, and C can be inferred as the husband or the wife of B, then A can be inferred as the granddaughter of B.
relation(A, grandson, B) :- isRelationOf(A, brother, C), relation(C, (grandson;granddaughter), B), B != A ::: If A is the brother of C, and C can be inferred as the grandson or the granddaughter of B, then A can be inferred as the grandson of B.
relation(A, granddaughter, B) :- isRelationOf(A, sister, C), relation(C, (grandson;granddaughter), B), B != A ::: If A is the sister of C, and C can be inferred as the grandson or the granddaughter of B, then A can be inferred as the granddaughter of B.
relation(A, father_in_law, B) :- isRelationOf(A, father, C), relation(C, (husband;wife), B), B != A ::: If A is the father of C, and C can be inferred as the husband or the wife of B, then A can be inferred as the father-in-law of B.
relation(A, mother_in_law, B) :- isRelationOf(A, mother, C), relation(C, (husband;wife), B), B != A ::: If A is the mother of C, and C can be inferred as the husband or the wife of B, then A can be inferred as the mother-in-law of B.
relation(A, son_in_law, B) :- isRelationOf(A, husband, C), relation(C, daughter, B), B != A ::: If A is the husband of C, and C can be inferred as the daughter of B, then A can be inferred as the son-in-law of B.
relation(A, daughter_in_law, B) :- isRelationOf(A, wife, C), relation(C, son, B), B != A ::: If A is the wife of C, and C can be inferred as the son of B, then A can be inferred as the daughter-in-law of B.
relation(A, brother_in_law, B) :- isRelationOf(A, husband, C), relation(C, sister, B), B != A ::: If A is the husband of C, and C can be inferred as the sister of B, then A can be inferred as the brother-in-law of B.
relation(A, sister_in_law, B) :- isRelationOf(A, wife, C), relation(C, brother, B), B != A ::: If A is the wife of C, and C can be inferred as the brother of B, then A can be inferred as the sister-in-law of B.
relation(A, husband, B) :- isRelationOf(B, wife, A), B != A ::: If A is the wife of B, then A can be inferred as the husband of B.
relation(A, wife, B) :- isRelationOf(B, husband, A), B != A ::: If A is the husband of B, then A can be inferred as the wife of B.
relation(A, husband, B) :- isRelationOf(A, father, C), relation(C, (daughter;son), B), B != A ::: If A is the father of C, and C can be inferred as the daughter or the son of B, then A can be inferred as the husband of B.
relation(A, wife, B) :- isRelationOf(A, mother, C), relation(C, (daughter;son), B), B != A ::: If A is the mother of C, and C can be inferred as the daughter or the son of B, then A can be inferred as the wife of B.
relation(A, brother, B) :- isRelationOf(A, uncle, C), relation(C, (son;daughter), B), B != A ::: If A is the uncle of C, and C can be inferred as the son or the daughter of B, then A can be inferred as the brother of B.
relation(A, sister, B) :- isRelationOf(A, aunt, C), relation(C, (son;daughter), B), B != A ::: If A is the aunt of C, and C can be inferred as the son or the daughter of B, then A can be inferred as the sister of B.
relation(A, brother, B) :- isRelationOf(A, son, C), relation(C, (father;mother), B), B != A ::: If A is the son of C, and C can be inferred as the father or the mother of B, then A can be inferred as the brother of B.
relation(A, sister, B) :- isRelationOf(A, daughter, C), relation(C, (father;mother), B), B != A ::: If A is the daughter of C, and C can be inferred as the father or the mother of B, then A can be inferred as the sister of B.
relation(A, brother, B) :- isRelationOf(A, brother, C), relation(C, (brother;sister), B), B != A ::: If A is the brother of C, and C can be inferred as the brother or the sister of B, then A can be inferred as the brother of B.
relation(A, sister, B) :- isRelationOf(A, sister, C), relation(C, (brother;sister), B), B != A ::: If A is the sister of C, and C can be inferred as the brother or the sister of B, then A can be inferred as the sister of B.
</Rules>

<Example>
Narrative: [Alice] celebrated her birthday with her son [Ben]. [Chris] visited his sister [Alice] and her family. [David] played soccer with his cousin [Ben]. [Eve] baked a cake for her grandson [David].

Initila Fact:
isRelationOf(ben, son, alice) ::: [Alice] celebrated her birthday with her son [Ben].

Applying Rules Iteratively
Iteration 1
    Rule: relation(A, son, B) :- isRelationOf(A, son, C), relation(C, (husband;wife), B), B != A
    No applicable facts.

    Rule: relation(A, daughter, B) :- isRelationOf(A, daughter, C), relation(C, (husband;wife), B), B != A
    No applicable facts.

    Rule: relation(A, father, B) :- isRelationOf(A, grandfather, C), relation(C, (son;daughter), B), B != A
    No applicable facts.

    Rule: relation(A, mother, B) :- isRelationOf(A, grandmother, C), relation(C, (son;daughter), B), B != A
    No applicable facts.

    Rule: relation(A, father, B) :- isRelationOf(A, father, C), relation(C, (brother;sister), B), B != A
    No applicable facts.

    Rule: relation(A, mother, B) :- isRelationOf(A, mother, C), relation(C, (brother;sister), B), B != A
    No applicable facts.

    Rule: relation(A, uncle, B) :- isRelationOf(A, (brother;brother_in_law), C), relation(C, (father;mother), B), B != A
    No applicable facts.

    Rule: relation(A, aunt, B) :- isRelationOf(A, (sister;sister_in_law), C), relation(C, (father;mother), B), B != A
    No applicable facts.

    Rule: relation(A, nephew, B) :- isRelationOf(A, son, C), relation(C, (brother;sister;brother_in_law;sister_in_law), B), B != A
    No applicable facts.

    Rule: relation(A, niece, B) :- isRelationOf(A, daughter, C), relation(C, (brother;sister;brother_in_law;sister_in_law), B), B != A
    No applicable facts.

    Rule: relation(A, grandfather, B) :- isRelationOf(A, father, C), relation(C, (father;mother), B), B != A
    No applicable facts.

    Rule: relation(A, grandmother, B) :- isRelationOf(A, mother, C), relation(C, (father;mother), B), B != A
    No applicable facts.

    Rule: relation(A, grandson, B) :- isRelationOf(A, son, C), relation(C, (son;daughter), B), B != A
    No applicable facts.

    Rule: relation(A, granddaughter, B) :- isRelationOf(A, daughter, C), relation(C, (son;daughter), B), B != A
    No applicable facts.

    Rule: relation(A, father_in_law, B) :- isRelationOf(A, father, C), relation(C, (husband;wife), B), B != A
    No applicable facts.

    Rule: relation(A, mother_in_law, B) :- isRelationOf(A, mother, C), relation(C, (husband;wife), B), B != A
    No applicable facts.

    Rule: relation(A, son_in_law, B) :- isRelationOf(A, husband, C), relation(C, daughter, B), B != A
    No applicable facts.

    Rule: relation(A, daughter_in_law, B) :- isRelationOf(A, wife, C), relation(C, son, B), B != A
    No applicable facts.

    Rule: relation(A, brother_in_law, B) :- isRelationOf(A, husband, C), relation(C, sister, B), B != A
    No applicable facts.

    Rule: relation(A, sister_in_law, B) :- isRelationOf(A, wife, C), relation(C, brother, B), B != A
    No applicable facts.

    Rule: relation(A, husband, B) :- isRelationOf(B, wife, A), B != A
    No applicable facts.

    Rule: relation(A, wife, B) :- isRelationOf(B, husband, A), B != A
    No applicable facts.

    Rule: relation(A, husband, B) :- isRelationOf(A, father, C), relation(C, (daughter;son), B), B != A
    No applicable facts.

    Rule: relation(A, wife, B) :- isRelationOf(A, mother, C), relation(C, (daughter;son), B), B != A
    No applicable facts.

    Rule: relation(A, brother, B) :- isRelationOf(A, uncle, C), relation(C, (son;daughter), B), B != A
    No applicable facts.

    Rule: relation(A, sister, B) :- isRelationOf(A, aunt, C), relation(C, (son;daughter), B), B != A
    No applicable facts.

    Rule: relation(A, brother, B) :- isRelationOf(A, son, C), relation(C, (father;mother), B), B != A
    No applicable facts.

    Rule: relation(A, sister, B) :- isRelationOf(A, daughter, C), relation(C, (father;mother), B), B != A
    No applicable facts.

    Rule: relation(A, brother, B) :- isRelationOf(A, brother, C), relation(C, (brother;sister), B), B != A
    No applicable facts.

    Rule: relation(A, sister, B) :- isRelationOf(A, sister, C), relation(C, (brother;sister), B), B != A
    No applicable facts.

New Fact Derived
    isRelationOf(chris, brother, alice): Chris is the brother of Alice.

Iteration 2
    Rule: relation(A, son, B) :- isRelationOf(A, brother, C), relation(C, (son;daughter), B), B != A
        relation(chris, son, alice): Chris is the son of Alice.

New Fact Derived
    isRelationOf(chris, son, alice): Chris is the son of Alice.

Iteration 3
    Rule: relation(A, son, B) :- isRelationOf(A, brother, C), relation(C, (son;daughter), B), B != A
        relation(david, grandson, alice): David is the grandson of Alice.
        relation(eve, grandmother, ben): Eve is the grandmother of Ben.

New Facts Derived
    isRelationOf(david, grandson, alice): David is the grandson of Alice.
    isRelationOf(eve, grandmother, ben): Eve is the grandmother of Ben.

Iteration 4
    Rule: relation(A, mother, B) :- isRelationOf(A, grandmother, C), relation(C, (son;daughter), B), B != A
        relation(eve, mother, alice): Eve is the mother of Alice.

New Fact Derived
    isRelationOf(eve, mother, alice): Eve is the mother of Alice.

Iteration 5
    Rule: relation(A, grandmother, B) :- isRelationOf(A, mother, C), relation(C, (father;mother), B), B != A
        relation(eve, grandmother, chris): Eve is the grandmother of Chris.

New Fact Derived
    isRelationOf(eve, grandmother, chris): Eve is the grandmother of Chris.

Iteration 6
    Rule: relation(A, uncle, B) :- isRelationOf(A, brother, C), relation(C, (father;mother), B), B != A
        relation(david, uncle, ben): David is the uncle of Ben.

New Fact Derived
    isRelationOf(david, uncle, ben): David is the uncle of Ben.

Final Set of Inferred Facts
1. isRelationOf(ben, son, alice): Ben is the son of Alice.
2. isRelationOf(chris, brother, alice): Chris is the brother of Alice.
3. isRelationOf(chris, son, alice): Chris is the son of Alice.
4. isRelationOf(david, grandson, alice): David is the grandson of Alice.
5. isRelationOf(eve, grandmother, ben): Eve is the grandmother of Ben.
6. isRelationOf(eve, mother, alice): Eve is the mother of Alice.
7. isRelationOf(eve, grandmother, chris): Eve is the grandmother of Chris.
8. isRelationOf(david, uncle, ben): David is the uncle of Ben.

Output:
isRelationOf(ben, son, alice): Ben is the son of Alice.
isRelationOf(chris, brother, alice): Chris is the brother of Alice.
isRelationOf(chris, son, alice): Chris is the son of Alice.
isRelationOf(david, grandson, alice): David is the grandson of Alice.
isRelationOf(eve, grandmother, ben): Eve is the grandmother of Ben.
isRelationOf(eve, mother, alice): Eve is the mother of Alice.
isRelationOf(eve, grandmother, chris): Eve is the grandmother of Chris.
isRelationOf(david, uncle, ben): David is the uncle of Ben.
</Example>

Input:
Narrative: {narrative}

Initial Fact:
{initial_fact}

Output:
"""

resolution_refutation_score_prompt="""<Instructions>
Conduct resolution refutation on the followoing set of inferred facts and narrative.
Please score the resolution refutation in terms of how consistent the inferred facts are with the given narrative. 
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
isRelationOf(ben, son, alice): Ben is the son of Alice.
isRelationOf(chris, brother, alice): Chris is the brother of Alice.
isRelationOf(chris, son, alice): Chris is the son of Alice.
isRelationOf(david, grandson, alice): David is the grandson of Alice.
isRelationOf(eve, grandmother, ben): Eve is the grandmother of Ben.
isRelationOf(eve, mother, alice): Eve is the mother of Alice.
isRelationOf(eve, grandmother, chris): Eve is the grandmother of Chris.
isRelationOf(david, uncle, ben): David is the uncle of Ben.

Narrative: [Alice] celebrated her birthday with her son [Ben]. [Chris] visited his sister [Alice] and her family. [David] played soccer with his cousin [Ben]. [Eve] baked a cake for her grandson [David].

Step 1: Negate the Inferred Facts
1. ¬isRelationOf(ben, son, alice): Ben is not the son of Alice.
2. ¬isRelationOf(chris, brother, alice): Chris is not the brother of Alice.
3. ¬isRelationOf(chris, son, alice): Chris is not the son of Alice.
4. ¬isRelationOf(david, grandson, alice): David is not the grandson of Alice.
5. ¬isRelationOf(eve, grandmother, ben): Eve is not the grandmother of Ben.
6. ¬isRelationOf(eve, mother, alice): Eve is not the mother of Alice.
7. ¬isRelationOf(eve, grandmother, chris): Eve is not the grandmother of Chris.
8. ¬isRelationOf(david, uncle, ben): David is not the uncle of Ben.

Step 2: Convert All Statements into CNF (Conjunctive Normal Form)
All Statements are in CNF

Step 3: Apply Resolution
We will check for consistency by seeing if the inferred facts can coexist without contradiction:

1. Ben and Alice:
    - Narrative: "Alice celebrated her birthday with her son Ben."
    - Inferred: isRelationOf(ben, son, alice)
    - Consistent.

2. Chris and Alice:
    - Narrative: "Chris visited his sister Alice."
    - Inferred: isRelationOf(chris, brother, alice)
    - Consistent.

3. Chris and Alice (conflicting role):
    - Inferred: isRelationOf(chris, son, alice)
    - Contradicts isRelationOf(chris, brother, alice)
    - Inconsistent.

4. David and Alice:
    - Inferred: isRelationOf(david, grandson, alice)
    - Narrative does not directly state this but doesn't contradict it either.
    - Consistent.

5. Eve and Ben:
    - Narrative: "Eve baked a cake for her grandson David."
    - Inferred: isRelationOf(eve, grandmother, ben) and isRelationOf(eve, grandmother, chris)
    - Consistent if David is Alice's son (implying Eve is Alice's mother)
    - Consistent.

6. Eve and Alice:
    - Narrative consistency with inferred: isRelationOf(eve, mother, alice)
    - Consistent.

7. David and Ben:
    - Narrative: "David played soccer with his cousin Ben."
    - Inferred: isRelationOf(david, uncle, ben)
    - Contradictory roles if David is Ben's cousin
    - Inconsistent.

Step 4: Derive Contradiction
By identifying inconsistent relationships:
    - Chris as both brother and son of Alice: Contradiction.
    - David as both uncle and cousin to Ben: Contradiction.

Final Consistency Score
Output: Given the contradictions identified, we observe that the inferred facts are not fully consistent with the narrative. At least two inferred relationships directly contradict each other or the narrative. <Consistency>4</Consistency>
</Example>

Facts: {facts}

Narrative: {narrative}
"""

aggregate_prompt = """<Instructions>
Perform aggregation on the two sets of facts to generate a new set of facts.

The format of the string should be: 
Some logic program: Some description text.
Some logic program: Some description text.
Some logic program: Some description text.
...
<Instructions>

Combine the following strings into a single string:
Set 1:
{input1}

Set 2:
{input2}

New set:
"""

reasoning_prompt_got = """<Instructions>
Given the following narrative and goal statement, determine if the goal statement is True or False. Use the program to help you determine if the goal is True or False.
</Instructions.

<Approach>
To accurately answer the question, follow these steps:
1. Carefully read and understand the given narrative. Identify key relationships with the subjects mentioned.
2. Pay attention to any terms that are defined or explained within the narrative itself.
3. Use the inferred facts to help draw out your conclusion. The inferred facts should give you clues about the subjects's relationships.
</Approach>

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

Inferred Facts:
isRelationOf(alice, daughter, eve): Alice is the daughter of Eve.
isRelationOf(ben, son, alice): Ben is the son of Alice.
isRelationOf(chris, son, alice): Chris is the son of Alice.
isRelationOf(eve, grandmother, ben): Eve is the grandmother of Ben.
isRelationOf(eve, grandmother, chris): Eve is the grandmother of Chris.
isRelationOf(david, grandson, eve): David is the grandson of Eve.
isRelationOf(david, uncle, ben): David is the uncle of Ben.
isRelationOf(david, uncle, chris): David is the uncle of Chris.
isRelationOf(chris, brother, ben): Chris is the brother of Ben.
isRelationOf(david, brother, alice): David is the brother of Alice.

Goal: relation(chris, uncle, david)

Inference: From the program, we know that Ben is Alice's son. Chris is Alice's brother, which makes Chris Ben's uncle. David is Ben's cousin. This implies that David's parent is a sibling of Ben's parent (Alice). Since Chris is Alice's brother, Chris is also the uncle of David because the uncle relationship extends to the children of siblings. Therefore, the goal statement relation(chris, uncle, david) is True. 
Output: True

</Example>

Narrative: {narrative}

Program:
{program}

Inferred Facts:
{aggregated_facts}

Goal: {goal}

Output:
"""