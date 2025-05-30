from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from srs.srsapi.models import Word


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = [
            "id",
            "text",
            "last_reviewed",
            "next_review",
            "repetitions",
        ]
        read_only_fields = [
            "id",
            "text",
            "owner",
            "last_reviewed",
            "next_review",
            "repetitions",
        ]


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="A user with that email already exists.",
            )
        ],
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],  # Django's built-in password validators
    )
    password2 = serializers.CharField(
        write_only=True, required=True
    )  # For password confirmation

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "password2",
        )  # Add any other fields you want to collect

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"], email=validated_data["email"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
