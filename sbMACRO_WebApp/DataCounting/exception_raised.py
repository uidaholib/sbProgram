import pysb
import sys
import time

SB = pysb.SbSession()

def main(ProblemID, sb_action):
    print("--------Waiting for 404 to reset...")
    #time.sleep(300)
    t = 300
    countdown(t)
    if sb_action == ".get_item":
        try:
            item_json = SB.get_item(ProblemID)
            print("It worked!")
            return item_json
        except Exception:
            return False
    elif sb_action == ".get_child_ids":
        try:
            item_children = SB.get_child_ids(ProblemID)
            print("It worked!")
            return item_children
        except Exception:
            return False
    elif sb_action == ".get_ancestor_ids":
        try:
            item_ancestors = SB.get_ancestor_ids(ProblemID)
            print("It worked!")
            return item_ancestors
        except Exception:
            return False
    elif sb_action == ".get_shortcut_ids":
        try:
            item_shortcuts = SB.get_shortcut_ids(ProblemID)
            print("It worked!")
            return item_shortcuts
        except Exception:
            return False
    else:
        print("Unrecognized sb_action (exception_raised.py main()")
        try:
            item = SB.get_item(ProblemID)
            print("It worked!")
            return item
        except Exception:
            return False


def countdown(t): # in seconds
    for remaining in range(t, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write("{:2d} seconds remaining.".format(remaining))
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\rComplete!            \n")
