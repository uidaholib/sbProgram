# pylint: disable=W0703
"""Handle Science Base Exceptions via waiting time (5 min)."""
import sys
import time
import sciencebasepy

SB = sciencebasepy.SbSession()

def main(problem_id, sb_action):
    """Handle Exceptions, return values if successful, return False otherwise.

    Arguments:
        problem_id -- (string) the Science Base ID whose request raised the
                      Exception from Science Base.
        sb_action -- (string) the Science Base function name that was being
                     used when the Exception was raised by Science Base.

    Returns:
        item_json -- (json) the json of the problem_id if successfully
                     retrieved and the Science Base function was .get_item().
        item_children -- (list) a list of the Science Base IDs (strings) of
                         the children of the problem_id if successfully
                         retrieved and the Science Base function was
                         .get_child_ids().
        item_ancestors -- (list) a list of the Science Base IDs (strings) of
                          the descendents of the problem_id if successfully
                          retrieved and the Science Base function was
                          .get_ancestor_ids().
        item_shortcuts -- (list) a list of the Science Base IDs (strings) of
                          any shortcuts found within problem_id if successfully
                          retrieved and the Science Base function was
                          .get_shortcut_ids().
        False -- (boolean) returned if any of the above operations were
                 unsuccessful.

    Raises:
        ValueError -- if sb_action does not contain a legal string

    """
    print("--------Waiting for 404 to reset...")
    print("problem_id: {0}".format(problem_id))
    seconds = 5
    countdown(seconds)
    if sb_action == ".get_item":
        if __debug__:
            print("sb_action is '.get_item'")
        try:
            item_json = SB.get_item(problem_id)
            time.sleep(.050)  # Possibly for use to combat exceptions
            print("It worked!")
            if __debug__:
                print("Returning: \n{0}".format(item_json))
            return item_json
        except Exception:
            print("Didn't work")
            return False
    elif sb_action == ".get_child_ids":
        if __debug__:
            print("sb_action is '.get_child_ids'")
        try:
            item_children = SB.get_child_ids(problem_id)
            time.sleep(1)  # Possibly for use to combat exceptions
            print("It worked!")
            if __debug__:
                print("Returning: \n{0}".format(item_children))
            return item_children
        except Exception:
            print("Didn't work")
            return False
    elif sb_action == ".get_ancestor_ids":
        if __debug__:
            print("sb_action is '.get_ancestor_ids'")
        try:
            item_ancestors = SB.get_ancestor_ids(problem_id)
            time.sleep(.050)  # Possibly for use to combat exceptions
            print("It worked!")
            if __debug__:
                print("Returning: \n{0}".format(item_ancestors))
            return item_ancestors
        except Exception:
            print("Didn't work")
            return False
    elif sb_action == ".get_shortcut_ids":
        if __debug__:
            print("sb_action is '.get_item'")
        try:
            item_shortcuts = SB.get_shortcut_ids(problem_id)
            time.sleep(.050)  # Possibly for use to combat exceptions
            print("It worked!")
            if __debug__:
                print("Returning: \n{0}".format(item_shortcuts))
            return item_shortcuts
        except Exception:
            print("Didn't work")
            return False
    else:
        raise ValueError("Unrecognized Science Base function in "
                         + "exception_raised.main().")


def countdown(seconds): # in seconds
    """Countdown function that displays progress on one line.

    Arguments:
        seconds -- (integer) the number of seconds from which to count down to
                   zero.

    """
    for remaining in range(seconds, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write("{:2d} seconds remaining.".format(remaining))
        sys.stdout.flush()
        time.sleep(1)  # Possibly for use to combat exceptions
    sys.stdout.write("\rComplete!            \n")
