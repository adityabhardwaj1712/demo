from rest_framework import serializers
from .models import Organization, Membership


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["id", "name", "created_at"]


class MembershipSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Membership
        fields = ["id", "user", "role"]


class AddMemberSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    role = serializers.ChoiceField(
        choices=["ADMIN", "DEVELOPER", "VIEWER"]
    )