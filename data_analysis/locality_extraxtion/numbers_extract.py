import re

list_of_items = ["123th main", "abc123", "45/6", "2-3", "789xyz", "42"]

pattern =  r'[-+]?\b\d+(?:\.\d+)?\b'#r'^\d+$'

numbers_only = [item for item in list_of_items if re.match(pattern, item)]

print(numbers_only)

# import re

text = "The quick bfoxn (fox) jumped over the lazy dog."
word_to_find = "fox"

pattern = r'\b' + re.escape(word_to_find) + r'\b'

matches = re.findall(pattern, text, re.IGNORECASE)  # Case-insensitive matching

print(matches)
print(re.sub(pattern, '', text, flags=re.IGNORECASE))

