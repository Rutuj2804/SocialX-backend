from django.urls import path
from .views import AddPost, DeletePost, AddCommentInPost, AddLikeInPost, GetPosts, GetPostDetailView, GetMyProfilePosts, GetOthersProfilePosts

urlpatterns = [
    path('add/', AddPost.as_view()),
    path('delete/', DeletePost.as_view()),
    path('comment/', AddCommentInPost.as_view()),
    path('like/', AddLikeInPost.as_view()),
    path('get-all/', GetPosts.as_view()),
    path('get/', GetPostDetailView.as_view()),
    path('get-my/', GetMyProfilePosts.as_view()),
    path('get-other/', GetOthersProfilePosts.as_view()),
]