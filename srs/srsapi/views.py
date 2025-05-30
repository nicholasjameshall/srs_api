from datetime import timedelta

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from srs.srsapi.models import Word
from srs.srsapi.permissions import IsOwnerOfObject
from srs.srsapi.serializers import RegisterSerializer, WordSerializer


class WordViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows words to be viewed or edited.
    """

    queryset = Word.objects.all().order_by("-last_reviewed")
    serializer_class = WordSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOfObject]

    def perform_create(self, serializer):
        # Automatically set the owner to the current authenticated user
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Word.objects.filter(owner=self.request.user).order_by("-last_reviewed")

    @action(detail=True, methods=["post"], url_path="reviewed")
    def word_reviewed(self, request, pk=None):
        """
        Marks a word as reviewed and updates its review schedule.
        """
        word = self.get_object()

        word.last_reviewed = timezone.now()
        word.repetitions += 1
        word.next_review = word.last_reviewed + timedelta(days=2**word.repetitions)

        word.save()  # Save the updated word

        # Return the updated word instance. You can serialize it to show the new values.
        serializer = self.get_serializer(word)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterView(generics.CreateAPIView):
    """
    API endpoint that allows new users to register.
    """

    queryset = User.objects.all()  # No need to filter for specific users here
    permission_classes = (AllowAny,)  # Allow unauthenticated users to register
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()  # This calls the create method in the serializer

        token_serializer = TokenObtainPairSerializer(
            data={
                "username": user.username,
                "password": request.data["password"],
            }
        )
        token_serializer.is_valid(raise_exception=True)
        tokens = token_serializer.validated_data

        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                "user": serializer.data,
                "tokens": tokens,
            },  # Return user data and tokens
            status=status.HTTP_201_CREATED,
            headers=headers,
        )
