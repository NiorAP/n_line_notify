# --------------------------------------------------------------------------- #
#                              Import Libraries                               #
# --------------------------------------------------------------------------- #

from importlib.resources import read_text, read_binary
import json
import sys
from line_notify import LineNotify
from imageio import imread

# --------------------------------------------------------------------------- #
#                               Load Resources                                #
# --------------------------------------------------------------------------- #

try:
    settings = json.loads(read_text('resources', 'settings.json'))
except FileNotFoundError:
    settings = None

# --------------------------------------------------------------------------- #
#                             Unit Test Functions                             #
# --------------------------------------------------------------------------- #


def test(token: str) -> None:

    """Function that performs test on all command of LineNotify class"""

    if token is None:
        return None

    notify = LineNotify(token)

    # ----------------------------------------------------------------------- #
    print('Testing send text via Line Notify')
    response_1 = notify.send_text('Test send text via Line Notify')
    if response_1[0] == 200:
        print('test send text via Line Notify Successfully')
    else:
        print('test send text via Line Notify failed:', response_1[1])

    # ----------------------------------------------------------------------- #
    print('Testing send sticker via Line Notify')
    response_2 = notify.send_sticker(2, 1, 'Test send sticker via Line Notify')
    if response_2[0] == 200:
        print('test send sticker via Line Notify Successfully')
    else:
        print('test send sticker via Line Notify failed:', response_2[1])

    # ----------------------------------------------------------------------- #
    print('Testing send image via Line Notify')
    response_3 = notify.send_image(
        imread(read_binary('resources', 'NAP.jpg')),
        'Test send (numpy array) image via Line Notify')
    if response_3[0] == 200:
        print('test send (numpy array) image via Line Notify Successfully')
    else:
        print('test send (numpy array) image via Line Notify failed:',
              response_3[1])

# --------------------------------------------------------------------------- #
#                               Main Executions                               #
# --------------------------------------------------------------------------- #


if __name__ == '__main__':

    # Get all command line arguments
    arg = sys.argv

    # Check if there are 2 arguments (this filename and token) or not
    if len(arg) == 2:
        # Use token from the argument
        print('Use given token')
        test_token = arg[1]

    elif settings is not None:
        # Check if there are more than 2 arguments, print some message
        if len(arg) > 2:
            print('Too many arguments, trying to use default test token...')

        # Use default test token
        test_token = settings['token']

    else:
        print('No token was given or too many arguments to parse.')
        print('The test cannot be done.')
        test_token = None

    # Call unit test function
    test(test_token)

# --------------------------------------------------------------------------- #