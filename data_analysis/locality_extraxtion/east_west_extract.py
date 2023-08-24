import re

locality_name = "Ghatkopar (west)"
locality_keywords = ["east","west"]
# Define the regular expression pattern to match the keyword "west"
pattern  = r'\s*\(?(west|east)\)?'

# Use the re.search function to find the pattern in the locality_name
match = re.search(pattern, locality_name, flags=re.IGNORECASE)

if match:
    keyword_found = match.group()
    cleaned_locality_name = re.sub(pattern, '', locality_name, flags=re.IGNORECASE).strip()

    print(cleaned_locality_name)
else:
    print("Keyword not found")
