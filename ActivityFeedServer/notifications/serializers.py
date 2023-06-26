from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Action


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = "__all__"


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data["username"])
        user.set_password(validated_data["password"])
        user.save()
        return user
