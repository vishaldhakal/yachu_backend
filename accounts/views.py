from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer, OrganizationDetailSerializer, OrganizationSerializer, UserSerializer, DepartmentSerializer
from .models import CustomUser, Organization, Profile, Department
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import FilterSet, CharFilter, DjangoFilterBackend
from rest_framework.filters import SearchFilter

# Create your views here.


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        try:
            # Create a mutable copy of the request data
            data = request.data.copy()
            # Extract password from request data
            password = data.get('password', None)

            if not password:
                return Response({
                    'error': 'Password is required'
                }, status=status.HTTP_400_BAD_REQUEST)

            if not data.get('username'):
                return Response({
                    'error': 'Username is required'
                }, status=status.HTTP_400_BAD_REQUEST)
            if CustomUser.objects.filter(username=data.get('username')).exists():
                return Response({
                    'error': 'Username already exists'
                }, status=status.HTTP_400_BAD_REQUEST)

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
            refresh['user_id'] = user.id
            refresh['username'] = user.username
            refresh['email'] = user.email
            refresh['phone_number'] = user.phone_number
            refresh['address'] = user.address

            headers = self.get_success_headers(serializer.data)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED, headers=headers)

        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
            refresh = RefreshToken.for_user(user)
            refresh['user_id'] = user.id
            refresh['username'] = user.username
            refresh['email'] = user.email
            refresh['phone_number'] = user.phone_number
            refresh['address'] = user.address

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        return Response({
            'error': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)


class OrganizationFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')
    person_in_charge = CharFilter(
        field_name='person_in_charge', lookup_expr='icontains')
    phone_number = CharFilter(
        field_name='phone_number', lookup_expr='icontains')
    address = CharFilter(field_name='address', lookup_expr='icontains')

    class Meta:
        model = Organization
        fields = ['name', 'person_in_charge', 'phone_number', 'address']


class OrganizationListCreateView(generics.ListCreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = OrganizationFilter
    permission_classes = [IsAuthenticated]
    search_fields = ['name']


class OrganizationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OrganizationDetailSerializer
        return OrganizationSerializer


class DepartmentListCreateView(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
