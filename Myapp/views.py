import random
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Viewer
from django.utils import timezone
from django.shortcuts import *
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from .serializers import *
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication



API_DATA = {
    "api1": {
        "viewer": [{"title": "Public Data 1"}],
        "developer": [{"title": "Dev Data 1", "created_at": "2024-11-20"}],
        "admin": [{"title": "Admin Data 1", "access_level": "Full"}],
    },
    "api2": {
        "viewer": [{"title": "Public Data 2"}],
        "developer": [{"title": "Dev Data 2", "created_at": "2024-11-21"}],
        "admin": [{"title": "Admin Data 2", "access_level": "Full"}],
    },
}


from django.core.mail import send_mail
from django.conf import settings

def generate_otp(request, number):
    viewer = get_object_or_404(Viewer, number=number)

    viewer.generated_otp = str(random.randint(100000, 999999))
    viewer.otp_expiry = datetime.now() + timedelta(minutes=5)  # 5 minutes expiry
    viewer.user_otp = None
    viewer.save()

    if viewer.email: 
        try:
            send_mail(
                subject="Your OTP Code",
                message=f"Your OTP code is {viewer.generated_otp}. It will expire in 5 minutes.",
                from_email=settings.EMAIL_HOST_USER ,
                recipient_list=[viewer.email],
                fail_silently=False, 
            )
        except Exception as e:
            return JsonResponse({"error": f"Failed to send email: {str(e)}"}, status=500)

    return JsonResponse({
        "message": "OTP generated and sent successfully thorough mail.",
        "number": viewer.number,
        "expiry": viewer.otp_expiry.strftime("%Y-%m-%d %H:%M:%S")
    })

def verify_otp(request, number, user_otp):
    viewer = get_object_or_404(Viewer, number=number)

    if viewer.generated_otp == str(user_otp):
        if viewer.otp_expiry and timezone.now() <= viewer.otp_expiry:
            
            viewer.user_otp = user_otp
            viewer.save()  
            return JsonResponse({"message":"Valid"},status=200)
        
        else:
            return JsonResponse({"error": "OTP has expired."}, status=400)
    else:
        return JsonResponse({"error": "Invalid OTP."}, status=400)
    
    

def api_list(request):
    number = request.GET.get('number')
    if number:
        viewer = Viewer.objects.filter(number=number).first()
        if viewer:
            role = 'viewer' 
            if viewer.user_otp:
                user_api_data = {
                    api: {"title": f"Data for {api}"} for api in API_DATA.keys()
                }
                return JsonResponse(user_api_data)
            else:
                return JsonResponse({"error": "OTP not verified."}, status=401)
    return JsonResponse({"error": "Viewer not found."}, status=404)


def fetch_api_data(request, api_name):
    number = request.GET.get('number')
    if number:
        viewer = Viewer.objects.filter(number=number).first()
        if viewer:
            role = 'viewer'  
            if viewer.user_otp:
                if api_name in API_DATA:
                    api_data = API_DATA[api_name].get(role, [])
                    if api_data:
                        return JsonResponse({"data": api_data})
                    else:
                        return JsonResponse({"error": f"No data available for role {role} in {api_name}."}, status=404)
                else:
                    return JsonResponse({"error": "API not found."}, status=404)
            else:
                return JsonResponse({"error": "OTP not verified."}, status=401)
    return JsonResponse({"error": "Viewer not found."}, status=404)

@api_view(['POST'])

@permission_classes([AllowAny])  # Allow access without authentication

def form_submission(request):
   
        serializer = FormSerializer(data=request.data)
            
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       
class DeveloperLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        DeveloperID = request.data.get('DeveloperID')
        password = request.data.get('password')

        try:
            developer = Developer.objects.get(DeveloperID=DeveloperID)
        except Developer.DoesNotExist:
            return Response(
                {"detail": "Invalid DeveloperID or password."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not developer.check_password(password):
            return Response(
                {"detail": "Invalid DeveloperID or password."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Generate JWT Token
        refresh = RefreshToken.for_user(developer)
        
        # Add DeveloperID to the access token's payload
        access_token = refresh.access_token
        access_token['DeveloperID'] = developer.DeveloperID  # Add DeveloperID to the token

        return Response({
            "refresh": str(refresh),
            "access": str(access_token),
        }, status=status.HTTP_200_OK)
        
from .authentication import DeveloperJWTAuthentication  # Import the custom authentication class

class DeveloperDashBoard(APIView):
    permission_classes = [IsAuthenticated]  # Ensure user is authenticated
    authentication_classes = [DeveloperJWTAuthentication]  # Use custom JWT authentication

    def get(self, request):
        developer = request.user  # Now request.user will be a Developer instance
        return Response({
            'message': f'Welcome, Developer {developer.DeveloperID}'
        }, status=200)