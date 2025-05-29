from rest_framework import serializers
from .models import Game
from django.contrib.auth.models import User

class GameSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # albo `UserSerializer` jeśli chcesz pełne info

    class Meta:
        model = Game
        fields = '__all__'  # albo wypisz wszystkie pola w tym `user`

    def create(self, validated_data):
        # Tutaj automatycznie przypisz usera z kontekstu request
        user = self.context['request'].user
        return Game.objects.create(user=user, **validated_data)
    
class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Hasła nie są takie same.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')  # usuwa zanim utworzy usera
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user
