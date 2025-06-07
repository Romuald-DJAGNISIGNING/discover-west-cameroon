

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomSession
from .serializers import CustomSessionSerializer

class CustomSessionListCreateView(generics.ListCreateAPIView):
    queryset = CustomSession.objects.all()
    serializer_class = CustomSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

class CustomSessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomSession.objects.all()
    serializer_class = CustomSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only allow users to see sessions they are involved in
        user = self.request.user
        return CustomSession.objects.filter(student=user) | CustomSession.objects.filter(tutor=user)

class ConfirmSessionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            session = CustomSession.objects.get(pk=pk)
        except CustomSession.DoesNotExist:
            return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)

        if request.user != session.tutor:
            return Response({"error": "Only the tutor can confirm the session"}, status=status.HTTP_403_FORBIDDEN)

        session.confirmed = True
        session.save()
        return Response({"success": "Session confirmed"}, status=status.HTTP_200_OK)
