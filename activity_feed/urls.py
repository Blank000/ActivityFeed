# notification_project/urls.py

from django.urls import path
from notifications.views import FileEditView, ActionListView

urlpatterns = [
    path('api/projects/<int:project_id>/file-edit/', FileEditView.as_view(), name='file-edit'),
    path('api/projects/<int:project_id>/actions/', ActionListView.as_view(), name='action-list'),
]

