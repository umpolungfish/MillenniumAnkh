#!/usr/bin/env python3
"""Replace descent_even_coeff and its callers with standalone lemmas."""

with open('Imscribing/Classical/Solitary10.lean', 'r') as f:
    content = f.read()

# Find positions
import re

# Find descent_even_coeff
m = re.search(r'/-- A general descent lemma.*?lemma descent_even_coeff.*?lt_irrefl _ h_contra\n', content, re.DOTALL)
if m:
    print(f"descent_even_coeff: {m.start()}-{m.end()}")
else:
    print("descent_even_coeff NOT FOUND!")
    # Try to find just the lemma
    m2 = re.search(r'lemma descent_even_coeff', content)
    if m2:
        print(f"  starts at {m2.start()}")

# Find descent_332_465 
m332 = re.search(r'/-- Special case: 332.*?lemma descent_332_465.*?\n', content, re.DOTALL)
if m332:
    print(f"descent_332_465 (first): {m332.start()}-{m332.end()}")
    
m41872 = re.search(r'/-- Special case: 41872.*?lemma descent_41872_51305.*?\n', content, re.DOTALL)
if m41872:
    print(f"descent_41872_51305 (first): {m41872.start()}-{m41872.end()}")

# Find theorem ten_is_solitary
m_theorem = re.search(r'theorem ten_is_solitary', content)
if m_theorem:
    print(f"theorem: {m_theorem.start()}")
