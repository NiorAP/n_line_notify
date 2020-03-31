# --------------------------------------------------------------------------- #
#                              Import Libraries                               #
# --------------------------------------------------------------------------- #

import sys
import requests
from typing import Tuple, Union
# from ap_line_notify._settings import settings
import json
from importlib.resources import read_text

# --------------------------------------------------------------------------- #
#                              Class Definitions                              #
# --------------------------------------------------------------------------- #


class LineNotify:

    """
    An object that stores Line Notify API token
    It has send_text, send_sticker, and send_image methods

    Parameter(s)
        token   : Line Notify token generated from https://notify-bot.line.me/

    Examples:
        from a_line_notify import LineNotify

        token = 'Token generated from link above'
        notify = LineNotify(token)

        # Send text
        notify.send_text('Test send text via Line Notify')

        # Send sticker
        notify.send_sticker(2, 1)

        # Send image
        notify.send_image('https://avatars3.githubusercontent.com/u/48649457')
    """

    # Initial Method, Only save the token
    def __init__(self, token: str) -> None:

        self.token = token

    # ----------------------------------------------------------------------- #
    # Response Reader Private Method, read raw response and return readable one
    def __read_response(self, response: requests.models.Response) \
            -> Tuple[int, str]:

        code = response.status_code

        status = {200: 'Success', 400: 'Unauthorized request',
                  401: 'Invalid access token',
                  500: 'Failure due to server error'}

        if code in status.keys():
            return code, status[code]

        else:
            return code, 'Processed over time or stopped'

    # ----------------------------------------------------------------------- #
    # Request Sender Private Method, Send POST request to Line Notify server
    def __send_line(self, headers: dict, data: dict, file: dict = None) \
            -> Tuple[int, str]:

        response = requests.post('https://notify-api.line.me/api/notify',
                                 headers=headers, data=data, files=file)

        return self.__read_response(response)

    # ----------------------------------------------------------------------- #
    def send_text(self, message: str) -> Tuple[int, str]:

        """
        Method use to send text message via Line Notify
        Argument(s):
            message     : [String] Text to send
        """

        headers = {'Authorization': 'Bearer ' + self.token,
                   'content-type': 'application/x-www-form-urlencoded'}

        data = {'message': message}

        return self.__send_line(headers, data)

    # ----------------------------------------------------------------------- #
    def send_sticker(self, sticker_id: int, package_id: int,
                     message: str = ' ') -> Tuple[int, str]:

        """
        Method use to send sticker via Line Notify
        Argument(s):
            sticker_id  : [Integer] ID of the sticker
            package_id  : [Integer] ID of the package of the sticker you want
            message     : [String][Default ' '] Text to send with sticker

        Find out more about sticker_id and package_id at
        https://devdocs.line.me/files/sticker_list.pdf
        """

        headers = {'Authorization': 'Bearer ' + self.token,
                   'content-type': 'application/x-www-form-urlencoded'}

        data = {'message': message, 'stickerPackageId': package_id,
                'stickerId': sticker_id}

        return self.__send_line(headers, data)

    # ----------------------------------------------------------------------- #
    def send_image(self, image: Union[bytes, str], message: str = ' ') \
            -> Tuple[int, str]:

        """
        Method use to send sticker via Line Notify
        Argument(s):
            image       : [bytes|string] image to send, can be either
                          - bytes object image
                          - image file's local path
                          - image file's web url
            message     : [String][Default ' '] Text to send with image
        """

        headers = {'Authorization': 'Bearer ' + self.token}

        data = {'message': message}

        if type(image) == bytes:
            return self.__send_line(headers, data, file={'imageFile': image})

        elif type(image) == str:

            if image[:4] == 'http':
                headers['content-type'] = 'application/x-www-form-urlencoded'
                data['imageThumbnail'] = image
                data['imageFullsize'] = image
                return self.__send_line(headers, data)

            else:
                with open(image, 'rb') as file:

                    return self.__send_line(headers, data,
                                            file={'imageFile': file})

# --------------------------------------------------------------------------- #
#                             Unit Test Functions                             #
# --------------------------------------------------------------------------- #


def test_line_notify(token: str) -> None:

    """Function that performs test on all command of LineNotify class"""

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
        settings['sample_image'],
        'Test send image via Line Notify')
    if response_3[0] == 200:
        print('test send image via Line Notify Successfully')
    else:
        print('test send image via Line Notify failed:', response_3[1])

# --------------------------------------------------------------------------- #
#                               Main Executions                               #
# --------------------------------------------------------------------------- #


if __name__ == '__main__':

    settings = json.loads(read_text('ap_line_notify', 'settings.json'))

    # Get all command line arguments
    arg = sys.argv

    # Check if there are 2 arguments (this filename and token) or not
    if len(arg) == 2:
        # Use token from the argument
        print('Use given token')
        test_token = arg[1]

    else:
        # Check if there are more than 2 arguments, print some message
        if len(arg) > 2:
            print('Too many arguments, use default test token instead.')

        # Use default test token
        test_token = settings['token']

    # Call unit test function
    test_line_notify(test_token)

# --------------------------------------------------------------------------- #
