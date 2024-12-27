from asgiref.sync import async_to_sync
from project.celery import app
from channels.layers import get_channel_layer
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist

from ticket.models import Service, Incident, Maintenance, Update


def send_websocket_update(message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)("updates", {"type": "send_update", "message": message})


def get_instance_message(instance, model, created):
    if model is Service:
        message = {
            "service_id": instance.id,
            "message": f"{'created' if created else 'updated'} service {instance.name}",
        }
    else:
        name = model.__name__.lower()
        message = {
            "service_id": instance.service_id,
            f"{name}_id": instance.id,
            "message": (
                f"{instance.created_by if created else instance.updated_by}"
                f" {'created' if created else 'updated'} {name} {instance.title}"
            ),
        }
    return message


def create_log(instance, model, remark):
    data = {
        f"{model.__name__.lower()}": instance,
        "status": instance.status,
        "update_text": remark,
        "created_at": instance.updated_at,
        "updated_by": instance.updated_by,
    }
    # creating a log for incident and maintenance
    Update.objects.create(**data)


@app.task
def send_model_updates(instance_id, model_name, created, remark):
    try:
        content_type = ContentType.objects.get(model=model_name.lower())
        model = content_type.model_class()
        instance = model.objects.get(id=instance_id)
    except ObjectDoesNotExist:
        return f"data not for id {instance_id} of {model_name}"
    else:
        if model in (Incident, Maintenance):
            if not created:
                create_log(instance, model, remark)
        message = get_instance_message(instance, model, created)
        send_websocket_update(message)
        return f"sent {message} via websocket"
