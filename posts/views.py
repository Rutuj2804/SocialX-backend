from rest_framework.response import Response
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.views import APIView
from accounts.models import UserProfile
from accounts.serializers import UserProfileSerializer
from django.contrib.auth.models import User


class AddPost(APIView):

    def post(self, request, format=None):
        try:
            data = self.request.data
            user = self.request.user
            title = data['title']
            image = data['image']
            if image:
                post = Post.objects.create(title=title, admin=user, image=image)
            else:
                post = Post.objects.create(title=title, admin=user)
            serializer = PostSerializer(post)
            return Response({'success': 'Successfully created post', 'post': serializer.data})
        except:
            return Response({'error': 'Something went wrong while adding post'})


class GetPosts(APIView):

    def get(self, request, format=None):
        try:
            posts = Post.objects.all()
            serializer = []
            user_profile = UserProfile.objects.get(user=self.request.user)
            for post in posts:
                post_user = UserProfile.objects.get(user=post.admin)
                serial_instance = {
                    "id":post.id,
                    "title": post.title,
                    "full_name": post.admin.first_name+' '+post.admin.last_name,
                    "username": post.admin.username,
                    "created_at": post.created_at,
                    "likes": post.likes.all().count(),
                    "image": "/media/"+str(post.image) if post.image else None,
                    "profileimage": "/media/"+str(post_user.photo) if post_user.photo else None,
                    "isLiked": post.likes.filter(username=self.request.user).exists(),
                    "comments": post.comments.all().count(),
                    "isBookmarked": user_profile.bookmark.filter(id=post.id).exists()
                }
                serializer.append(serial_instance)
                serializer.reverse()
            return Response({'success': 'Successfully fetched post', 'post': serializer})
        except:
            return Response({'error': 'Something went wrong while adding post'})


class GetMyProfilePosts(APIView):

    def get(self, request, format=None):
        try:
            posts = Post.objects.filter(admin=self.request.user)
            serializer = []
            user_profile = UserProfile.objects.get(user=self.request.user)
            for post in posts:
                serial_instance = {
                    "id":post.id,
                    "title": post.title,
                    "full_name": post.admin.first_name+' '+post.admin.last_name,
                    "username": post.admin.username,
                    "created_at": post.created_at,
                    "likes": post.likes.all().count(),
                    "image": "/media/"+str(post.image) if post.image else None,
                    "isLiked": post.likes.filter(username=self.request.user).exists(),
                    "profileimage": "/media/"+str(user_profile.photo) if user_profile.photo else None,
                    "comments": post.comments.all().count(),
                    "isBookmarked": user_profile.bookmark.filter(id=post.id).exists()
                }
                serializer.append(serial_instance)
                serializer.reverse()
            return Response({'success': 'Successfully fetched post', 'post': serializer})
        except:
            return Response({'error': 'Something went wrong while adding post'})


class GetOthersProfilePosts(APIView):

    def post(self, request, format=None):
        try:
            data = self.request.data['username']
            user = User.objects.get(username=data)
            posts = Post.objects.filter(admin=user)
            serializer = []
            user_profile = UserProfile.objects.get(user=user)
            for post in posts:
                post_user = UserProfile.objects.get(user=post.admin)
                serial_instance = {
                    "id":post.id,
                    "title": post.title,
                    "full_name": post.admin.first_name+' '+post.admin.last_name,
                    "username": post.admin.username,
                    "created_at": post.created_at,
                    "profileimage": "/media/"+str(post_user.photo) if post_user.photo else None,
                    "likes": post.likes.all().count(),
                    "image": "/media/"+str(post.image) if post.image else None,
                    "isLiked": post.likes.filter(username=user).exists(),
                    "comments": post.comments.all().count(),
                    "isBookmarked": user_profile.bookmark.filter(id=post.id).exists()
                }
                serializer.append(serial_instance)
                serializer.reverse()
            return Response({'success': 'Successfully fetched post', 'post': serializer})
        except:
            return Response({'error': 'Something went wrong while adding post'})


class GetPostDetailView(APIView):

    def post(self, request, format=None):
        try:
            id = self.request.data['id']
            post = Post.objects.get(id=id)
            comments = post.comments.all()
            arr=[]
            for comment in comments:
                userprofile = UserProfile.objects.get(user=comment.admin)
                userprofile = UserProfileSerializer(userprofile).data
                serial_comment = {
                    "user": userprofile,
                    "comment": comment.comment
                }
                arr.append(serial_comment)
            serializer = {
                'id': post.id,
                'title': post.title,
                'admin': post.admin.username,
                "full_name": post.admin.first_name+' '+post.admin.last_name,
                'created_at': post.created_at,
                "username": post.admin.username,
                "image": "/media/"+str(post.image) if post.image else None,
                'likes': post.likes.all().count(),
                'comments': arr,
                'isLiked': post.likes.filter(username=self.request.user).exists()
            }
            return Response({'success': 'Successfully fetched post', 'post': serializer})
        except:
            return Response({'error': 'Something went wrong while adding post'})


class DeletePost(APIView):

    def delete(self, request, format=None):
        try:
            data = self.request.data
            user = self.request.user
            id = data['id']
            post = Post.objects.get(id=id)
            if post.admin.username == user.username:
                Post.objects.filter(id=id).delete()
                return Response({'success': 'Successfully deleted post'})
            return Response({'error': 'You are not creator of this post'})
        except:
            return Response({'error': 'Something went wrong while adding post'})


class AddCommentInPost(APIView):

    def post(self, request, format=None):
        try:
            data = self.request.data
            user = self.request.user
            id = data['id']
            comment = data['comment']
            comment_obj = Comment.objects.create(admin=user, comment=comment)
            post_obj = Post.objects.get(id=id)
            post_obj.comments.add(comment_obj)
            serializer = CommentSerializer(comment_obj)
            return Response({'success': 'Successfully created comment', 'comment': serializer.data})
        except:
            return Response({'error': 'Something went wrong while adding comment'})


class AddLikeInPost(APIView):

    def post(self, request, format=None):
        try:
            data = self.request.data
            user = self.request.user
            id = data['id']
            post_obj = Post.objects.get(id=id)
            if post_obj.likes.filter(username=user.username).exists():
                post_obj.likes.remove(user)
            else:
                post_obj.likes.add(user)
            return Response({'success': 'Successfully fulfilled request'})
        except:
            return Response({'error': 'Something went wrong while adding like'})