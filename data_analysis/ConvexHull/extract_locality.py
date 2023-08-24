import re
import pymongo
import openpyxl

def extract_locality(locality_str,sublocality_str):
    # Split the locality string using commas and spaces as delimiters
    # print("locailty = ",locality_str)
    # print("sublocaity = ",sublocality_str)
    locality_parts = re.split(r',', locality_str)
    sublocality_part = re.split(r',', sublocality_str)

    # Filter out empty or noise words
    locality_words = [part for part in locality_parts if part.strip()]
    sublocality_words = [part for part in sublocality_part if part.strip()]
    # print("refined parts = ",parts)
    # print("refined sublocality = ",sublocality)

    non_accept_keywords = ["mall", "Bank of", "floor", "Estate", "room", "plot", "near",
     "opp", "next", "beside", "society", "chs", "behind","before","blg","building"]
    # word_indicate_localities = ["rd","road","street","nagar","sector","circle","marg","hwy","area","zone"]
    for index,locality in enumerate(locality_words):
        is_last = False # indicating current locality is last in list of multiple localities
        if len(locality_words) == index+1:
            is_last = True
        locality = locality.strip().lower()
        # locality = locality
        # print("start = ",part)
        # check for locality contain just numbers with some symbols
        # yes then move next
        pattern = r'[-+]?\b\d+(?:\.\d+)?\b'#r'\b\w*\d[\w\s]*\b'  # Regular expression to match words with spaces and numbers
        matches = re.findall(pattern, locality)
        if len(matches) > 0:
            continue

        #for east west identification:
        pattern = r'\s*\(?(west|east)\)?'
        pattern2 = r'\s?\([we]\)'
        regex = re.compile(pattern)
        estwst1 = regex.search(locality) is None
        # print("estwst1 : ", estwst1)
        regex = re.compile(pattern2)
        estwst2 = regex.search(locality) is None
        # print("estwst2 : ", estwst2)
        if not estwst1 or not estwst2: # any of west, east and (w), (e) matches will pass check
            locality_refined = locality
            if estwst2 is not True:
                locality_refined = re.sub(pattern2, '', locality, flags=re.IGNORECASE)
            if estwst1 is not True:
                locality_refined = re.sub(pattern, '', locality, flags=re.IGNORECASE)
            # Remove target words using re.sub()

            return locality_refined

        # for key in ['east', 'west','(e)','(w)']:  # extracting words contain east west
        #     part_lower = locality.lower().strip()
        #
        #
        #
        #     # print("checking east west ",part_lower)
        #     pattern = r'\b\s*' + re.escape(key) + r'\s*\b'
        #
        #     matches = re.findall(pattern, part_lower, re.IGNORECASE)  # Case-insensitive matching
        #     print("matches : ", matches, " locality : ", locality)
        #     if len(matches)>0:
        #         pattern = r'\s*\(?(west|east)\)?'
        #         pattern2 = r'\s?\([we]\)'
        #         regex = re.compile(pattern)
        #         estwst1 = regex.search(locality) is None
        #         print("estwst1 : ", estwst1)
        #         regex = re.compile(pattern2)
        #         estwst2 = regex.search(locality) is None
        #         print("estwst2 : ", estwst2)
        #         locality_refined = ''
        #         if estwst2 is not True:
        #             locality_refined = re.sub(pattern2, '', locality, flags=re.IGNORECASE)
        #         if estwst1 is not True:
        #             locality_refined = re.sub(pattern, '', locality, flags=re.IGNORECASE)
        #         # Remove target words using re.sub()
        #
        #         return locality_refined


        # print("num check done, not single word")
        flag_not_accept = False

        for not_accept_key in non_accept_keywords:

            if not_accept_key.lower() in locality:
                if is_last:
                    return locality
                else:
                    flag_not_accept = True

                break
        # print("not key accept check done!")

        if flag_not_accept:
            continue

        #check
        if len(locality_words) == 1 and len(locality.strip()) > 0:  # checking for empty string
            return locality
        for sublocality_word in sublocality_words:
            sublocality_word_refined = sublocality_word.strip().lower()
            # print("sublocality comparison = ", sublocality_word_refined)
            if locality in sublocality_word_refined:
                flag_not_accept = True
                break
            if sublocality_word_refined in locality:
                flag_not_accept = True
                break
        # why last locality word returned as locality?, no locality matched so returning last index locality
        if is_last:
            return locality
        # print("sublocality check done! for =", part,flag_not_accept)
        if not flag_not_accept:  # if part contain not acceptible key then skip that part
            return locality
    return None  # Return None if no suitable locality is found

#
# # create mongoDB connection save all records in data variable
# mongoClient = pymongo.MongoClient('mongodb://localhost:27017/')
#
# addressDB = mongoClient['training']
# addressCollection = addressDB["localities_ambiguousData"]
# data = addressCollection.find()
# # Iterate through the JSON data and extract localities
# dictionary = {"localities_found":"available_samples"}
# workbook = openpyxl.Workbook()
# sheet = workbook.active
# for entry in data:
#     locality = extract_locality(entry["locality_name"], entry["sub_locality_1_name"])
#     print("Original locality_name:", entry["locality_name"])
#     print("Original sub_locality_1_name:", entry["sub_locality_1_name"])
#     print("Extracted locality:", locality)
#
#     if dictionary.get(locality) is not None:
#         dictionary[locality] = dictionary[locality]+1
#     else:
#         dictionary[locality] = 1
#     print("-" * 40)
# for key, value in dictionary.items():
#     sheet.append([key, value])
#
# # Save the workbook to a file
# workbook.save("output_dict.xlsx")