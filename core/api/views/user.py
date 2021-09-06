from .. import serializers
from .. import utils
from rest_framework import generics, mixins, permissions
from rest_framework.views import APIView
from ... import models
from rest_framework.response import Response


class UserDetail(generics.RetrieveAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_field = 'username'

class UserMe(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        serializer = serializers.UserSerializer(request.user)
        return Response(serializer.data)

class UserMeSchedule(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        date = utils.parse_date_query_param(request)
        ongoing_timetables = request.user.get_ongoing_timetables()

        result = []

        for timetable in ongoing_timetables:
            result.extend(timetable.day_schedule(target_date=date))

        result.sort(key=lambda x: (x['time']['start'], x['time']['end']))

        return Response(result)