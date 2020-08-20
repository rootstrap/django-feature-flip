from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests


@api_view(['GET'])
def status(request):
    """
    List all code snippets, or create a new snippet.
    """
    r = requests.get('http://localhost:9002/status')
    print(r)

    return Response({"status": r.status_code})
