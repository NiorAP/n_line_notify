# Line Notify Library
by Nior.A.P

Python package use to send text, sticker, and image via Line Notify

## Before use this
you have to generate API token first
1. go to https://notify-bot.line.me/
2. Log In using your line account.
3. Click "Generate token" button.
4. Enter token name and select a chat to send notifications to.
5. Click "Generate token" button and you will get the token you want.

## Install Library:
```shell script
pip install git+https://github.com/NiorAP/ap_line_notify.git
```

## Example:
```python
from line_notify import LineNotify

token = 'Token generated from link above'
notify = LineNotify(token)

# Send text
notify.send_text('Test send text via Line Notify')

# Send sticker
notify.send_sticker(2, 1)

# Send image
notify.send_image('https://avatars3.githubusercontent.com/u/48649457')
```

Stickers' sticker_id and package_id can be found at
https://devdocs.line.me/files/sticker_list.pdf