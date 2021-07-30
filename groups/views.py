from rest_framework.response import Response
from .models import Group
from .serailizers import GroupSerailizer
from rest_framework.views import APIView
from django.contrib.auth.models import User


class GroupCreateApiView(APIView):

    def post(self, request, format=None):
        try:
            data = self.request.data
            name = data['name']
            desc = data['desc']
            group = Group.objects.create(name=name, desc=desc, admin=self.request.user)
            serializer = GroupSerailizer(group)
            return Response({'success': 'successfully created group', 'group': serializer.data})
        except:
            return Response({'error': 'Something went wrong while creating group'})


class GroupEditApiView(APIView):

    def put(self, request, format=None):
        try:
            data = self.request.data
            id = data['id']
            name = data['name']
            desc = data['desc']
            group = Group.objects.get(id=id)
            if group.admin.username == self.request.user.username:
                group.name = name
                group.desc = desc
                group.save()
                serializer = GroupSerailizer(group)
                return Response({'success': 'successfully editied group', 'group': serializer.data})
            else:
                return Response({'error': 'You are not admin'})
        except:
            return Response({'error': 'Something went wrong while editing group'})


class GroupDisplayPictureApiView(APIView):

    def put(self, request, format=None):
        try:
            data = self.request.data
            id = data['id']
            photo = data['photo']
            group = Group.objects.get(id=id)
            if group.admin == self.request.user:
                group.photo = photo
                group.save()
                serializer = GroupSerailizer(group)
                return Response({'success': 'successfully edited group', 'group': serializer.data})
            else:
                return Response({'error': 'You are not admin'})
        except:
            return Response({'error': 'Something went wrong while creating group'})


class AddMemberApiView(APIView):

    def post(self, request, format=None):
        try:
            data = self.request.data
            id = data['id']
            member = data['member']
            user = User.objects.get(id=member)
            group = Group.objects.get(id=id)
            if group.admin == self.request.user:
                group.members.add(user)
                serializer = GroupSerailizer(group)
                return Response({'success': 'successfully edited group', 'group': serializer.data})
            else:
                return Response({'error': 'You are not admin'})
        except:
            return Response({'error': 'Something went wrong while adding member'})


class RemoveMemberApiView(APIView):

    def post(self, request, format=None):
        try:
            data = self.request.data
            id = data['id']
            member = data['member']
            user = User.objects.get(id=member)
            group = Group.objects.get(id=id)
            if group.admin.username == self.request.user.username:
                group.members.remove(user)
                serializer = GroupSerailizer(group)
                return Response({'success': 'successfully edited group', 'group': serializer.data})
            else:
                return Response({'error': 'You are not admin'})
        except:
            return Response({'error': 'Something went wrong while removing member'})


class LeaveGroupApiView(APIView):

    def post(self, request, format=None):
        try:
            data = self.request.data
            id = data['id']
            group = Group.objects.get(id=id)
            group.members.remove(self.request.user)
            serializer = GroupSerailizer(group)
            return Response({'success': 'successfully edited group', 'group': serializer.data})
        except:
            return Response({'error': 'Something went wrong while creating group'})


class FetchGroups(APIView):

    def get(self, request, format=None):
        try:
            user = self.request.user
            arr=[]
            groups = Group.objects.filter(members=user)
            for group in groups:
                serializer = {
                    'name': group.name,
                    'id': group.id,
                    'desc': group.desc,
                    'photo': '/media/'+str(group.photo) if group.photo else None,
                    'members': group.members.all().count()
                }
                arr.append(serializer)
            groups_my = Group.objects.filter(admin=user)
            for group in groups_my:
                serializer = {
                    'name': group.name,
                    'id': group.id,
                    'desc': group.desc,
                    'photo': '/media/'+str(group.photo) if group.photo else None,
                    'members': group.members.all().count()
                }
                arr.append(serializer)
            return Response({'group': arr,'success':'Succeffully fetched groups'})
        except:
            return Response({'error': 'Something went wrong while fetching groups'})


class FetchGroupDetailView(APIView):

    def post(self, request, format=None):
        try:
            id = self.request.data['id']
            group = Group.objects.get(id=id)
            serializer = GroupSerailizer(group)
            return Response({'group': serializer.data, 'success': 'Succeffully fetched group'})
        except:
            return Response({'error': 'Something went wrong while fetching group'})