from django.forms import ModelForm
from .models import ForumRoom, Topic


class ForumRoomForm(ModelForm):
    
    class Meta:
        model = ForumRoom
        fields = "__all__"
        exclude = ['creator', 'participiants']
        
class TopicForm(ModelForm):
    
    class Meta:
        model = Topic
        fields = "__all__"
