import requests
import random
import json
import vk

session = vk.Session()
api = vk.API(session, v=5.0)


def get_random_wall_picture(group_id, token):
    max_num = api.photos.get(
        owner_id=group_id, album_id="wall", count=0, access_token=token
    )["count"]
    num = random.randint(1, max_num)
    photo = api.photos.get(
        owner_id=str(group_id), album_id="wall", count=1, offset=num, access_token=token
    )["items"][0]["id"]
    attachment = "photo" + str(group_id) + "_" + str(photo)
    return attachment


def send_message(user_id, token, message, attachment="", file=None):
    if file:
        _send_photo(user_id, token, message, file)
    else:
        api.messages.send(
            access_token=token,
            user_id=str(user_id),
            message=message,
            attachment=attachment,
        )


def _send_photo(user_id, token, message, file):
    openedfile = open(file, "rb")
    files = {"file": openedfile}
    fileonserver = json.loads(
        requests.post(
            api.photos.getMessagesUploadServer(access_token=token)["upload_url"],
            files=files,
        ).text
    )
    attachment = api.photos.saveMessagesPhoto(
        access_token=token,
        server=fileonserver["server"],
        photo=fileonserver["photo"],
        hash=fileonserver["hash"],
    )
    attachment = f'photo{attachment[0]["owner_id"]}_{attachment[0]["id"]}'
    if message:
        api.messages.send(
            access_token=token, user_id=user_id, message=message, attachment=attachment
        )
    else:
        api.messages.send(access_token=token, user_id=user_id, attachment=attachment)
    openedfile.close()
