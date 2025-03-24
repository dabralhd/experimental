from flask import Response


def liveness_probe() -> Response:
    return Response(status=200)


def readiness_probe() -> Response:
    return Response(status=200)
