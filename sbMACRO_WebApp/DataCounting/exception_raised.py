import pysb
import sys
import time

SB = pysb.SbSession()

def main(ProblemID, sb_action):
    print("--------Waiting for 404 to reset...")
    print("ProblemID: {0}".format(ProblemID))
    #time.sleep(300)
    t = 300
    countdown(t)
    if sb_action == ".get_item":
        if __debug__:
            print("sb_action is '.get_item'")
        try:
            item_json = SB.get_item(ProblemID)
            print("It worked!")
            return item_json
        except Exception:
            if __debug__:
                print("Didn't work")
            return False
    elif sb_action == ".get_child_ids":
        if __debug__:
            print("sb_action is '.get_child_ids'")
        try:
            item_children = SB.get_child_ids(ProblemID)
            print("It worked!")
            return item_children
        except Exception:
            if __debug__:
                print("Didn't work")
            return False
    elif sb_action == ".get_ancestor_ids":
        if __debug__:
            print("sb_action is '.get_ancestor_ids'")
        try:
            item_ancestors = SB.get_ancestor_ids(ProblemID)
            print("It worked!")
            return item_ancestors
        except Exception:
            if __debug__:
                print("Didn't work")
            return False
    elif sb_action == ".get_shortcut_ids":
        if __debug__:
            print("sb_action is '.get_item'")
        try:
            item_shortcuts = SB.get_shortcut_ids(ProblemID)
            print("It worked!")
            return item_shortcuts
        except Exception:
            if __debug__:
                print("Didn't work")
            return False
    else:
        assert True, "Unrecognized sb_action in exception_raised.py main()"
        try:
            item = SB.get_item(ProblemID)
            print("It worked!")
            return item
        except Exception:
            if __debug__:
                print("Didn't work")
            return False


def countdown(t): # in seconds
    for remaining in range(t, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write("{:2d} seconds remaining.".format(remaining))
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\rComplete!            \n")
