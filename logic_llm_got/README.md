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
    "context": "[Jenny] spent a great day shopping with her daughter, [Mary]. [Kelley] took her sister, [Mary], out to dinner for her birthday. [Kelley] watched a golf tournament with her aunt [April]. [April] had picked her daughter [Melba] out the cutest new dress to wear on her birthday.",
    "goal": "relation(melba, niece, jenny)",
    "label": true,
    "raw_logic_programs": [
      "Predicates:\nparent(X, Y) ::: X is a parent of Y.\nsibling(X, Y) ::: X is a sibling of Y.\naunt(X, Y) ::: X is an aunt of Y.\nniece(X, Y) ::: X is a niece of Y.\n\nFacts: \nparent(jenny, mary) ::: jenny is a parent of mary.\nsibling(mary, kelley) ::: mary is a sibling of kelley.\naunt(april, kelley) ::: april is an aunt of kelley.\nparent(april, melba) ::: april is a parent of melba.\n\nRules:\n∀X,Y (spent_day_shopping(X,Y) ⇒ parent(X,Y)) ::: If X spent a day shopping with Y, then X is a parent of Y.\n∀X,Y (took_out_to_dinner(X,Y) ⇒ sibling(X,Y)) ::: If X took Y out to dinner, then X and Y are siblings.\n∀X,Y (watched_golf_with(X,Y) ⇒ aunt(X,Y)) ::: If X watched a golf tournament with Y, then X is an aunt of Y.\n∀X,Y (picked_out_dress_for(X,Y) ⇒ parent(X,Y)) ::: If X picked out a dress for Y, then X is a parent of Y.\n\nQuery:\nniece(melba, jenny) ::: melba is a niece of jenny."
    ]
},
```

## abductivePerson

**Sample:**

```
{
    "id": "Abduction-Person-1332-Q1",
    "context": "All people that are short, are thin, and are wealthy, are also little. Charlie is small. All people that are thin, are short, and are small, are little. People that are poor, are dull, and are sad, are also rough. Gary is imperfect. If something is heavy, is huge, and is high, it is also big. Gary is dull. Charlie is tiny. Erin is strong. All things that are smart, are sad, and are high, are also little. Fiona is smart. Gary is sad. All things that are kind, are wealthy, and are smart, are also clever. If a person is heavy, is thin, and is dull, that person is clever. If something is kind, is small, and is huge, then it is also rough. Fiona is wealthy. Things that are sad, are kind, and are smart, are also clever. Charlie is short. Things that are short, are wealthy, and are poor, are big. If a person is high, is small, and is huge, then that person is also big. Erin is heavy. Erin is huge. All people that are poor, are dull, and are heavy, are rough.",
    "question": "Erin is big.",
    "label": "Erin is high.",
    "raw_logic_programs": [
        "Predicates:\nShort(x): x is short\nThin(x): x is thin\nWealthy(x): x is wealthy\nLittle(x): x is little\nSmall(x): x is small\nPoor(x): x is poor\nDull(x): x is dull\nRough(x): x is rough\nImperfect(x): x is imperfect\nHeavy(x): x is heavy\nHuge(x): x is huge\nHigh(x): x is high\nBig(x): x is big\nTiny(x): x is tiny\nStrong(x): x is strong\nSmart(x): x is smart\nKind(x): x is kind\nClever(x): x is clever\n\nFacts:\nSmall(Charlie)\nImperfect(Gary)\nDull(Gary)\nTiny(Charlie)\nStrong(Erin)\nSmart(Fiona)\nSad(Gary)\nWealthy(Fiona)\nShort(Charlie)\nHeavy(Erin)\nHuge(Erin)\n\nRules:\n∀x(Short(x) ∧ Thin(x) ∧ Wealthy(x) → Little(x))\n∀x(Thin(x) ∧ Short(x) ∧ Small(x) → Little(x))\n∀x(Poor(x) ∧ Dull(x) ∧ Sad(x) → Rough(x))\n∀x(Heavy(x) ∧ Huge(x) ∧ High(x) → Big(x))\n∀x(Smart(x) ∧ Sad(x) ∧ High(x) → Little(x))\n∀x(Kind(x) ∧ Wealthy(x) ∧ Smart(x) → Clever(x))\n∀x(Heavy(x) ∧ Thin(x) ∧ Dull(x) → Clever(x))\n∀x(Kind(x) ∧ Small(x) ∧ Huge(x) → Rough(x))\n∀x(Sad(x) ∧ Kind(x) ∧ Smart(x) → Clever(x))\n∀x(Short(x) ∧ Wealthy(x) ∧ Poor(x) → Big(x))\n∀x(High(x) ∧ Small(x) ∧ Huge(x) → Big(x))\n∀x(Poor(x) ∧ Dull(x) ∧ Heavy(x) → Rough(x))\n\nQuery:\nBig(Erin)"
    ],
    "QCat": "0"
},
```
