import re
import pymongo
# import openpyxl
import numpy as np
import extract_locality as loc
import pandas as pd
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def ccw(A,B,C):
    return (C.y-A.y)*(B.x-A.x) > (B.y-A.y)*(C.x-A.x)

def intersect(A, B, C, D):
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)
def lineLineIntersection(A, B, C, D, tolerance=1):
    x1, y1 = A.x,A.y
    x2, y2 = B.x,B.y
    x3, y3 = C.x,C.y
    x4, y4 = D.x,D.y

    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    if denominator == 0:
        return None  # Lines are parallel or coincident

    t1 = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominator
    t2 = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denominator

    if 0 <= t1 <= 1 and 0 <= t2 <= 1:
        intersection_x = x1 + t1 * (x2 - x1)
        intersection_y = y1 + t1 * (y2 - y1)
        return intersection_x, intersection_y
    else:
        return None  # Intersection is outside the line segments


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
        if True:#locality in ['borivali', 'dahisar']: # for testing
            lat = entry["location"]["coordinates"][0]
            long = entry["location"]["coordinates"][1]
            if dictionary.get(locality) is not None:
                dictionary[locality].append([lat, long])
            else:
                dictionary[locality] = [[lat, long]]
        # print("-" * 40)

    print(dictionary)
    # create convex hull for each label on same graph
    import matplotlib.pyplot as plt
    from scipy.spatial import ConvexHull
    import numpy as np

    plt.figure(figsize=(8, 6))
    dict_edges_CH = {} # stores edges of convex hull region in format = [[x1,x2],[y1,y2]]
    for region_label, region_points in dictionary.items():
        dict_edges_CH[region_label] = []
        if len(region_points) < 3:
            continue
        region_points = np.array(region_points)
        x_values = [point[0] for point in region_points]
        y_values = [point[1] for point in region_points]
        plt.scatter(x_values, y_values, label=region_label)
        hull = ConvexHull(region_points)

        for simplex in hull.simplices:
            print(" simplex = ", simplex)
            print(type(simplex))
            print(" region_points[simplex, 0] = ", region_points[simplex, 0], " region_points[simplex, 1] = ", region_points[simplex, 1])
            dict_edges_CH[region_label].append([region_points[simplex, 0], region_points[simplex, 1]])
            plt.plot(region_points[simplex, 0], region_points[simplex, 1], 'gray')
        print("region  = ", region_label)
        print("boundries of region", dict_edges_CH[region_label])

    # loop over every boundry edge of every region
    # need here check for avoid rework create visited dic which maintain
    # calculated intersections
    # every edge in current region compared with every other region
    # find intersection points
    # find points inside other region
    dict_visited_regions = {} # as common region same for visited region it prevents to recalculate for visited region
    print("dict_edges_CH = ", dict_edges_CH)
    # points to remember that format of convex hull lines are [[x1,x2],[y1,y2]]
    for curr_region, curr_convex_hull_points in dict_edges_CH.items():
        # creating region_visited record of empty dictionary
        if dict_visited_regions.get(curr_region) is None:
            dict_visited_regions[curr_region] = []
        print("dict_visited_regions = ", dict_visited_regions[curr_region], " curr_region = ", curr_region)
        for region_label, convex_hull_points in dict_edges_CH.items(): # looping over every other region
            # creating region_label record of empty dictionary
            if dict_visited_regions.get(region_label) is None:
                dict_visited_regions[region_label] = []
            if curr_region is not region_label and region_label not in dict_visited_regions[curr_region]:
                dict_visited_regions[curr_region].append(region_label)
                dict_visited_regions[region_label].append(curr_region)
                intersection_points = []
                # points to remember that format of convex hull lines are [[x1,x2],[y1,y2]]
                for curr_region_line in curr_convex_hull_points: # current region contain set of edges
                    # looping over every edge to check for intersection with other region edge
                    A = Point(curr_region_line[0][0], curr_region_line[1][0])
                    B = Point(curr_region_line[0][1], curr_region_line[1][1]) # edge AB
                    for region_line in convex_hull_points: # looping over other region edges
                        C = Point(region_line[0][0], region_line[1][0])
                        D = Point(region_line[0][1], region_line[1][1]) # edge CD
                        # check any of point A/B inside convex hull of region_line and vice versa
                        curr_convex_hull = ConvexHull(dictionary[curr_region])
                        region_convex_hull = ConvexHull(dictionary[region_label])
                        # Check if the test point is in the convex hull
                        if all(curr_convex_hull.equations @ np.hstack(([C.x, C.y], 1)) <= 0):
                            intersection_points.append([C.x, C.y])
                        if all(curr_convex_hull.equations @ np.hstack(([D.x, D.y], 1)) <= 0):
                            intersection_points.append([D.x, D.y])
                        if all(region_convex_hull.equations @ np.hstack(([A.x, A.y], 1)) <= 0):
                            intersection_points.append([A.x, A.y])
                        if all(region_convex_hull.equations @ np.hstack(([B.x, B.y], 1)) <= 0):
                            intersection_points.append([B.x, B.y])
                        intersection_point = None
                        if intersect(A, B, C, D):
                            intersection_point = lineLineIntersection(A, B, C, D)
                        if intersection_point is not None:
                            intersection_points.append(intersection_point)

                intersection_points = np.array(intersection_points)
                if len(intersection_points) == 0:
                    print("there are no intersection..")
                    continue
                print("intersection_points[:, 0] = ", intersection_points)
                print(len(intersection_points))
                convex_hull = ConvexHull(intersection_points) # creating convex hull intersection points to fill common region
                convex_hull_vertices = intersection_points[convex_hull.vertices]
                plt.fill(convex_hull_vertices[:, 0], convex_hull_vertices[:, 1], color='red', alpha=0.5)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Convex Hull of Multiple Regions")
    plt.legend()
    plt.show()
    print(dict_edges_CH)
    # finding intersection points between convex hull
    # print(type(dict_edges_CH['jogeshwari'][0][0]))
    # print(dict_edges_CH['jogeshwari'][0][0][0])



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
