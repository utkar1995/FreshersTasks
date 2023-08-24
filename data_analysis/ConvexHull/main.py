import re
import pymongo
# import openpyxl
import numpy as np
import extract_locality as loc
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

# def plot_convex_hull(points, color='gray'):
#     hull = ConvexHull(points)
#     for simplex in hull.simplices:
#         plt.plot(points[simplex, 0], points[simplex, 1], color)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # create mongoDB connection save all records in data variable
    mongoClient = pymongo.MongoClient('mongodb://localhost:27017/')
    addressDB = mongoClient['training']
    addressCollection = addressDB["localities_ambiguousData"]
    data = addressCollection.find()
    # Iterate through the JSON data and extract localities
    dictionary = {}

    for entry in data:
        locality = loc.extract_locality(entry["locality_name"], entry["sub_locality_1_name"])
        # print("Original locality_name:", entry["locality_name"])
        # print("Original sub_locality_1_name:", entry["sub_locality_1_name"])
        # print("Extracted locality:", locality)
        lat = entry["location"]["coordinates"][0]
        long = entry["location"]["coordinates"][1]
        # print(" points = ","(", lat,    ", ", long, ")")

        if dictionary.get(locality) is not None:
            dictionary[locality].append([lat, long])
        else:
            dictionary[locality] = [[lat, long]]
        print("-" * 40)
    # dictionary["andheri"].append([1, 2])
    print(dictionary)
    # create convex hull for each label on same graph
    import matplotlib.pyplot as plt
    from scipy.spatial import ConvexHull
    import numpy as np

    plt.figure(figsize=(8, 6))

    for region_label, region_points in dictionary.items():
        if len(region_points)<3:
            continue
        region_points = np.array(region_points)
        x_values = [point[0] for point in region_points]
        y_values = [point[1] for point in region_points]
        plt.scatter(x_values, y_values, label=region_label)
        hull = ConvexHull(region_points)

        for simplex in hull.simplices:
            plt.plot(region_points[simplex, 0], region_points[simplex, 1], 'gray')

        # plot_convex_hull(region_points, color='blue')
    
    # Plot convex hulls for each region



    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Convex Hull of Multiple Regions")
    plt.legend()
    plt.show()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
