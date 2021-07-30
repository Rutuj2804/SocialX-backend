from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Notification
from accounts.models import UserProfile
from accounts.serializers import UserProfileSerializer


class GetNotifications(APIView):

    def get(self, request, format=None):
        try:
            notification = Notification.objects.filter(requested_to=self.request.user)
            serializer = []
            for notify in notification:
                type = 'FRIEND' if notify.acknowledged else 'REQUESTED'
                req_user = UserProfile.objects.get(user=notify.requested_by)
                req_user = UserProfileSerializer(req_user).data
                serializer_instance = {
                    'text': type,
                    'user': req_user,
                    'id': notify.id
                }
                serializer.append(serializer_instance)
            return Response({'success': 'Successfully fetched notifications', 'notifications':serializer})
        except:
            return Response({'error': 'Something went wrong while fetching notifications'})