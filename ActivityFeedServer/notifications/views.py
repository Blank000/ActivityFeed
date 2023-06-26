from notifications.models import Action
from notifications.serializers import ActionSerializer, UserRegistrationSerializer
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from notifications.tasks import send_file_edit_event


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileEditView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, project_id):
        # Notify all users in the project's room

        data = request.data

        # Trigger the Celery task to send the file edit event asynchronously
        send_file_edit_event.delay(project_id, data, request.user.id)

        return Response({"message": "File edit event triggered"})


class ActionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        actions = Action.objects.filter(project_id=project_id).order_by("-timestamp")
        serializer = ActionSerializer(actions, many=True)
        return Response(serializer.data)
