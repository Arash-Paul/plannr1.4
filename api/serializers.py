from rest_framework import serializers
from .models import User, CreatedEvent


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField()
    profile_picture = serializers.ImageField()
    username = serializers.CharField()
    # birth_date = serializers.DateField()
    gender = serializers.CharField()
    password = serializers.CharField()
    # contact = serializers.CharField()
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = '__all__'


class UserMinFoSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    full_name = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'full_name')


class CreatedEventSerializer(serializers.ModelSerializer):
    # user_id = serializers.EmailField()
    event_name = serializers.CharField()
    event_date_time = serializers.DateTimeField()
    address = serializers.CharField()

    class Meta:
        model = CreatedEvent
        # fields = '__all__'
        fields = ('event_name', 'event_date_time', 'address')
