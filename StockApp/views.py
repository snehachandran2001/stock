# stockdata/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import redirect
from .models import FyersToken
from .serializers import FyersTokenSerializer
import requests

# FYERS API credentials
CLIENT_ID = 'your_client_id'
SECRET_KEY = 'your_secret_key'
REDIRECT_URI = 'your_redirect_uri'


@api_view(['GET'])
def get_auth_url(request):
    auth_url = f"https://api.fyers.in/api/v2/generate-authcode?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&state=sample_state"
    return redirect(auth_url)


@api_view(['GET'])
def handle_redirect(request):
    code = request.GET.get('code')
    state = request.GET.get('state')

    # Exchange auth code for access token
    token_url = 'https://api.fyers.in/api/v2/validate-authcode'
    payload = {
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'secret_key': SECRET_KEY,
        'redirect_uri': REDIRECT_URI,
        'code': code,
    }
    response = requests.post(token_url, json=payload)
    token_data = response.json()

    # Store access token securely
    fyers_token, created = FyersToken.objects.get_or_create(id=1)
    fyers_token.access_token = token_data['access_token']
    fyers_token.refresh_token = token_data.get('refresh_token')
    fyers_token.token_type = token_data.get('token_type')
    fyers_token.expires_in = token_data.get('expires_in')
    fyers_token.scope = token_data.get('scope')
    fyers_token.save()

    return redirect('fetch_live_data')


@api_view(['GET'])
def fetch_live_data(request):
    try:
        fyers_token = FyersToken.objects.get(id=1)
    except FyersToken.DoesNotExist:
        return Response({'error': 'Access token not found'}, status=404)

    headers = {
        'Authorization': f'Bearer {fyers_token.access_token}'
    }
    params = {
        'symbol': 'NSE:RELIANCE-EQ'
    }
    response = requests.get('https://api.fyers.in/api/v2/data/quotes', headers=headers, params=params)
    data = response.json()

    return Response(data)
