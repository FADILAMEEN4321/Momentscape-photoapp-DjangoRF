from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework import status
from .serializers import RegistrationSerializer,ProfileSerializer,UserUpdateSerializer,UserProfileSerializer,ProfileUpdateSerializer
from rest_framework.permissions import IsAuthenticated
from base.models import Profile


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['is_superuser'] = user.is_superuser
        token['user_id'] = user.id
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer    


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token',
        '/api/token/refresh'
    ]
    return Response(routes)



@api_view(['POST'])
def signup_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User successfully registered.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class UserListView(generics.ListCreateAPIView):
    queryset = Profile.objects.filter(is_superuser=False)
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]


class ProfileDeleteView(generics.DestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer



class UserUpdateView(generics.UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserUpdateSerializer

    def update(self, request, *args, **kwargs):
        # Get the user object to be updated
        instance = self.get_object()

        # Get the new username from the request data
        new_username = request.data.get('username')

        # Check if a user with the new username already exists
        if Profile.objects.filter(username=new_username).exclude(id=instance.id).exists():
            return Response({'detail': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Perform the username update
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)    
    

@api_view(['GET'])
def get_user_profile(request, user_id):
    try:
        user_profile = Profile.objects.get(id=user_id)
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Profile.DoesNotExist:
        return Response(
            {'detail': 'User profile not found.'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['PUT'])
def update_user_profile(request,user_id):
    try:
        user_profile = Profile.objects.get(id=user_id)
    except Profile.DoesNotExist:
        return Response({'detail': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ProfileUpdateSerializer(user_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        


