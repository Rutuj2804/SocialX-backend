from django.urls import path
from .views import RegisterUser, CheckAuthentication, GetUserApiView, GetOtherUserApiView, EditDisplayPictureApiView, EditUserApiView, FilterUserApiView, AddFollowRequestApiView, AcceptFollowRequestApiView, DeleteFollowRequestApiView, AddBookmark, FetchBookmarks, GetFriendListFive, UnfollowRequestApiView

urlpatterns = [
    path('register/', RegisterUser.as_view()),
    path('edit/', EditUserApiView.as_view()),
    path('filter/', FilterUserApiView.as_view()),
    path('edit-dp/', EditDisplayPictureApiView.as_view()),
    path('check-auth/', CheckAuthentication.as_view()),
    path('get/', GetUserApiView.as_view()),
    path('get-other/', GetOtherUserApiView.as_view()),
    path('follow-request/', AddFollowRequestApiView.as_view()),
    path('unfollow-request/', UnfollowRequestApiView.as_view()),
    path('accept-request/', AcceptFollowRequestApiView.as_view()),
    path('delete-request/', DeleteFollowRequestApiView.as_view()),
    path('add-bookmark/', AddBookmark.as_view()),
    path('fetch-bookmark/', FetchBookmarks.as_view()),
    path('get-list/', GetFriendListFive.as_view())
]