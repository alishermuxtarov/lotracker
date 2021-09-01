from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from lotracker.models import FilterSetLot


class InfoView(APIView):
    """
    get:

    ### Endpoint for periodically getting common information such as badges counters, user information etc.

    Request example:
    `https://lotracker.rbc-group.uz/api/v1/info/`

    Response example:

        {
            "badges": {
                "favourite": 2,
                "subscription": 0
            }
        }

    """
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        return Response({
            'badges': {
                'favourite': request.user.favourite_lots.values_list('id').count(),
                'subscription': FilterSetLot.objects.filter(
                    user=request.user, is_displayed=False
                ).values_list('id').count(),
            }
        })
