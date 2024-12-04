from django.http import JsonResponse
from django.utils import timezone
from .models import Viewer
from django.utils.timezone import now
from .models import *


class ZeroTrustMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/api/"):
            number = request.GET.get('number') 
            user_otp = request.GET.get('user_otp')
            
            print(f"Zero Trust Middleware - Number: {number}, OTP: {user_otp}")  

            if number and user_otp:
                try:
                    viewer = Viewer.objects.get(number=number)

                    if viewer.generated_otp == user_otp:
                        return self.get_response(request)
                    else:
                        return JsonResponse({"error": "Invalid OTP."}, status=400)
                except Viewer.DoesNotExist:
                    return JsonResponse({"error": "User not found."}, status=404)
            else:
                return JsonResponse({"error": "OTP and number are required."}, status=400)

        return self.get_response(request)


class ViewerBehaviourMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Attempt to get user information (assuming you use session or auth framework)
        user_number = request.GET.get('number')  # Assuming the number is passed in the query params

        if user_number:
            try:
                viewer = Viewer.objects.get(number=user_number)  # Retrieve the Viewer object
            except Viewer.DoesNotExist:
                print(f"No Viewer found with number: {user_number}")
                return response  # Exit middleware if no viewer matches
            
            # Capture the viewer's behavior if they access specific API routes
            if request.path.startswith('/api/'):
                if request.path == '/api/list/':
                    action = "Listing the API"
                    api_name = "api_list"
                elif request.path == '/api/data/':
                    action = "Viewing API Data"
                    api_name = "api_data"
                else:
                    action = "Accessing API"
                    api_name = request.path

                # Log behavior into the ViewerBehaviour model
                ViewerBehaviour.objects.create(
                    user=viewer,
                    action=action,
                    api_name=api_name,
                    url=request.path,
                    timestamp=now()
                )

        return response