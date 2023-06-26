from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from notifications.enums import ActionTypes
from notifications.models import Action
from notifications.serializers import ActionSerializer


def save_action(data):
    from notifications.serializers import ActionSerializer

    serializer = ActionSerializer(data=data)
    if serializer.is_valid():
        serializer.save()


@shared_task
def send_file_edit_event(project_id, data, user_id):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "project_{}".format(project_id),
        {
            "type": "send_file_edit",
            "text": json.dumps(data),
        },
    )

    action_data = {
        "user": user_id,
        "project_id": project_id,
        "action_type": ActionTypes.FILE_EDIT.value,
    }

    save_action(action_data)
