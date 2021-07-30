from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import UserProfile
from .serializers import UserProfileSerializer
from notifications.models import Notification
from posts.models import Post
from posts.serializers import PostSerializer


class GetUserApiView(APIView):

    def get(self, request, format=None):
        try:
            user = self.request.user
            user_profile = UserProfile.objects.get(user=user)
            serializer = UserProfileSerializer(user_profile)
            return Response({'success': 'Successfully fetched user', 'user': serializer.data})
        except:
            return Response({'error': 'Something went wrong while fetching user'})


class GetOtherUserApiView(APIView):

    def post(self, request, format=None):
        try:
            user = User.objects.get(username=self.request.data['username'])
            user_profile = UserProfile.objects.get(user=user)
            serializer = UserProfileSerializer(user_profile)
            return Response({'success': 'Successfully fetched user', 'user': serializer.data})
        except:
            return Response({'error': 'Something went wrong while fetching user'})


class RegisterUser(APIView):
    permission_classes = [AllowAny,]

    def post(self, request, format=None):
        data = self.request.data
        try:
            first_name = data['first_name']
            last_name = data['last_name']
            email = data['email']
            username = data['username']
            password = data['password']
            re_password = data['re_password']
            if password == re_password:
                if first_name != '' and last_name != '' and username != '':
                    if User.objects.filter(username=username).exists():
                        return Response({'error': 'user already exists'})
                    else:
                        user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username,
                                                        password=password, email=email)
                        UserProfile.objects.create(user=user)
                        Token.objects.create(user=user)
                        return Response({'success': 'Successfully created user'})
                else:
                    return Response({'error': 'Each field is necessary'})
            else:
                return Response({'error': 'passwords do not match'})
        except:
            return Response({'error': 'Something went wrong while registering'})


class EditUserApiView(APIView):

    def put(self, request, format=None):
        data = self.request.data
        try:
            user = self.request.user
            first_name = data['first_name']
            last_name = data['last_name']
            email = data['email']
            username = data['username']
            User.objects.filter(username=user.username).update(first_name=first_name, last_name=last_name, email=email, username=username)
            return Response({'success': 'Successfully updated user'})
        except:
            return Response({'error': 'Something went wrong while updating'})


class EditDisplayPictureApiView(APIView):

    def put(self, request, format=None):
        data = self.request.data
        try:
            user = self.request.user
            photo = data['photo']
            user_profile = UserProfile.objects.get(user=user)
            user_profile.photo = photo
            user_profile.save()
            return Response({'success': 'Successfully updated photo'})
        except:
            return Response({'error': 'Something went wrong while updating'})


class CheckAuthentication(APIView):
    permission_classes = [AllowAny,]

    def get(self, request, format=None):
        try:
            user = self.request.user
            if User.objects.filter(username=user).exists():
                return Response({'success': 'IsAuthenticated'})
            else:
                return Response({'error': 'Not Authenticated'})
        except:
            return Response({'error': 'Not Authenticated'})


class GetFriendListFive(APIView):

    def get(self, request, format=None):
        try:
            user_list = UserProfile.objects.all()[0:5]
            serial = []
            for user in user_list:
                serializer = {
                    'username': user.user.username,
                    'full_name': user.user.first_name + ' ' + user.user.last_name,
                    'photo': '/media/'+str(user.photo) if user.photo else None
                }
                serial.append(serializer)
            return Response({'success': 'Successfully fetched list', 'user': serial})
        except:
            return Response({'error': 'Something went wrong while fetching list'})


# add follow request
class AddFollowRequestApiView(APIView):

    def post(self, request, format=None):
        try:
            data = self.request.data
            username = data['username']
            username = User.objects.get(username=username)
            user = self.request.user
            Notification.objects.create(requested_by=user, requested_to=username)
            return Response({'success': 'Successfully requested to follow user'})
        except:
            return Response({'error': 'Something went wrong while following'})


# accept follow request
class AcceptFollowRequestApiView(APIView):

    def post(self, request, format=None):
        try:
            data = self.request.data
            notification = data['notification']
            notification = Notification.objects.get(id=notification)
            notification.acknowledged = True
            notification.save()
            myuser_profile = UserProfile.objects.get(user=self.request.user.id)
            myuser_profile.following.add(notification.requested_by.id)
            oppuser_profile = UserProfile.objects.get(user=notification.requested_by.id)
            oppuser_profile.followers.add(self.request.user.id)
            return Response({'success': 'Successfully followed user'})
        except:
            return Response({'error': 'Something went wrong while following'})


# unfollow
class UnfollowRequestApiView(APIView):

    def post(self, request, format=None):
        try:
            data = self.request.data
            user = self.request.user
            username = data['username']
            user_instance=User.objects.get(username=username)
            myuser_profile = UserProfile.objects.get(user=self.request.user.id)
            myuser_profile.following.add(user_instance)
            user_opp = UserProfile.objects.get(user=user_instance.id)
            user_opp.followers.remove(user)
            return Response({'success': 'Successfully followed user'})
        except:
            return Response({'error': 'Something went wrong while following'})


# delete follow request
class DeleteFollowRequestApiView(APIView):

    def delete(self, request, format=None):
        try:
            data = self.request.data
            notification = data['notification']
            notification = Notification.objects.get(id=notification)
            notification.delete()
            return Response({'success': 'Successfully deleted request'})
        except:
            return Response({'error': 'Something went wrong while following'})


class FilterUserApiView(APIView):

    def post(self, request, format=None):
        try:
            data = self.request.data
            username = data['username']
            username = User.objects.filter(username__icontains=username)
            serializer = []
            for user in username:
                serial_instance = {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "username": user.username,
                    "id": user.id
                }
                serializer.append(serial_instance)
            return Response({'success': 'successfully filtered users', 'user': serializer})
        except:
            return Response({'error': 'Something went wrong while filtering user'})


class AddBookmark(APIView):

    def post(self, request, format=None):
        try:
            data = self.request.data
            id = data['id']
            user_profile = UserProfile.objects.get(user=self.request.user)
            post = Post.objects.get(id=id)
            if user_profile.bookmark.filter(id=id).exists():
                user_profile.bookmark.remove(post)
                return Response({'success': 'successfully removed as bookmark'})
            else:
                user_profile.bookmark.add(post)
                return Response({'success': 'successfully added as bookmark'})
        except:
            return Response({'error': 'Something went wrong while adding bookmark'})


class FetchBookmarks(APIView):

    def get(self, request, format=None):
        try:
            user_profile = UserProfile.objects.get(user=self.request.user)
            serializer = []
            for post in user_profile.bookmark.all():
                post_user = UserProfile.objects.get(user=post.admin)
                serializer_instance = {
                        "id":post.id,
                        "title": post.title,
                        "full_name": post.admin.first_name+' '+post.admin.last_name,
                        "created_at": post.created_at,
                        "likes": post.likes.all().count(),
                        "username": post.admin.username,
                        "image": "/media/"+str(post.image) if post.image else None,
                        "profileimage": "/media/"+str(post_user.photo) if post_user.photo else None,
                        "isLiked": post.likes.filter(username=self.request.user).exists(),
                        "comments": post.comments.all().count(),
                        "isBookmarked": user_profile.bookmark.filter(id=post.id).exists()
                    }
                serializer.append(serializer_instance)
            return Response({'success': 'successfully fetched as bookmark', 'bookmarks': serializer})
        except:
            return Response({'error': 'Something went wrong while fetching bookmark'})