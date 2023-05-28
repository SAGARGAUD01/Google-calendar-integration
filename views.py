from django.shortcuts import redirect
from django.http import HttpResponse
from django.views import View
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

# Google Calendar API scopes
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# View for initiating OAuth flow
class GoogleCalendarInitView(View):
    def get(self, request):
        flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
        authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')
        request.session['state'] = state
        return redirect(authorization_url)

# View for handling OAuth redirect and retrieving access token
class GoogleCalendarRedirectView(View):
    def get(self, request):
        state = request.session.get('state')
        flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES, state=state)
        flow.fetch_token(authorization_response=request.get_full_path())
        credentials = flow.credentials

        # Use the access token to get a list of events in the user's calendar
        service = build('calendar', 'v3', credentials=credentials)
        events_result = service.events().list(calendarId='primary').execute()
        events = events_result.get('items', [])

        # Process the events as required
        # ...

        return HttpResponse("Events retrieved successfully!")
