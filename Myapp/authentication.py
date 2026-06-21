from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import Developer

class DeveloperJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Call the base authentication to validate the JWT token
        raw_token = request.headers.get('Authorization')

        if raw_token is None:
            return None

        # Strip "Bearer " from the token if it exists
        if raw_token.startswith("Bearer "):
            raw_token = raw_token[7:]

        # Validate the token and extract the user
        try:
            validated_token = self.get_validated_token(raw_token)
            developer_id = validated_token.get("DeveloperID")
            if not developer_id:
                raise AuthenticationFailed('DeveloperID not in token payload.')

            # Retrieve the Developer instance using the DeveloperID
            developer = Developer.objects.get(DeveloperID=developer_id)

            return (developer, validated_token)  # Return Developer and token

        except Exception as e:
            raise AuthenticationFailed(f"Invalid token: {e}")