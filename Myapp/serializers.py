from rest_framework import serializers
from .models import *

class ViewerSerializer(serializers.ModelSerializer):
    
    class Meta :
        model = Viewer
        fields = '__all__'
        
class DeveloperSerializer(serializers.ModelSerializer):
    
    class Meta :
        model = Developer
        fields = '__all__'

class AdminSerializer(serializers.ModelSerializer):
    
    class Meta :
        model = Admin
        fields = '__all__'
        

class FormSerializer(serializers.ModelSerializer):
    
    class Meta :
        model = FormSubmission
        fields = '__all__'
        