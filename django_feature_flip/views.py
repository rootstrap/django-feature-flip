from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests


@api_view(['GET'])
def status(request):
    """
    List all code snippets, or create a new snippet.
    """
    r = requests.post('http://tunnel:9002/', data={'key': 'value'})
    print(r.status_code, r.text)

    return Response({"status": r.text})
