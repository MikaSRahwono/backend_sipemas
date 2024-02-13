from rest_framework import serializers
from .models import *

class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    fields = FieldSerializer(read_only=True,many=True)
    
    class Meta:
        model = UserProfile
        fields = ['name', 'major', 'about', 'profile_image', 'line_id', 'linkedin_url', 'github_url', 'is_open', 'fields']

    def create(self,validated_data):
        fields = self.initial_data['fields']
        fieldsInstances = []
        
        for field in fields:
            fieldsInstances.append(Field.objects.get(id = field['id']))
        user_profile = UserProfile.objects.create(**validated_data)
        user_profile.fields.set(fieldsInstances)

        return user_profile
    
    def update(self, instance, validated_data):
        try: 
            fields = self.initial_data['fields']
            fieldsInstances = []
            for field in fields:
                fieldsInstances.append(Field.objects.get(pk = field['id']))
            instance.fields.set(fieldsInstances) 

        except:
            pass
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()
        return instance
    
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetail
        fields = ['email', 'kode_identitas', 'role', 'is_external']

class UserSerializer(serializers.ModelSerializer):
    user_detail = UserDetailSerializer(read_only=True)
    user_profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_detail', 'user_profile']

