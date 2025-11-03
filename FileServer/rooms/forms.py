from django import forms

class JoinRoomForm(forms.Form):
    room_code = forms.CharField(max_length=20, label="Room Code")

