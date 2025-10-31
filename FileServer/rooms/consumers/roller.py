import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import redis

r = redis.Redis(host="localhost", port=6379, db=0)

class RollerConsumer(WebsocketConsumer):
    def connect(self):
        route_kwargs = self.scope.get("url_route", {}).get("kwargs", {})
        self.room_name = route_kwargs.get("room_name", "none")
        user = self.scope.get("user", None)
        print("DEBUG user:", user)
        print("Authenticated:", getattr(user, "is_authenticated", False))
        if self.room_name is None:
            return

        async_to_sync(self.channel_layer.group_add) (
            self.room_name, self.channel_name
        )
        user = self.scope.get("user")
        if not user or not getattr(user, "is_authenticated", False):
            self.close(code=4003)
            return
        else:
            username = user.username

        self.accept()

        r.sadd(f"room:{self.room_name}:users", username)

        async_to_sync(self.channel_layer.group_send) (
            self.room_name, {"type": "members.load"}
        )


    def disconnect(self, code):
        user = self.scope.get("user", None)
        if not user or not getattr(user, "is_authenticated", False):
            username = "Anonymous"
        else:
            username = user.username

        r.srem(f"room:{self.room_name}:users", username)
        if len(r.smembers(f"room:{self.room_name}:users")) == 0:
            async_to_sync(self.channel_layer.group_discard) (
                self.room_name, self.channel_name
            )
        else:
            async_to_sync(self.channel_layer.group_send) (
                self.room_name, {"type": "members.load"}
            )

        self.close()


    def receive(self, text_data: str | None = None, bytes_data: bytes | None = None):
        if not text_data:
            return
        roll_data_json = json.loads(text_data)
        contents = roll_data_json["contents"]

        context = {
            'contents': contents,
            'id': id,
        }

        self.send(text_data=json.dumps({"file": context}))

        async_to_sync(self.channel_layer.group_send) (
            self.room_name, {"type": "roll", "file": context}
        )

    def members_load(self, event):
        current_members = r.smembers(f"room:{self.room_name}:users")
        print(current_members)
        current_members = [m.decode("utf-8") for m in current_members]
        print(current_members)
        self.send(text_data=json.dumps({"type": "load.users", "users": current_members}))
