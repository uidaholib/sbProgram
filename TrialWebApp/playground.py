
# import g
# from pprint import pprint
# import json
# import requests
# import pysb

# def get_NW_FYs():
#     NWCSC_FYs_OrderedDict = {}
#     SWCSC_FYs_OrderedDict = {}
#     # NWCSC_FYs = sb.get_child_ids("4f8c64d2e4b0546c0c397b46")
#     NWCSC_FYs = ["ID1", "ID2", "ID3", "ID4", "ID5", "ID6", "ID7", "ID8"]  # Delete later
#     #print(NWCSC_FYs)
#     NWCSC_FYs_Dict = {}
#     TitleNum = 2018  # Delete later
#     for ID in NWCSC_FYs:
#         # json = sb.get_item(ID)
#         #title = json['title']
#         title = "Fiscal Year "+str(TitleNum)  # Delete later
#         TitleNum -= 1  # Delete later

#         NWCSC_FYs_Dict.update({title: ID})
#     print(NWCSC_FYs_Dict)
#     return(NWCSC_FYs_Dict)

# def get_SW_FYs():
#     # SWCSC_FYs = sb.get_child_ids("4f8c6580e4b0546c0c397b4e")
#     SWCSC_FYs = ["ID1", "ID2", "ID3", "ID4", "ID5", "ID6", "ID7", "ID8"]  # Delete later
#     print(SWCSC_FYs)
#     SWCSC_FYs_Dict = {}
#     TitleNum = 2018  # Delete later
#     for ID in SWCSC_FYs:
#         # json = sb.get_item(ID)
#         # title = json['title']
#         title = "Fiscal Year "+str(TitleNum)  # Delete later
#         TitleNum -= 1  # Delete later
#         SWCSC_FYs_Dict.update({title: ID})
#     print(SWCSC_FYs_Dict)

#     return(SWCSC_FYs_Dict)

# #@app.route('/', methods=['GET', 'POST'])
# def index():
#     error = None
#     NWCSC_FYs_Dict = get_NW_FYs()
#     SWCSC_FYs_Dict = get_SW_FYs()
#     NWCSC_FYs_json = json.dumps(NWCSC_FYs_Dict, sort_keys = True, indent = 2)
#     NWCSC_FYs_json_load = json.load(NWCSC_FYs_json)
#     print(NWCSC_FYs_json_load)
#     SWCSC_FYs_json = json.dumps(SWCSC_FYs_Dict, sort_keys = True, indent = 2)
#     print(SWCSC_FYs_json)
#     print(NWCSC_FYs_json.type())
#     for title in NWCSC_FYs_json:
#         print(title)

#     #return(render_template('index.html', **locals(), title="Home"))


# # index()


import json

class Object:
    age = None
    name = None
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


me = Object()
me.name = "Onur"
me.age = 35
me.dog = Object()
me.dog.name = "Apollo"

print(me.toJSON())
