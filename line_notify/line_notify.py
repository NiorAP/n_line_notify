# --------------------------------------------------------------------------- #
#                              Import Libraries                               #
# --------------------------------------------------------------------------- #

import requests

from typing import Tuple, Union
from numpy import ndarray
from io import BytesIO
from imageio import imsave
from urllib.parse import urlparse

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
    def send_image(self, image: Union[ndarray, str], message: str = ' ') \
            -> Tuple[int, str]:

        """
        Method use to send sticker via Line Notify
        Argument(s):
            image       : [numpy.ndarray|string] image to send, can be either
                          - numpy array image
                          - image file's local path
                          - image file's web url
            message     : [String][Default ' '] Text to send with image
        """

        headers = {'Authorization': 'Bearer ' + self.token}

        data = {'message': message}

        if isinstance(image, ndarray):
            temp = BytesIO()
            imsave(temp, image, format='png')
            return self.__send_line(headers, data,
                                    file={'imageFile': temp.getvalue()})

        elif isinstance(image, str):

            parsed = urlparse(image)
            if parsed[1] != '':
                headers['content-type'] = 'application/x-www-form-urlencoded'
                data['imageThumbnail'] = image
                data['imageFullsize'] = image
                return self.__send_line(headers, data)

            else:
                with open(image, 'rb') as file:

                    return self.__send_line(headers, data,
                                            file={'imageFile': file})

        else:
            raise TypeError

# --------------------------------------------------------------------------- #
