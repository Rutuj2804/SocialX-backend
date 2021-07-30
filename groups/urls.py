from django.urls import path
from .views import GroupCreateApiView, GroupEditApiView, GroupDisplayPictureApiView, AddMemberApiView, RemoveMemberApiView, LeaveGroupApiView, FetchGroups, FetchGroupDetailView

urlpatterns = [
    path('create/', GroupCreateApiView.as_view()),
    path('edit/', GroupEditApiView.as_view()),
    path('edit-dp/', GroupDisplayPictureApiView.as_view()),
    path('add-member/', AddMemberApiView.as_view()),
    path('remove-member/', RemoveMemberApiView.as_view()),
    path('leave/', LeaveGroupApiView.as_view()),
    path('fetch/', FetchGroups.as_view()),
    path('fetch-detail/', FetchGroupDetailView.as_view()),
]