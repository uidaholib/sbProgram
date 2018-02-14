import sys
import os
from pprint import pprint
import json
import datetime
import pysb  # pylint: disable=wrong-import-order



SB = pysb.SbSession()

def main():
    # marshes to mudflats: approved datasets
    marshes_id = "5046465ce4b0241d49d62c5b"
    # marshes test ids
    willapa_elevation_id = "554ce97fe4b082ec54129d8f"
    willapa_SLR_id = "55b2e697e4b09a3b01b5d9fd"
    SHORTCUT_veg = "587035dae4b01a71ba0c6087"
    #test:
    marshes_list = []
    marshes_list.extend((willapa_elevation_id, willapa_SLR_id, SHORTCUT_veg))
    print("Starting Marshes to Mudflats...")
    descendents = SB.get_ancestor_ids(marshes_id)
    found = 0
    for ID in marshes_list:
        if ID in descendents:
            print("Found {0} in descendents".format(ID))
            found += 1
    print("Found {0} of {1} test cases.".format(found, len(marshes_list)))
    print("Done")



    #Forest Management Tools... Approved Datasets
    forest_id = "570c0f67e4b0ef3b7ca04ed1"
    # Forest Man... Test ids
    Timelapse_Snoqualmie = "5706a650e4b032f77a8a4f82"
    Timelapse_Ollalie = "56eb39b5e4b0f59b85d91b51"
    #test:
    forest_list = []
    forest_list.extend((Timelapse_Snoqualmie, Timelapse_Ollalie))
    print("\n\n\nStarting Forest Management Tools...")
    descendents = SB.get_ancestor_ids(forest_id)
    found = 0
    for ID in forest_list:
        if ID in descendents:
            print("Found {0} in descendents".format(ID))
            found += 1
    print("Found {0} of {1} test cases.".format(found, len(forest_list)))
    print("Done")

    # UNDERSTANDING FUTURE EXTREME WATER EVENTS...
    fut_extreme_water_id = "502a9bd6e4b0a8e4a0fdb147"
    #test ids
    SHORTCUT_WesternUS = "54dd5e5ee4b08de9379b3908"
    #test:
    water_list = []
    water_list.append(SHORTCUT_WesternUS)
    print("\n\n\nStarting Future Extreme Water...")
    descendents = SB.get_ancestor_ids(fut_extreme_water_id)
    found = 0
    for ID in water_list:
        if ID in descendents:
            print("Found {0} in descendents".format(ID))
            found += 1
    print("Found {0} of {1} test cases.".format(found, len(water_list)))
    print("Done")


    # PINE BEETLE
    beetle_id = "5046564de4b0241d49d62c98"
    #test ids
    #DEEP
    Cascades_2019_99 = "53595d91e4b0031b2f49f18e"
    Yellowstone_2010_99 = "5359a66ae4b09cf31232550c"
    Rockies_2010_99 = "535af634e4b0d08644976d65"
    #Shallow
    Cascades_pine_mortality = "53593b35e4b0031b2f49edfe"
    #test:
    beetle_list = []
    beetle_list.extend((Cascades_2019_99, Yellowstone_2010_99, Rockies_2010_99, Cascades_pine_mortality))
    print("\n\n\nStarting Pine Beetle...")
    descendents = SB.get_ancestor_ids(beetle_id)
    found = 0
    for ID in beetle_list:
        if ID in descendents:
            print("Found {0} in descendents".format(ID))
            found += 1
    print("Found {0} of {1} test cases.".format(found, len(beetle_list)))
    print("Done")


if __name__ == "__main__":
    main()
