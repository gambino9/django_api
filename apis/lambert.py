from scipy import spatial
import pandas as pd
import math
import csv
import os

# Load CSV file with absolute path
dirname = os.path.dirname(__file__)
path_coordinates = os.path.join(dirname, '../resources/2018_01_Sites_mobiles_2G_3G_4G_France_metropolitaine_L93.csv')
# Create dataframe from CSV file and remove last row (N/A datas)
dataframe = pd.read_csv(path_coordinates)
dataframe = dataframe.drop([dataframe.index[-1]])


def retrieve_lambert_from_json(json_dict):
    """
    Get the lambert93 values from the governmental API data
    Returns tuple containing x and y
    """
    # Takes only the first element of the response of
    # the Gov API because they are sorted by relevance
    first_item = json_dict['features'][0]
    x = first_item['properties']['x']
    y = first_item['properties']['y']
    return x, y


def create_coordinates_tree():
    """
    Load CSV file, create and returns a KD tree using
    a list of points (x, y) we create from the dataset
    """
    with open(path_coordinates) as csv_file:
        csv_reader = csv.reader(csv_file)

        next(csv_reader)  # skip header
        list_coord = []
        # creating list of X and Y while iterating through dataset
        for row in csv_reader:
            row_list = row[0].split(';')
            list_coord.append((row_list[1], row_list[2]))
    list_coord.remove(list_coord[-1])  # remove row containing N/A datas
    tree_coord = spatial.KDTree(list_coord)
    return tree_coord


def find_nearest_points(x, y, tree):
    """
    Find the 8 nearest points in tree and checks if they are close enough
    Returns list of indexes of those nearest points.
    """
    array_distances, array_indexes = tree.query((x, y), k=8)
    indexes_list = []
    for i in range(len(array_distances)):
        # If absolute distance between the closest point and current point < 100
        if math.isclose(array_distances[0], array_distances[i], abs_tol=100):
            indexes_list.append(array_indexes[i])
    return indexes_list


def create_list_rows(indexes):
    """
    Returns list of lists of the nearest points rows from the dataset
    Keeps only one row per provider
    """
    list_rows = []
    dict_index = {}
    for index in indexes:
        df_rows = dataframe.iloc[index]
        row = df_rows[0].split(';')
        if row[0] not in dict_index:  # make sure no duplicate provider in list
            list_rows.append(row)
            dict_index[row[0]] = 0
        else:
            pass
    return list_rows


def format_coverage_dict(list_of_lists):
    """
    Returns a dictionary of dictionaries of the network coverage
    """
    provider_dict = {
        20801: "Orange",
        20810: "SFR",
        20815: "Free",
        20820: "Bouygues",
    }

    dict_coverage = {}
    for lis in list_of_lists:
        dict_coverage[provider_dict[int(lis[0])]] = {
            '2G': bool(int(lis[3])),
            '3G': bool(int(lis[4])),
            '4G': bool(int(lis[5])),
        }
    return dict_coverage
