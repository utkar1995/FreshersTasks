import re

address = "Shop # 5,ground Floor, Plot 670, Shiravane Village, Thane Belapur Road, Nerul, Navi Mumbai,Mumbai, Maharashtra, 400706"

# Extracting components using regex
components = re.split(r',\s*', address)

# Assign extracted components to JSON format
json_format = {
    "state_name": components[-2],
    "district_name": components[-3],
    "city_name": components[-4],
    "locality_name": components[-5],
    "sub_locality_1_name": components[-6],
    "building_number": components[0],
    "floor_number": "",
    "pin_code": components[-1]
}

# Print the formatted JSON
print(json_format)
