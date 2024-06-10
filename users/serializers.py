from django.db.models import Q
from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from users.models import CustomUser


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'username', 'email', 'password')


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'password')

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        if username and password:
            user = CustomUser.objects.filter(Q(username=username) |
                                             Q(email=username)).first()
            if user and check_password(password, user.password):
                return user

        else:
            msg = "Должно включать 'username_or_email' и 'password'"
            raise serializers.ValidationError(msg, code='authorization')
        msg = "Неверное имя пользователя или пароль"
        raise serializers.ValidationError(msg, code='authorization')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "phone",
            "billing_address",
            "shipping_address",
            "birth_date",
            "age"
        )


class TokenObtainPairResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()
