import sys
import g

import requests
import json
import pysb
import sys
import time


from pprint import pprint

sb = pysb.SbSession()


sys.excepthook = g.excepthook

def main():
    var1 = "True"
    var2 = False
    var3 = None
    var4 = "thing"
    main2()

def main2():
    print("Starting...")
    ID = "57daef3fe4b090824ffc3226"
    v1 = True
    v2 = "This"
    v3 = "is"
    v4 = 'test'
    child = sb.get_child_ids(ID)
    number = True
    if number is True:
        print("True")
        vari1 = 3
        vari2 = 4
        vari4 = 8
        for i in range(0,2):
            quote = "This is a thing."
            print("range")
            raise Exception('User does not have access.')
    for i in range(0, 5000):
        info = sb.get_item(ID)
    print("Done")



def old(type, value, traceback):
    print('Unhandled error:', type, value, traceback)
    v5 = inspect.getsource(traceback)
    print(v5)
    #v1 = inspect.trace(traceback)[-1][0].f_locals()
    #print(v1)
    v6 = inspect.getmembers(traceback)
    pprint(v6)
    v9 = list(v6)
    v8 = getattr(v9[0], 'tb_frame')
    print(v8)
    v7 = v6.__getitem__([-1])
    print(v7)
    thing = inspect.getmembers(v5, tb_frame)
    print(thing)
    thing2 = getargvalues(thing)
    print(thing2)
    #v4 = inspect(traceback, tb_frame)
    #print(v4)
    #v3 = inspect.getargvalues(v4)
    #print(v3)
    v1 = inspect.trace(traceback)[-1][0].f_locals[-1]
    print(v1)
    v2 = inspect.code().co_varnames()
    getargvalues
    print(v2)
if __name__ == '__main__':
    #try:
    main()
    #except Exception:
    #    import g
    #    g.excepthook
