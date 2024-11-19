import re

class UnificationError(Exception):
    pass

def is_variable(x):
    """Check if x is a variable (a lowercase string)."""
    return isinstance(x, str) and x[0].islower()

def unify(x, y, subst={}):
    """Attempt to unify two terms x and y, given the current substitution."""
    
    # Case 1: If both terms are the same, nothing needs to be done.
    if x == y:
        return subst
    
    # Case 2: If x is a variable, bind x to y (if possible).
    if is_variable(x):
        return unify_variable(x, y, subst)
    
    # Case 3: If y is a variable, bind y to x (if possible).
    if is_variable(y):
        return unify_variable(y, x, subst)
    
    # Case 4: If both terms are compound (lists, tuples), try to unify their components.
    if isinstance(x, tuple) and isinstance(y, tuple):
        if len(x) != len(y):
            raise UnificationError(f"Cannot unify {x} and {y} with different arity")
        for xx, yy in zip(x, y):
            subst = unify(xx, yy, subst)
        return subst
    
    # Case 5: If we reach here, the terms cannot be unified.
    raise UnificationError(f"Cannot unify {x} and {y}")

def unify_variable(var, term, subst):
    """Unify a variable with a term."""
    
    # Check if the variable is already in the substitution.
    if var in subst:
        return unify(subst[var], term, subst)
    
    # Ensure that we do not create a circular dependency.
    if term == var:
        return subst
    
    # Add the substitution (variable -> term) to the substitution map.
    new_subst = subst.copy()
    new_subst[var] = term
    return new_subst

def parse_term(term_str):
    """Parse a string term into a Python object (e.g., tuple or string)."""
    # Remove spaces and handle nested terms
    term_str = term_str.strip()
    
    if term_str[0] == '(' and term_str[-1] == ')':
        # This is a compound term of the form f(...).
        term_str = term_str[1:-1]  # Strip the surrounding parentheses
        terms = split_terms(term_str)
        return tuple(parse_term(t) for t in terms)
    elif term_str.isdigit():
        # This is a simple integer
        return int(term_str)
    else:
        # If it's a variable (e.g., X, Y), return the variable name
        return term_str

def split_terms(term_str):
    """Split a term string by commas, respecting nested parentheses."""
    terms = []
    depth = 0
    start = 0
    for i, c in enumerate(term_str):
        if c == ',' and depth == 0:
            terms.append(term_str[start:i].strip())
            start = i + 1
        elif c == '(':
            depth += 1
        elif c == ')':
            depth -= 1
    terms.append(term_str[start:].strip())
    return terms

def get_user_input():
    """Get user input for two terms and parse them."""
    print("Enter the first term:")
    term1_str = input().strip()
    print("Enter the second term:")
    term2_str = input().strip()
    
    # Parse the terms into Python objects
    term1 = parse_term(term1_str)
    term2 = parse_term(term2_str)
    
    return term1, term2

def display_substitutions(subst):
    """Display the variable substitutions in a readable format."""
    for var, value in subst.items():
        print(f"{var} = {value}")

# Main function to unify user input terms
def main():
    term1, term2 = get_user_input()
    
    try:
        result = unify(term1, term2)
        print("Unification successful! Resulting substitution:")
        display_substitutions(result)
    except UnificationError as e:
        print(e)

# Run the main function
if __name__ == "__main__":
    main()
