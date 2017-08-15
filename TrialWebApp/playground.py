from random import randint

NWCSC_FYs = ("ID1", "ID2", "ID3", "ID4", "ID5", "ID6", "ID7", "ID8", )  # Delete later
NWCSC_FYs_Dict = {}
TitleNum = 2018  # Delete later
for ID in NWCSC_FYs:
    # json = sb.get_item(ID)
    #title = json['title']
    title = "Fiscal Year "+str(randint(2011, 2020))  # Delete later
    TitleNum -= 1  # Delete later

    NWCSC_FYs_Dict.update({title: ID})

print(NWCSC_FYs_Dict)
sort = sorted(NWCSC_FYs_Dict)
#print(sort)
NWCSC_FYs_OrderedDict = {}
for i in sort:
    NWCSC_FYs_OrderedDict.update({i: NWCSC_FYs_Dict[i]})

print(NWCSC_FYs_OrderedDict)
