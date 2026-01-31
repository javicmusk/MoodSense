from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from django.utils.dateparse import parse_date

from .models import MoodEntry
from .serializers import MoodEntrySerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer

from .ai import analyze_mood 


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
        text = serializer.validated_data.get("text")

        mood, confidence = analyze_mood(text)

        serializer.save(
            user=self.request.user,
            detected_mood=mood,
            confidence_score=round(confidence, 3)
        )


#for signup
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#signup API view
from .serializers import SignupSerializer
class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#get logged-in user
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "id": request.user.id,
            "username": request.user.username,
            "email": request.user.email
        })
    
class AnalyzeMoodView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        text = request.data.get("text")

        if not text:
            return Response(
                {"error": "Text is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        mood, confidence = analyze_mood(text)
        return Response({
            "detected_mood": mood,
            "confidence_score": confidence,
            "message": "Mood analyzed successfully"
        })
   
    


