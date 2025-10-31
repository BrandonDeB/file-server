import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from ..models import (
    File,
)

class FileConsumer(WebsocketConsumer):
    def connect(self):
        route_kwargs = self.scope.get("url_route", {}).get("kwargs", {})
        self.file_id = route_kwargs.get("file_id")
        self.file_group_name = f"file_{self.file_id}"
        file_obj = File.objects.get(id=self.file_id)
        if not file_obj.can_access(self.scope["user"].client):
            print("Cannot access this file")
            self.close(code=4003) 
            return
        async_to_sync(self.channel_layer.group_add) (
            self.file_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard) (
            self.file_group_name, self.channel_name
        )
        self.close()

    def receive(self, text_data: str | None = None, bytes_data: bytes | None = None):
        if not text_data:
            return
        file_data_json = json.loads(text_data)
        contents = file_data_json["contents"]
        id = file_data_json["file_id"]

        file_obj = File.objects.get(id=id)
        if not file_obj.can_access(self.scope["user"].client):
            print("Cannot access this file")
            self.close()
            return
        with open(file_obj.upload.path, "w") as writer:
            writer.write(contents)

        context = {
            'name': file_obj.upload.url,
            'contents': contents,
            'id': id,
        }

        self.send(text_data=json.dumps({"file": context}))

        async_to_sync(self.channel_layer.group_send) (
            self.file_group_name, {"type": "save.document", "file": context}
        )

    def save_document(self, event):
        file = event["file"]
        file_obj = File.objects.get(id=file['id'])
        if not file_obj.can_access(self.scope.get("user").client):
            self.close()
            return
        self.send(text_data=json.dumps({"file": file}))
