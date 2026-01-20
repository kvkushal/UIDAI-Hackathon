import re

# Read app.py
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Count original occurrences
original_count = content.count('ASS')
print(f"Found {original_count} occurrences of 'ASS' in app.py")

# Replace ASS with AHS (carefully to avoid replacing parts of words)
replacements = [
    ("'ASS'", "'AHS'"),
    ('"ASS"', '"AHS"'),
    ('[ASS]', '[AHS]'),
    ('avg_ass', 'avg_ahs'),
]

for old, new in replacements:
    content = content.replace(old, new)

# Write back
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

# Verify
new_count = content.count('ASS')
print(f"After replacement: {new_count} occurrences remaining")
print("✅ app.py updated: ASS -> AHS")
