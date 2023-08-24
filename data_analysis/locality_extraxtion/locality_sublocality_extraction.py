import re
import pymongo
import openpyxl
import pandas as pd
# # Sample JSON data
# data = [
# {
#         "country_name": "India",
#         "state_name": "Utter Pradesh",
#         "district_name": "Ghaziabad",
#         "city_name": "Ghaziabad",
#         "locality_name": "sudisa, sidsdoi",
#         "sub_locality_1_name": "",
#         "building_number": "",
#         "floor_number": "",
#         "pin_code": "99999999"
#     }
#     ,
#
#     {
#         "country_name": "India",
#         "state_name": "Maharashtra",
#         "district_name": "Mumbai",
#         "city_name": "Mumbai",
#         "locality_name": "bandra",
#         "sub_locality_1_name": "bandra west",
#         "building_number": "90/4",
#         "floor_number": "3",
#         "pin_code": "99999999"
#     },
#     {
#
#         "country_name": "India",
#         "state_name": "Karnataka",
#         "district_name": "Bengaluru",
#         "city_name": "Bengaluru",
#         "locality_name": "88, Ratna Vilas Road, Southend Circle, Basavanagudi,",
#         "sub_locality_1_name": "Ratna Vilas Road",
#         "building_number": "88",
#         "floor_number": "",
#         "pin_code": "560004"
#     },
#
#     {
#
#         "country_name": "India",
#         "state_name": "Maharashtra",
#         "district_name": "Mumbai",
#         "city_name": "Mumbai",
#         "locality_name": "naigaon,dadar",
#         "sub_locality_1_name": "Hasan Chamber, SS Wagh Marg, Shindewari, Radhika Saikripa Co-op Society,Naigaon",
#         "building_number": "90/4",
#         "floor_number": "3",
#         "pin_code": "400014"
#     },
#     {
#
#         "country_name": "India",
#         "state_name": "Maharashtra",
#         "district_name": "Mumbai",
#         "city_name": "Mumbai",
#         "locality_name": "Mahul Rd, Chembur Colony, Chembur",
#         "sub_locality_1_name": "Mahul Rd",
#         "building_number": "90/4",
#         "floor_number": "3",
#         "pin_code": "400074"
#     },
#     {
#
#         "country_name": "India",
#         "state_name": "Maharashtra",
#         "district_name": "Mumbai",
#         "city_name": "Mumbai",
#         "locality_name": "Zoom Plaza Mall, Gorai 1, Borivali",
#         "sub_locality_1_name": "Gorai 1",
#         "building_number": "90/4",
#         "floor_number": "3",
#         "pin_code": "400092"
#     },
#     {
#
#         "country_name": "India",
#         "state_name": "Maharashtra",
#         "district_name": "Mumbai",
#         "city_name": "Mumbai",
#         "locality_name": "Kandivali West",
#         "sub_locality_1_name": "Shri Sevantilal Khandwala Marg, Kandivali, Charkop Industrial Estate,",
#         "building_number": "90/4",
#         "floor_number": "3",
#         "pin_code": "400067"
#     },
#     {
#
#         "country_name": "India",
#         "state_name": "Maharashtra",
#         "district_name": "Mumbai",
#         "city_name": "Mumbai",
#         "locality_name": "Kurar, Ambewadi,Malad East",
#         "sub_locality_1_name": "near Shantaram Pond, Kurar Village Rd, Shantaram Talao, Kurar, Ambewadi",
#         "building_number": "90/4",
#         "floor_number": "3",
#         "pin_code": "400097"
#     },
#     {
#
#         "country_name": "India",
#         "state_name": "Maharashtra",
#         "district_name": "Mumbai",
#         "city_name": "Mumbai",
#         "locality_name": "AAREY, Goregaon,",
#         "sub_locality_1_name": "CHECK NAKA, SHOP NO . 5 NAVYUG CHS, Western Express Hwy, near AAREY,",
#         "building_number": "5",
#         "floor_number": "",
#         "pin_code": "400063"
#     },
#     {
#
#         "country_name": "India",
#         "state_name": "Maharashtra",
#         "district_name": "Mumbai",
#         "city_name": "Mumbai",
#         "locality_name": "Jai Bhim Nagar, Goregaon,",
#         "sub_locality_1_name": "Jai Bhim Nagar,",
#         "building_number": "90/4",
#         "floor_number": "3",
#         "pin_code": "400065"
#     },
#     {
#
#         "country_name": "India",
#         "state_name": "Maharashtra",
#         "district_name": "Mumbai",
#         "city_name": "Mumbai",
#         "locality_name": "Ruhaan Enterprises, Hanuman Road, Western Express Hwy, Vile Parle East,",
#         "sub_locality_1_name": "Ruhaan Enterprises, Hanuman Road, Western Express Hwy, Vile Parle East,",
#         "building_number": "90/4",
#         "floor_number": "3",
#         "pin_code": "400057"
#     },
#     {
#
#         "country_name": "India",
#         "state_name": "Maharashtra",
#         "district_name": "Mumbai",
#         "city_name": "Mumbai",
#         "locality_name": "Andheri",
#         "sub_locality_1_name": "J B Nagar, Andheri East,",
#         "building_number": "90/4",
#         "floor_number": "3",
#         "pin_code": "400053"
#     },
#     {
#
#         "country_name": "India",
#         "state_name": "Maharashtra",
#         "district_name": "Mumbai",
#         "city_name": "Mumbai",
#         "locality_name": "State Bank of India, Plot No 12, 1St Floor, UTI Building, Rd Number 9, behind Hotel Tunga Paradise, Marol MIDC Industry Estate, Andheri East,",
#         "sub_locality_1_name": "State Bank of India, Plot No 12, 1St Floor, UTI Building, Rd Number 9, behind Hotel Tunga Paradise, Marol MIDC Industry Estate, Andheri East,",
#         "building_number": "12",
#         "floor_number": "1",
#         "pin_code": "400093"
#     }
# ]


# Define a function to extract locality from the "locality_name" field
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
        for key in ['east', 'west','(e)','(w)']:  # extracting words contain east west
            part_lower = locality.lower().strip()



            # print("checking east west ",part_lower)
            pattern = r'\b' + re.escape(key) + r'\b'

            matches = re.findall(pattern, part_lower, re.IGNORECASE)  # Case-insensitive matching

            if len(matches)>0:
                pattern = r'\s*\(?(west|east)\)?'

                # Remove target words using re.sub()
                locality_refined = re.sub(pattern, '', locality, flags=re.IGNORECASE)
                return locality_refined
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


def extract_sublocality( sublocality_str):
    # Split the locality string using commas and spaces as delimiters
    # print("locailty = ",locality_str)
    # print("sublocaity = ",sublocality_str)

    sublocality_part = re.split(r',', sublocality_str)

    # Filter out empty or noise words

    sublocality_words = [part for part in sublocality_part if part.strip()]
    # print("refined parts = ",parts)
    # print("refined sublocality = ",sublocality)

    non_accept_keywords = ["mall", "Bank of", "floor", "Estate", "room", "plot", "near",
                           "opp", "next", "beside", "society", "chs", "behind", "before", "blg", "building"]
    # word_indicate_localities = ["rd","road","street","nagar","sector","circle","marg","hwy","area","zone"]
    for index, sublocality in enumerate(sublocality_words):
        is_last = False  # indicating current locality is last in list of multiple localities
        if len(sublocality_words) == index + 1:
            is_last = True
        sublocality = sublocality.strip().lower()
        # locality = locality
        # print("start = ",part)
        # check for locality contain just numbers with some symbols
        # yes then move next
        pattern = r'[-+]?\b\d+(?:\.\d+)?\b'  # r'\b\w*\d[\w\s]*\b'  # Regular expression to match words with spaces and numbers
        matches = re.findall(pattern, sublocality)
        if len(matches) > 0:
            continue

        # print("num check done, not single word")
        flag_not_accept = False

        for not_accept_key in non_accept_keywords:

            if not_accept_key.lower() in sublocality:
                if is_last:
                    return sublocality
                else:
                    flag_not_accept = True

                break
        # print("not key accept check done!")

        if flag_not_accept:
            continue

        # check
        for key in ['east', 'west', '(e)', '(w)']:  # extracting words contain east west
            part_lower = sublocality.lower().strip()

            # print("checking east west ",part_lower)
            pattern = r'\b' + re.escape(key) + r'\b'

            matches = re.findall(pattern, part_lower, re.IGNORECASE)  # Case-insensitive matching

            if len(matches) > 0:
                pattern = r'\s*\(?(west|east)\)?'

                # Remove target words using re.sub()
                locality_refined = re.sub(pattern, '', sublocality, flags=re.IGNORECASE)
                return locality_refined
        if len(sublocality_words) == 1 and len(sublocality.strip()) > 0:  # checking for empty string
            return sublocality
        # why last locality word returned as locality?, no locality matched so returning last index locality
        if is_last:
            return sublocality
        # print("sublocality check done! for =", part,flag_not_accept)
        if not flag_not_accept:  # if part contain not acceptible key then skip that part
            return sublocality

    return None  # Return None if no suitable locality is found


# create mongoDB connection save all records in data variable
mongoClient = pymongo.MongoClient('mongodb://localhost:27017/')

addressDB = mongoClient['training']
addressCollection = addressDB["locality_eg_addresses"]
data = addressCollection.find()
# Iterate through the JSON data and extract localities
dictionary = {"localities_found":[],"sublocalities_found":[],"data_samples":[]}
workbook = openpyxl.Workbook()
sheet = workbook.active
for entry in data:
    locality = extract_locality(entry["locality_name"], entry["sub_locality_1_name"])
    sublocality = extract_sublocality(entry["sub_locality_1_name"])
    flag_data_appended = False
    localities = dictionary.get("localities_found")
    sublocalities = dictionary.get("sublocalities_found")
    dataSamples = dictionary.get("data_samples")
    if sublocality is None:
        sublocality = "NA"
    if locality is None:
        locality = "NA"
    for index, loc in enumerate(localities):
        sublocality_for_current_locality = localities[index]

        if locality == loc and sublocality_for_current_locality == sublocality:
            dictionary.get("data_samples")[index] = dataSamples[index]+1
            flag_data_appended = True
            break

    if not flag_data_appended:
        localities.append(locality)
        sublocalities.append(sublocality)
        dataSamples.append(1)

    print("Original locality_name:", entry["locality_name"])
    print("Extracted locality:", locality)
    print("Original sub_locality_1_name:", entry["sub_locality_1_name"])
    print("Extracted sub - locality:", sublocality)
    print("-" * 40)
    df = pd.DataFrame(dictionary)
    df.to_excel("output_dict_loc_subloc.xlsx")
# for key, value in dictionary.items():
#     sheet.append([key, value])
#
# # Save the workbook to a file
# workbook.save("output_dict_loc_subloc.xlsx")