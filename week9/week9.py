#week 9
# Install dependencies
!sudo apt update
!sudo apt install swi-prolog -y
!pip install pyswip

from pyswip import Prolog

# Initialize Prolog engine
prolog = Prolog()

# Knowledge base
# a. If something is food, John likes it
prolog.assertz("likes(john, X) :- food(X)")

# b. Apple and vegetables are food
prolog.assertz("food(apple)")
prolog.assertz("food(vegetables)")

# c. Anything someone eats and is not killed is food
prolog.assertz("food(Z) :- eats(Y, Z), not_killed(Y)")

# d. Anil eats peanuts
prolog.assertz("eats(anil, peanuts)")

# e. Anil is alive
prolog.assertz("alive(anil)")

# f. If someone is alive, they are not killed
prolog.assertz("not_killed(X) :- alive(X)")

# Query to prove: John likes peanuts
query = "likes(john, peanuts)"

# Check if the query can be proven
result = list(prolog.query(query))

# Output the result
if result:
    print("Proven: John likes peanuts.")
else:
    print("Cannot prove that John likes peanuts.")
week 8 class ForwardChaining:
    def __init__(self):
        self.facts = set()  # Store known facts
        self.rules = []     # Store rules as (premise, conclusion)

    def add_fact(self, fact):
        """Add a fact to the knowledge base."""
        self.facts.add(fact)

    def add_rule(self, premise, conclusion):
        """Add a rule to the knowledge base."""
        self.rules.append((premise, conclusion))

    def apply_rule(self, rule):
        """Apply a rule and derive new facts."""
        premise, conclusion = rule
        if premise <= self.facts:  # Premise is a subset of facts
            self.facts.add(conclusion)  # Add the conclusion to the facts
            return True
        return False

    def forward_chain(self):
        """Perform forward chaining to derive new facts."""
        new_facts = True
        while new_facts:
            new_facts = False
            for rule in self.rules:
                if self.apply_rule(rule):
                    new_facts = True

    def prove_crime(self, person):
        """Check if a person is a criminal."""
        return ('Crime', person) in self.facts


# Initialize the forward chaining engine
fc = ForwardChaining()

# Facts
fc.add_fact(('American', 'Robert'))  # Robert is an American
fc.add_fact(('Sold', 'Robert', 'Missiles', 'A'))  # Robert sold missiles to Country A
fc.add_fact(('Hostile', 'A'))  # Country A is hostile

# Rule: If an American sells weapons to a hostile country, they are a criminal
fc.add_rule(
    {('American', 'X'), ('Sold', 'X', 'Missiles', 'Y'), ('Hostile', 'Y')},  # Premise
    ('Crime', 'X')  # Conclusion
)

# Perform forward chaining
fc.forward_chain()

# Check if Robert is a criminal
if fc.prove_crime('Robert'):
    print("Robert is not a criminal.")
else:
    print("Robert is a criminal.")