from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import SupportTicket, SupportMessage
from .serializers import SupportTicketSerializer, SupportMessageSerializer
from .permissions import IsTicketOwnerOrStaffOrReadOnly

class SupportTicketViewSet(viewsets.ModelViewSet):
    queryset = SupportTicket.objects.all().order_by('-created_at')
    serializer_class = SupportTicketSerializer
    permission_classes = [permissions.IsAuthenticated, IsTicketOwnerOrStaffOrReadOnly]
    filterset_fields = ['priority', 'status', 'village', 'attraction', 'festival', 'created_by', 'assigned_to']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_message(self, request, pk=None):
        ticket = self.get_object()
        serializer = SupportMessageSerializer(data=request.data, partial=True)  # Add partial=True
        if serializer.is_valid():
            serializer.save(ticket=ticket, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)


    @action(detail=True, methods=['post'], permission_classes=[IsTicketOwnerOrStaffOrReadOnly])
    def assign(self, request, pk=None):
        ticket = self.get_object()
        user_id = request.data.get("assigned_to")
        if user_id:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            try:
                user = User.objects.get(pk=user_id)
                ticket.assigned_to = user
                ticket.save()
                return Response({"status": "assigned", "id": ticket.id})
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=400)
        else:
            ticket.assigned_to = None
            ticket.save()
            return Response({"status": "assignment cleared", "id": ticket.id})


    @action(detail=True, methods=['post'], permission_classes=[IsTicketOwnerOrStaffOrReadOnly])
    def resolve(self, request, pk=None):
        ticket = self.get_object()
        ticket.status = 'resolved'
        ticket.resolution = request.data.get("resolution", "")
        ticket.save()
        return Response({"status": "resolved", "id": ticket.id})

    @action(detail=True, methods=['post'], permission_classes=[IsTicketOwnerOrStaffOrReadOnly])
    def close(self, request, pk=None):
        ticket = self.get_object()
        ticket.status = 'closed'
        ticket.resolution = request.data.get("resolution", "")
        ticket.save()
        return Response({"status": "closed", "id": ticket.id})

class SupportMessageViewSet(viewsets.ModelViewSet):
    queryset = SupportMessage.objects.all().order_by('created_at')
    serializer_class = SupportMessageSerializer
    permission_classes = [permissions.IsAuthenticated]