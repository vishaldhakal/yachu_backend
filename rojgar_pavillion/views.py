from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import Registration, Topic, TimeSlot
from .serializers import RegistrationSerializer, TopicSerializer, TimeSlotSerializer, RegistrationDetailSerializer

class RegistrationView(generics.ListCreateAPIView):
    queryset = Registration.objects.all()
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RegistrationSerializer
        return RegistrationDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            registration = serializer.save()
            # Increase the current participants count
            time_slot = registration.time_slot
            time_slot.current_participants += registration.total_participants
            time_slot.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
class RegistrationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Registration.objects.all()
    serializer_class = RegistrationDetailSerializer
    

class AvailableSessionsView(generics.ListAPIView):
    serializer_class = TopicSerializer
    
    def get_queryset(self):
        """
        Get active topics with available time slots
        """
        return Topic.objects.filter(
            is_active=True
        ).prefetch_related('time_slot_instances')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['include_available_spots'] = True
        return context
    
class TimeSlotByDateView(generics.ListAPIView):
    serializer_class = TimeSlotSerializer

    def get_queryset(self):
        date = self.request.query_params.get('date')  # Get the date from query parameters
        topic = self.request.query_params.get('topic')
        top = Topic.objects.get(id=topic)
        if date:
            return TimeSlot.objects.filter(date=date,topic=top)  # Filter time slots by the provided date
        return TimeSlot.objects.none() 