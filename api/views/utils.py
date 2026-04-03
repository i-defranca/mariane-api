from rest_framework.response import Response


def res(body=None, status=200):
    if body is None:
        body = []
    return Response(body, status=status)
