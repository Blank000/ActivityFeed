from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .serializers import ActionSerializer
from .models import Action

class FileEditView(APIView):
    def post(self, request):
        project_id = request.data.get('project_id')

        # Notify all users in the project's room
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'project_{}'.format(project_id),
            {
                'type': 'send_file_edit',
                'text': request.data,
                'action_data': {
                    'project_id': project_id,
                    'action_type': 'File Edit'
                }
            }
        )

        return Response({'message': 'File edit event sent'})

class ActionListView(APIView):
    def get(self, request, project_id):
        actions = Action.objects.filter(project_id=project_id).order_by('-timestamp')
        serializer = ActionSerializer(actions, many=True)
        return Response(serializer.data)

