from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests


@api_view(['POST'])
def serve(request):
    """
    List all code snippets, or create a new snippet.
    """
    print('server', request.data)
    r = requests.post('http://tunnel:9002/', json=request.data)
    print(r.status_code, r.text)

    return Response({"status": r.text})


@api_view(['POST'])
def middleware(request):
    """
    List all code snippets, or create a new snippet.
    """
    # r = requests.post('http://tunnel:9002/', data={'key': 'value'})
    print(request.data.dict())
    return Response({"status": 'ok'})
