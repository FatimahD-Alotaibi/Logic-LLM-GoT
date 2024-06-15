cluttr_prompt_io = """<Instructions>
Given the following narrative and goal statement, determine if the goal statement is True or False. Use the program to help you determine if the goal is True or False.
</Instructions>

<Example>
Narrative: [Alice] celebrated her birthday with her son [Ben]. [Chris] visited his sister [Alice] and her family. [David] played soccer with his cousin [Ben]. [Eve] baked a cake for her grandson [David].

Raw Logic Programs:
Predicates:
parent(X, Y) ::: X is a parent of Y.
sibling(X, Y) ::: X is a sibling of Y.
cousin(X, Y) ::: X is a cousin of Y.
grandparent(X, Y) ::: X is a grandparent of Y.
uncle(X, Y) ::: X is an uncle of Y.
Facts:
parent(alice, ben) ::: alice is a parent of ben.
sibling(alice, chris) ::: alice is a sibling of chris.
cousin(david, ben) ::: david is a cousin of ben.
grandparent(eve, david) ::: even is a grandparent of david.
Rules:
∀X, Y(celebrated_with(X, Y) ⇒ parent(X, Y)) ::: If X celebrated their birthday with Y, then X is a parent of Y.
∀X, Y(visited(X, Y) ⇒ sibling(X, Y)) ::: If X visited Y, then X and Y are siblings. 
∀X, Y(played_with(X, Y) ⇒ cousin(X, Y)) ::: If X played soccer with Y, then X and Y are cousins.
∀X, Y(baked_for(X, Y) ⇒ grandparent(X, Y)) ::: If X baked a cake for Y, then X is a grandparent of Y.
Query:
uncle(chris, david) ::: chris is an uncle of david.

Goal: relation(chris, uncle, david)

Answer: True
</Example>

Narrative: {narrative}

Raw Logic Programs:
{raw_logic_programs}

Goal: {goal}

Output: 
"""

cluttr_prompt_cot = """<Instructions>
Given the following narrative and goal statement, determine if the goal statement is True or False. Use the program to help you determine if the goal is True or False. Explain your inference.
</Instructions>

<Approach>
When printing your response, you should follow the EXACT same format as the examples provided. DO NOT USE ANY OTHER FORMAT!!!
</Approach>

<Example>
Narrative: [Alice] celebrated her birthday with her son [Ben]. [Chris] visited his sister [Alice] and her family. [David] played soccer with his cousin [Ben]. [Eve] baked a cake for her grandson [David].

Raw Logic Programs:
Predicates:
parent(X, Y) ::: X is a parent of Y.
sibling(X, Y) ::: X is a sibling of Y.
cousin(X, Y) ::: X is a cousin of Y.
grandparent(X, Y) ::: X is a grandparent of Y.
uncle(X, Y) ::: X is an uncle of Y.
Facts:
parent(alice, ben) ::: alice is a parent of ben.
sibling(alice, chris) ::: alice is a sibling of chris.
cousin(david, ben) ::: david is a cousin of ben.
grandparent(eve, david) ::: even is a grandparent of david.
Rules:
∀X, Y(celebrated_with(X, Y) ⇒ parent(X, Y)) ::: If X celebrated their birthday with Y, then X is a parent of Y.
∀X, Y(visited(X, Y) ⇒ sibling(X, Y)) ::: If X visited Y, then X and Y are siblings. 
∀X, Y(played_with(X, Y) ⇒ cousin(X, Y)) ::: If X played soccer with Y, then X and Y are cousins.
∀X, Y(baked_for(X, Y) ⇒ grandparent(X, Y)) ::: If X baked a cake for Y, then X is a grandparent of Y.
Query:
uncle(chris, david) ::: chris is an uncle of david.

Goal: relation(chris, uncle, david)

Inference: From the program, we know that Ben is Alice's son. Chris is Alice's brother, which makes Chris Ben's uncle. David is Ben's cousin. This implies that David's parent is a sibling of Ben's parent (Alice). Since Chris is Alice's brother, Chris is also the uncle of David because the uncle relationship extends to the children of siblings. Therefore, the goal statement relation(chris, uncle, david) is True. Output: True
</Example>
Narrative: {narrative}

Program:
{raw_logic_programs}

Goal: {goal}

Reasoning: 
"""

got_split_prompt = """<Instructions>
Split the following Facts from the input text into individual sentences. Output each sentence in the following format without additional text or thoughts. DO NOT Predicates or Query!!!
{{
    "Initial Fact 1": "Fact 1... ::: description text...",
    "Initial Fact 2": "Fact 2... ::: description text...",
    "Initial Fact 3": "Fact 3... ::: description text...",
    ...
}}
</Instructions>

<Example>
Raw Logic Programs:
Predicates:
parent(X, Y) ::: X is a parent of Y.
sibling(X, Y) ::: X is a sibling of Y.
cousin(X, Y) ::: X is a cousin of Y.
grandparent(X, Y) ::: X is a grandparent of Y.
uncle(X, Y) ::: X is an uncle of Y.
Facts:
parent(alice, ben) ::: alice is a parent of ben.
sibling(alice, chris) ::: alice is a sibling of chris.
cousin(david, ben) ::: david is a cousin of ben.
grandparent(eve, david) ::: even is a grandparent of david.
Rules:
∀X, Y(celebrated_with(X, Y) ⇒ parent(X, Y)) ::: If X celebrated their birthday with Y, then X is a parent of Y.
∀X, Y(visited(X, Y) ⇒ sibling(X, Y)) ::: If X visited Y, then X and Y are siblings. 
∀X, Y(played_with(X, Y) ⇒ cousin(X, Y)) ::: If X played soccer with Y, then X and Y are cousins.
∀X, Y(baked_for(X, Y) ⇒ grandparent(X, Y)) ::: If X baked a cake for Y, then X is a grandparent of Y.
Query:
uncle(chris, david) ::: chris is an uncle of david.

Output: 
{{
    "Initial Fact 1": "parent(alice, ben) ::: alice is a parent of ben.",
    "Initial Fact 2": "sibling(alice, chris) ::: alice is a sibling of chris.",
    "Initial Fact 3": "cousin(david, ben) ::: david is a cousin of ben.",
    "Initial Fact 4": "grandparent(eve, david) ::: even is a grandparent of david.",
}}
</Example>

Raw Logic Programs:
{raw_logic_programs}

Output:
"""



infer_facts_prompt = """<Instructions>
Given a narrative prompt, an initial fact and a set of logical rules, derive all possible inferred facts. Apply each rule iteratively until no more new conclusions can be drawn. Provide the inferred facts in logical format, along with their descriptions.
</Instructions>

<Approach>
1. Start with the initial fact and the narrative prompt.
2. Apply each rule to the current set of facts.
3. If a new fact is derived, add it to the set of known facts.
4. Repeat the process until no new facts can be derived.
5. Present the final set of inferred facts in logical format with descriptions.
<Approach>

<Example>
Rules:
∀X, Y(celebrated_with(X, Y) ⇒ parent(X, Y)) ::: If X celebrated their birthday with Y, then X is a parent of Y.
∀X, Y(visited(X, Y) ⇒ sibling(X, Y)) ::: If X visited Y, then X and Y are siblings. 
∀X, Y(played_with(X, Y) ⇒ cousin(X, Y)) ::: If X played soccer with Y, then X and Y are cousins.
∀X, Y(baked_for(X, Y) ⇒ grandparent(X, Y)) ::: If X baked a cake for Y, then X is a grandparent of Y.

Narrative: [Alice] celebrated her birthday with her son [Ben]. [Chris] visited his sister [Alice] and her family. [David] played soccer with his cousin [Ben]. [Eve] baked a cake for her grandson [David].

Initial Fact: parent(alice, ben) ::: alice is a prent of ben.

Output:
parent(alice, ben) ::: alice is a parent of ben.
sibling(chris, alice) ::: chris is a sibling of alice.
cousin(david, ben) ::: david is a cousin of ben.
grandparent(eve, david) ::: eve is a grandparent of david.
</Example>

Rules:
{rules}

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
parent(alice, ben) ::: alice is a parent of ben.
sibling(chris, alice) ::: chris is a sibling of alice.
cousin(david, ben) ::: david is a cousin of ben.
grandparent(eve, david) ::: eve is a grandparent of david.

Narrative: [Alice] celebrated her birthday with her son [Ben]. [Chris] visited his sister [Alice] and her family. [David] played soccer with his cousin [Ben]. [Eve] baked a cake for her grandson [David].

Step 1: Negate the Inferred Facts:
    1. ¬parent(alice, ben)
    2. ¬sibling(chris, alice)
    3. ¬cousin(david, ben)
    4. ¬grandparent(eve, david)

Step 2: Convert All Statements into CNF:
Narrative in CNF
    1. celebrated_with(alice, ben)
    2. visited(chris, alice)
    3. played_with(david, ben)
    4. baked_for(eve, david)

Rules in CNF
    1. ∀X,Y(¬celebrated_with(X,Y) ∨ parent(X,Y))
    2. ∀X,Y(¬visited(X,Y) ∨ sibling(X,Y))
    3. ∀X,Y(¬played_with(X,Y) ∨ cousin(X,Y))
    4. ∀X,Y(¬baked_for(X,Y) ∨ grandparent(X,Y))

Step 3: Apply Resolution
Combine Narrative and Rules
1. celebrated_with(alice, ben) with ∀X,Y(¬celebrated_with(X,Y) ∨ parent(X,Y)):
    - From celebrated_with(alice, ben)
    - ¬celebrated_with(alice,ben) ∨ parent(alice,ben)
    - Resolves to parent(alice, ben)

2. visited(chris, alice) with ∀X,Y(¬visited(X,Y) ∨ sibling(X,Y)):
    - From visited(chris, alice)
    - ¬visited(chris,alice) ∨ sibling(chris,alice)
    - Resolves to sibling(chris, alice)
3. played_with(david, ben) with ∀X,Y(¬played_with(X,Y) ∨ cousin(X,Y)):
    - From played_with(david, ben)
    - ¬played_with(david,ben) ∨ cousin(david,ben)
    - Resolves to cousin(david, ben)
4. baked_for(eve, david) with ∀X,Y(¬baked_for(X,Y) ∨ grandparent(X,Y)):
    - From baked_for(eve, david)
    - ¬baked_for(eve,david) ∨ grandparent(eve,david)
    - Resolves to grandparent(eve, david)

Step 4: Derive Contradiction
Now we check if there are contradictions with the negated facts:
    1. ¬parent(alice, ben) contradicts with parent(alice, ben)
    2. ¬sibling(chris, alice) contradicts with sibling(chris, alice)
    3. ¬cousin(david, ben) contradicts with cousin(david, ben)
    4. ¬grandparent(eve, david) contradicts with grandparent(eve, david)

Output: <Consistency>10</Consistency>
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

Raw Logic Programs:
Predicates:
parent(X, Y) ::: X is a parent of Y.
sibling(X, Y) ::: X is a sibling of Y.
cousin(X, Y) ::: X is a cousin of Y.
grandparent(X, Y) ::: X is a grandparent of Y.
uncle(X, Y) ::: X is an uncle of Y.
Facts:
parent(alice, ben) ::: alice is a parent of ben.
sibling(alice, chris) ::: alice is a sibling of chris.
cousin(david, ben) ::: david is a cousin of ben.
grandparent(eve, david) ::: even is a grandparent of david.
Rules:
∀X, Y(celebrated_with(X, Y) ⇒ parent(X, Y)) ::: If X celebrated their birthday with Y, then X is a parent of Y.
∀X, Y(visited(X, Y) ⇒ sibling(X, Y)) ::: If X visited Y, then X and Y are siblings. 
∀X, Y(played_with(X, Y) ⇒ cousin(X, Y)) ::: If X played soccer with Y, then X and Y are cousins.
∀X, Y(baked_for(X, Y) ⇒ grandparent(X, Y)) ::: If X baked a cake for Y, then X is a grandparent of Y.
Query:
uncle(chris, david) ::: chris is an uncle of david.

Inferred Facts:
parent(alice, ben) ::: alice is a parent of ben.
sibling(chris, alice) ::: chris is a sibling of alice.
cousin(david, ben) ::: david is a cousin of ben.
grandparent(eve, david) ::: eve is a grandparent of david.

Output: True

</Example>

Narrative: {narrative}

Raw Logic Programs:
{raw_logic_programs}

Inferred Facts:
{aggregated_facts}

Goal: {goal}

Output:
"""