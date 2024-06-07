# Datasets

## FOLIO

### Reasoning Type:

**Deductive Reasoning:** The primary reasoning type involved in the FOLIO dataset is deductive reasoning. The model needs to derive specific conclusions from the premises. For example, if the premise states "All birds can fly" and the hypothesis is "A robin can fly," the model needs to deduce that the hypothesis is true based on the premise.

**Sample:**

```
{
    "id": "FOLIO_dev_0",
    "context": "If people perform in school talent shows often, then they attend and are very engaged with school events. People either perform in school talent shows often or are inactive and disinterested members of their community. If people chaperone high school dances, then they are not students who attend the school. All people who are inactive and disinterested members of their community chaperone high school dances. All young children and teenagers who wish to further their academic careers and educational opportunities are students who attend the school. Bonnie either both attends and is very engaged with school events and is a student who attends the school, or she neither attends and is very engaged with school events nor is a student who attends the school.",
    "question": "Based on the above information, is the following statement true, false, or uncertain? Bonnie performs in school talent shows often.",
    "answer": "C",
    "options": [
        "A) True",
        "B) False",
        "C) Uncertain"
    ],
    "raw_logic_programs": [
        "Predicates:\nPerform(x) ::: x performs in school talent shows often.\nAttend(x) ::: x attends and is very engaged with school events.\nInactive(x) ::: x is an inactive and disinterested member of their community.\nChaperone(x) ::: x chaperones high school dances.\nStudent(x) ::: x is a student who attends the school.\nYoung(x) ::: x is a young child or teenager who wishes to further their academic careers and educational opportunities.\nPremises:\n∀x (Perform(x) → Attend(x)) ::: If people perform in school talent shows often, then they attend and are very engaged with school events.\n∀x (Perform(x) ⊕ Inactive(x)) ::: People either perform in school talent shows often or are inactive and disinterested members of their community.\n∀x (Chaperone(x) → ¬Student(x)) ::: If people chaperone high school dances, then they are not students who attend the school.\n∀x (Inactive(x) → Chaperone(x)) ::: All people who are inactive and disinterested members of their community chaperone high school dances.\n∀x (Young(x) → Student(x)) ::: All young children and teenagers who wish to further their academic careers and educational opportunities are students who attend the school.\n(Attend(bonnie) ∧ Student(bonnie)) ⊕ ¬(Attend(bonnie) ∨ Student(bonnie)) ::: Bonnie either both attends and is very engaged with school events and is a student who attends the school, or she neither attends and is very engaged with school events nor is a student who attends the school.\nConclusion:\nPerform(bonnie) ::: Bonnie performs in school talent shows often."
    ]
},
```

## CLUTTR

### Reasoning Type:

**Inductive Reasoning:** The CLUTTR dataset primarily involves inductive reasoning, where the model must generalize from specific instances to form broader conclusions. For instance, if the narrative includes statements like "John is older than Mary" and "Mary is older than Tom," the model must infer the transitive relation that "John is older than Tom."
**Compositional Reasoning:** Beyond simple inductive reasoning, CLUTTR also requires compositional reasoning, where multiple pieces of information need to be integrated to arrive at the correct answer to a query.

**Sample:**

```
{
    "id": 0,
    "body_text": "[Jenny] spent a great day shopping with her daughter, [Mary]. [Kelley] took her sister, [Mary], out to dinner for her birthday. [Kelley] watched a golf tournament with her aunt [April]. [April] had picked her daughter [Melba] out the cutest new dress to wear on her birthday.",
    "world_model": [
        "family_relation_rules"
    ],
    "goal": "relation(melba, niece, jenny)",
    "label": true,
    "program": [
        {
            "statement": "isRelationOf(melba, daughter, april).",
            "description": "[April] had picked her daughter [Melba] out the cutest new dress to wear on her birthday."
        },
        {
            "statement": "isRelationOf(april, aunt, kelley).",
            "description": "[Kelley] watched a golf tournament with her aunt [April]."
        },
        {
            "statement": "isRelationOf(mary, daughter, jenny).",
            "description": "[Jenny] spent a great day shopping with her daughter, [Mary]."
        },
        {
            "statement": "isRelationOf(kelley, sister, mary).",
            "description": "[Kelley] took her sister, [Mary], out to dinner for her birthday."
        }
    ]
},
```
