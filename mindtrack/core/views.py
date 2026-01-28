from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.dateparse import parse_date

from .models import MoodEntry
from .serializers import MoodEntrySerializer


class MoodEntryCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MoodEntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class MoodEntryListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = MoodEntry.objects.filter(user=request.user)

        # 🔍 Filter by date
        date = request.GET.get('date')
        if date:
            queryset = queryset.filter(created_at__date=parse_date(date))

        # 🔍 Filter by keyword
        keyword = request.GET.get('keyword')
        if keyword:
            queryset = queryset.filter(text__icontains=keyword)

        serializer = MoodEntrySerializer(queryset.order_by('-created_at'), many=True)
        return Response(serializer.data)
