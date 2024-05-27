cluttr_io_prompt = """<Instructions>
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

cluttr_cot_prompt = """<Instruction>
Given the following narrative and goal statement, determine if the goal statement is True or False. Use the program to help you determine if the goal is True or False. Explain your inference.
</Instruction>

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

cluttr_fg_prompt = """<Instruction>
Given the following narrative and goal statement, determine if the goal statement is True or False. Your task is to perform forward chaining to determine if the conclusion is true or false. Print the entire Step-by-Step Foward Chaining Process exactly like the examples provided. DO NOT SKIP A SINGLE STEP!!!
</Instruction>

<Approach>
Print your response using this format only. Use the examples to help you with your formatting. Your response should look exactly like the examples. Do not add any changes to the formatting or writing style.
Initial Facts:
1. "Fact number 1"
2. "Fact number 2"
3. "Fact number 3"
...

Rules:
1. "Rule number 1"
2. "Rule number 2"
3. "Rule number 3"
...

Inference Process:
Applying Rules:
Rule 1: "Apply rule 1".
Rule 2: "Apply rule 2".
Rule 3: "Apply rule 3".
...

Deriving Relationships:
From the rules applied:
"The implied realtions using the applied rules."

Checking Goal:
"Your inference to check the goal based on derived realtionships."

Conclusion: "Your concluding statement."

Answer: "Your answer choice."
</Approach>

<Example>
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

Step-by-Step Foward Chaining:
Initial Facts:
1. isRelationOf(emma, daughter, olivia)
2. isRelationOf(sophia, niece, noah)
3. isRelationOf(liam, cousin, emma)
4. isRelationOf(sophia, granddaughter, isabella)

Rules:
1. If isRelationOf(X, daughter, Y) and isRelationOf(Z, niece, X), then relation(Z, brother, Y).
2. If isRelationOf(X, niece, Y) and isRelationOf(X, granddaughter, Z), then relation(Y, son, Z).
3. If isRelationOf(X, cousin, Y) and isRelationOf(Y, daughter, Z), then relation(X, sibling, Z).

Inference Process:
Applying Rules: 
Rule 1: We don't have a fact matching `isRelationOf(Z, niece, X)` where X is a daughter of Y. 
Rule 2: We don't have a direct fact for `isRelationOf(X, granddaughter, Z)` leading to a `relation(Y, son, Z)` involving Noah. 
Rule 3: Given `isRelationOf(liam, cousin, emma)` and `isRelation(emma, daughter, olivia)`, we can't derive `relation(liam, sibling, olivia)` directly.

Deriving Relationships:
From `isRelationOf(sophia, niece, noah)`:
If Sophia is Noah's nieve, Noah coulbe be a sibling to Sophia's parent.
`isRelationOf(sophia, granddaughter, isabella)` implies Sophia's parent is Isabella's child.
However, this does not directly connect Noah and Emma as siblings.
From `isRelationOf(liam, cousin, emma):
Cousin relationship implies Emma's parent and Liam's parent are siblings.
We know Emma's mother is Olivia.

Checkig Goal: 
We need to establish a direct relationship between Noah and Emma:
`isReltionOf(sophia, niece, noah)` indicates that Noah could be a sibling to Sophia's parent.
`isRelationOf(sophia, granddaughter, isabella)` shows Sophia's parents mother is Isabella.

Conclusion: We do not have sufficient information to establish that Noah and Emma are siblings. There is no rule application or derived fact directly linking Noah as the brother of Emma. Therefore, the goal statement "relation(noah, brother, emma)" is False. 

Answer: False
.....
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

Step-by-Step Foward Chaining:
Initial Facts:
1. isRelationOf(ben, son, alice)
2. isRelationOf(chris, brother, alice)
3. isRelationOf(david, cousin, ben)
4. isRelationOf(david, grandson, eve)

Rules:
1. If isRelationOf(X, son, Y) and isRelationOf(Z, brother, Y), then relation(Z, uncle, X).
2. If isRelationOf(X, grandson, Y) and isRelationOf(Y, mother, Z), then isRelationOf(X, son, Z).
3. If isRelationOf(X, cousin, Y) and isRelationOf(Y, son, Z), then relation(X, nephew, Z).

Inference Process:
Applying Rules:
Rule 1: Given `isRelationOf(ben, son, alice)` and `isRelationOf(chris, brother, alice)`, we can derive: `relation(chris, uncle, ben)`.
Rule 2: We don't have a direct fact for `isRelationOf(david, grandson, eve)` leading to a `isRelationOf(david, son, Z)` involving another family memeber.
Rule 3: We don't have a direct fact for `isRelationOf(david, cousin, ben)` leading to a `relation(david, nephew, Z)` involving another family member.

Deriving Relationships:
From `isRelationOf(david, cousin, ben)`:
If David is Ben's cousin, it implies that David's parent is a sibling of Ben's parent.
Given `isRelationOf(ben, son, alice)`, Ben is the son of Alice.
`relation(chris, uncle, ben)` indicates Chris is Alice's brother.

Checking Goal: 
We need to establish a direct relationship between Chris and David:
`relation(chris, uncle, ben)` and `isRelationOf(david, cousin, ben)`:
If Ben is Alice's son and David is Ben's cousin, then David's parent must be Alice's sibling.
Since Chris is Alice's brother, Chris is David's uncle.

Conclusion: Based on the derived facts and inference, we can conclude that `realation(chris, uncle, david) is true. Therefore, the goal statement "relation(chris, uncle, david)" is True.

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

Step-by-Step Foward Chaining:
Initial Facts:
1. isRelationOf(ethan, son, ava)
2. isRelationOf(lucas, brother, mia)
3. isRelationOf(lucas, cousin, ethan)
4. isRelationOf(mia, granddaughter, sophia)

Rules:
1. If isRelationOf(X, son, Y) and isRelationOf(Z, brother, Y), then relation(Z, uncle, X).
2. If isRelationOf(X, brother, Y) and isRelationOf(Y, granddaughter, Z), then relation(X, grandson, Z).
3. If isRelationOf(X, cousin, Y) and isRelationOf(Y, son, Z), then relation(X, nephew, Z).

Inference Process
Applying Rules:
Rule 1: We don't have a fact matching `isRelationOf(Z, brother, Y)` where Y is a son of someone.
Rule 2: Give `isRelationOf(lucas, brother, mia)` and `isRelationOf(mia, granddaughter, sophia)`, we can derive: `relation(lucas, grandson, sophia)`.
Rule 3: We don't have a direct fact for `isRelationOf(lucas, cousin, ethan)` leading to a `relation(X, nephew, Z)` involving another family member.

Deriving Relationships:
From `isRelationOf(lucas, cousin, ethan)`:
If Lucas is Ethan's cousin, it implies that Lucas's parent is a sibling of Ethan's parent.
Given `isRelationOf(ethan, son, ava)`, Ethan is the son of Ava.
However, this does not directly connect Ethan and Sophia as siblings.

Checking Goal: 
We need to establish a direct relationship between Ethan and Sophia:
`isRelationOf(mia, ganddaughter, sophia)` indicates that Mia is Sophia's granddaughter.
`isRelationOf(lucas, brother, mia)` shows that Lucas is Mia's brother.
Therefore, Lucas is also Sophia's grandson through Mia.
Given `relation(lucas, grandson, sophia)`, it further confirms Lucas's relationship with Sophia but does not establish Ethan's direct relationship with Sophia.

Conclusion: We do not have sufficient information to establish that Ethan and Sophia are siblings. There is no rule application or derived fact directly linking Ethan as the brother of Sophia. Therefore, the goal statement "relation(ethan, brother, sophia)" is False.

Answer: False
</Example>

Narrative: {body_text}

Program:
{program}

Goal: {goal}

Step-by-Step Forward Chaining:
"""