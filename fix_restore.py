#!/usr/bin/env python3
"""Restore all apply h_contra back to omega except the last one"""
with open("Imscribing/Primitives/OPN_2adic.lean", "r") as f:
    c = f.read()

# Count occurrences of "apply h_contra"
count = c.count("apply h_contra")
print(f"Found {count} occurrences of 'apply h_contra'")

# Replace all but the LAST occurrence
for i in range(count - 1):
    c = c.replace("apply h_contra", "omega", 1)

with open("Imscribing/Primitives/OPN_2adic.lean", "w") as f:
    f.write(c)

# Verify
new_count = c.count("apply h_contra")
print(f"Remaining 'apply h_contra': {new_count}")
print("Done!")
