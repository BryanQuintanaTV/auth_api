from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication

# Class that is going to do all endpoints actions
# {URL}/api/v1/users
class UserViewSet(viewsets.ModelViewSet):
    # Request a valid JWT to use the endpoints
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # POST {URL}/api/v1/rest/
    def create(self, request):
        serializer = UserSerializer(data=request.data)

        # Verify if the body data is valid
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # If is not valid, returns a 400 Error
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # GET {URL}/api/v1/rest/
    def list(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    # GET {URL}/api/v1/rest/{id}/
    def retrieve(self, request, pk=None):

        try:
            # Tries to make a query with the id
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user, data=request.data, partial=True)

            # Verify if the body data in the request is valid
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            # if is not valid, returns a 400 Error respnse
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            # If anything fail, returns a 404 Error
            return Response(status=status.HTTP_404_NOT_FOUND)

    # PATCH {URL}/api/v1/rest/{id}/
    def partial_update(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        

    # DELETE {URL}/api/v1/rest/{id}/
    def destroy(self, request, pk=None):

        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return Response({"detail":"Se ha borrado el usuario correctamente"},status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            # If anything fails, returns a 404 Error
            return Response(status=status.HTTP_404_NOT_FOUND)

# Class with the actions that endpoints are going to do
# {URL}/api/v1/login/
class LoginView(APIView):
        # POST {URL}/api/v1/rest/
        def post(self, request):
            # Define the required params for the use of the endpoints
            username = request.data.get('username')
            print("username",username)
            password = request.data.get('password')
            print("password",password)

            try:
                # Try to do a query with the body data on the request
                user = User.objects.get(username=username)

                # Use the method to verify the password
                if user.check_password(password):
                    user = get_object_or_404(User, username=username)
                    serializer = UserSerializer(user)
                    refresh = RefreshToken.for_user(user)
                    print("PASSWORD CORRECT", serializer.data)

                    # If verify is correct, it returns the data of the Token (SimpleJWT)
                    return Response({
                        'refresh':str(refresh),
                        'access':str(refresh.access_token),
                        'user':serializer.data
                        # 'user':user
                    }, status=status.HTTP_200_OK)
                print("PASSWORD INCORRECT")
                # If the verification fails, returns a 401 error
                return Response({"detail":"Credenciales invalidas"},status=status.HTTP_401_UNAUTHORIZED)

            except User.DoesNotExist:
                # If fails, returns a 401 Error
                return Response({"detail":"Credenciales invalidas"}, status=status.HTTP_401_UNAUTHORIZED)