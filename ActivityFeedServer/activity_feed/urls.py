# notification_project/urls.py

from django.urls import path
from notifications.views import ActionListView, FileEditView, UserRegistrationView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("user/register/", UserRegistrationView.as_view(), name="user-registration"),
    path("user/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("user/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "projects/<int:project_id>/file-edit/", FileEditView.as_view(), name="file-edit"
    ),
    path(
        "projects/<int:project_id>/action-feed/",
        ActionListView.as_view(),
        name="action-list",
    ),
]
