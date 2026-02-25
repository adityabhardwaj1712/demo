from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Organization, Membership
from .serializers import (
    OrganizationSerializer,
    MembershipSerializer,
    AddMemberSerializer,
)
from accounts.models import User
from .permissions import is_org_admin


class OrganizationListCreateView(APIView):
    def get(self, request):
        orgs = Organization.objects.filter(
            membership__user=request.user
        ).distinct()
        return Response(OrganizationSerializer(orgs, many=True).data)

    def post(self, request):
        serializer = OrganizationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        org = serializer.save(owner=request.user)
        Membership.objects.create(
            user=request.user,
            organization=org,
            role="admin",
        )

        return Response(serializer.data, status=201)


class OrganizationMembersView(APIView):
    def get(self, request, org_id):
        if not Membership.objects.filter(
            user=request.user,
            organization_id=org_id,
        ).exists():
            return Response({"detail": "Forbidden"}, status=403)

        members = Membership.objects.filter(organization_id=org_id)
        return Response(MembershipSerializer(members, many=True).data)


class AddMemberView(APIView):
    def post(self, request, org_id):
        if not is_org_admin(request.user, org_id):
            return Response({"detail": "Admins only"}, status=403)

        serializer = AddMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(id=serializer.validated_data["user_id"])

        Membership.objects.create(
            user=user,
            organization_id=org_id,
            role=serializer.validated_data["role"],
        )

        return Response({"status": "member added"})