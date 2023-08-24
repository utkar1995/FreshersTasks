import re

address = "State Bank of India, Plot No 12, 1st Floor, UTI Building, Rd Number 9, behind Hotel Tunga Paradise, Marol MIDC Industry Estate, Andheri east"

sublocality = "State Bank of India, Plot No 12, 1st Floor, UTI Building, Rd Number 9, behind Hotel Tunga Paradise, Marol MIDC Industry Estate, Andheri east"

# Function to extract the locality from the address
def extract_locality(address):
    parts = re.split(r',', address) #re.split(r'[,\s]+', address)

    # Look for a recognizable locality keyword (e.g., "Estate", "Area", etc.)
    locality_keywords = ["east","west"]
    not_accept_keywords = ["circle","marg","Estate", "Area", "Colony", "Zone", "Sector", "room","plot","near","opp","next","beside","society","chs","nagar","behind"]

    for part in parts:
        # check for part contain number
        #yes then move next
        pattern = r'\b\w*\d[\w\s]*\b'  # Regular expression to match words with spaces and numbers
        matches = re.findall(pattern, part)
        if len(matches)>0:
            continue
        for key in locality_keywords: #extracting words contain east west
            if part.lower().__contains__(key):
                pattern = r'\s*\(?(west|east)\)?' #r'\b(?:' + '|'.join(locality_keywords) + r')\b'

                # Remove target words using re.sub()
                locality_refined = re.sub(pattern, '', part, flags=re.IGNORECASE)
                return locality_refined

        if len(parts) == 1 and len(part.strip())>0: # checking for empty string
            return part

        flag_not_accept=False
        for not_accept_key in not_accept_keywords:
            if part.__contains__(not_accept_key):
                flag_not_accept=True

        sublocality_words = re.split(r',', sublocality)
        for sublocality_word in sublocality_words:
            if sublocality_word.__contains__(part) or part.__contains__(sublocality_word):
                flag_not_accept = True
        if flag_not_accept:#if part contain not acceptible key then skip that part
            continue

    return None  # Return None if no suitable locality is found


locality = extract_locality(address)
if locality:
    print("Identified Locality:", locality)
else:
    print("No Recognizable Locality Found")
