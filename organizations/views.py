from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Organization, Membership
from .serializers import (
    OrganizationSerializer,
    MembershipSerializer,
    AddMemberSerializer,
)
from accounts.models import User
from .permissions import is_org_admin


class OrganizationListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orgs = Organization.objects.filter(
            memberships__user=request.user
        ).distinct()

        return Response(
            OrganizationSerializer(orgs, many=True).data
        )

    def post(self, request):
        serializer = OrganizationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        org = serializer.save(owner=request.user)

        Membership.objects.create(
            user=request.user,
            organization=org,
            role="ADMIN",
        )

        return Response(
            OrganizationSerializer(org).data,
            status=status.HTTP_201_CREATED
        )


class OrganizationMembersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        if not Membership.objects.filter(
            user=request.user,
            organization_id=pk,
        ).exists():
            return Response({"detail": "Forbidden"}, status=403)

        members = Membership.objects.filter(organization_id=pk)

        return Response(
            MembershipSerializer(members, many=True).data
        )


class AddMemberView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        if not is_org_admin(request.user, pk):
            return Response({"detail": "Admins only"}, status=403)

        serializer = AddMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(id=serializer.validated_data["user_id"])

        if Membership.objects.filter(user=user, organization_id=pk).exists():
            return Response({"detail": "Already a member"}, status=400)

        Membership.objects.create(
            user=user,
            organization_id=pk,
            role=serializer.validated_data["role"],
        )

        return Response({"status": "member added"})