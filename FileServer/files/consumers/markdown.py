import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class FileConsumer(WebsocketConsumer):
    def connect(self):
        route_kwargs = self.scope.get("url_route", {}).get("kwargs", {})
        self.file_id = route_kwargs.get("file_id")
        self.file_group_name = f"file_{self.file_id}"

        async_to_sync(self.channel_layer.group_add) (
            self.file_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard) (
            self.file_group_name, self.channel_name
        )

    def receive(self, text_data: str | None = None, bytes_data: bytes | None = None):
        if not text_data:
            return
        file_data_json = json.loads(text_data)
        file = file_data_json["file"]

        self.send(text_data=json.dumps({"file": file}))

        async_to_sync(self.channel_layer.group_send) (
            self.file_group_name, {"type": "save.document", "file": file}
        )

    def save_document(self, event):
        file = event["file"]
        self.send(text_data=json.dumps({"file": file}))
