import os
import json

class DataType(object):
    def __init__(self, d_type):
        self.type = d_type
        self.count = 1

date_type_list = []

fiscal_year_json_folder = os.path.abspath(os.path.dirname(__file__))
for the_file in os.listdir(fiscal_year_json_folder):
    file_path = os.path.join(fiscal_year_json_folder, the_file)
    try:
        if os.path.isfile(file_path) and file_path.endswith(".json"):
            with open(file_path) as json_data:
                print("\n\n\nOpening {}".format(the_file))
                data = json.load(json_data)
            try:  # If date doesn't exist replace the file.
                for project in data["projects"]:
                    print("\tStarting project: {}".format(project["name"]))
                    for item in project["project_items"]["Project_Item_List"]:
                        print("\t\tStarting item: {}".format(item["name"]))
                        try:
                            for date in item["sb_json"]["dates"]:
                                dtype = date["label"]
                                Found = False
                                for d in date_type_list:
                                    print("{0} == {1}??".format(d.type, dtype))
                                    if d.type == dtype:
                                        d.count += 1
                                        print("\t\t\tDate type: {} [Incr]"
                                              .format(dtype))
                                        Found = True
                                        break
                                # Was not found in list
                                if not Found:
                                    new_type = DataType(dtype)
                                    date_type_list.append(new_type)
                                    print("\t\t\tDate type: {} [Added]"
                                          .format(dtype))
                        except KeyError:
                            print("{} does not have 'dates'".format(item["name"]))

            except KeyError:
                print("Couldn't find date. This could be an error.")
                assert False, "Check this error"

    except Exception as err:  # pylint: disable=W0703
        raise Exception("Exception raised when getting filepath to jsons:"
                        + "\n" + err)
date_type_list.sort(key=lambda date: date.count, reverse=True)
print("Here's our list...")
num = 0
if len(date_type_list) == 0:
    print("List appears empty.")
    exit(0)
for i in date_type_list:
    num += 1
    if len(i.type) < 8:
        print("{0}.\t{1}\t\t\t\t{2}".format(num, i.type, i.count))
    elif len(i.type) > 15:
        print("{0}.\t{1}\t\t{2}".format(num, i.type, i.count))
    else:
        print("{0}.\t{1}\t\t\t{2}".format(num, i.type, i.count))
