from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer, OrganizationSerializer, UserSerializer, ProfileSerializer
from .models import CustomUser, Organization, Profile
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import FilterSet, CharFilter, NumberFilter, DjangoFilterBackend
# Create your views here.


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        # Create a mutable copy of the request data
        data = request.data.copy()
        # Extract password from request data
        password = data.get('password', None)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        # Create user with hashed password
        user = serializer.save()
        user.set_password(password)
        user.save()

        # Create a profile for the new user
        Profile.objects.create(user=user)

        # Generate tokens
        refresh = RefreshToken.for_user(user)

        headers = self.get_success_headers(serializer.data)
        return Response({
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED, headers=headers)


class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({
                'error': 'Please provide both username and password'
            }, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user:
            serializer = UserSerializer(user)
            refresh = RefreshToken.for_user(user)

            return Response({
                'user': serializer.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })

        return Response({
            'error': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)


class OrganizationFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')
    transaction_type = CharFilter(
        field_name='transaction_type', lookup_expr='icontains')
    balance_gt = CharFilter(field_name='balance', lookup_expr='gte')
    balance_lt = CharFilter(field_name='balance', lookup_expr='lte')

    class Meta:
        model = Organization
        fields = ['name', 'transaction_type', 'balance_gt', 'balance_lt']


class OrganizationListCreateView(generics.ListCreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrganizationFilter
    # permission_classes = [IsAuthenticated]
