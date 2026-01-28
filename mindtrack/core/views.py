from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from django.utils.dateparse import parse_date

from .models import MoodEntry
from .serializers import MoodEntrySerializer


class MoodEntryListCreateView(ListCreateAPIView):
    serializer_class = MoodEntrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = MoodEntry.objects.filter(user=self.request.user)

        # 🔍 filter by date
        date = self.request.GET.get('date')
        if date:
            queryset = queryset.filter(created_at__date=parse_date(date))

        # 🔍 filter by keyword
        keyword = self.request.GET.get('keyword')
        if keyword:
            queryset = queryset.filter(text__icontains=keyword)

        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
