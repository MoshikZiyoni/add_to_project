from django.forms import ModelForm
from rest_framework.serializers import ModelSerializer
from app.models import City,Night_Life
class Night_Lifeserializers(ModelSerializer):
    class Meta:
        model = Night_Life
        fields='__all__'