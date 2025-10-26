from typing import TYPE_CHECKING
from django.http import JsonResponse
from django.views import View
from dataclasses import asdict

if TYPE_CHECKING:
    from django.http import HttpRequest


from application.use_cases import GetUnitDetailsService
from infrastructure.repositories import DjangoRepository



class UnitDetailsView(View):
    """"
    Django View to handle requests for Unit details.
    """

    # TODO This unit id is so long because it's uuid string
    def get(self, request: "HttpRequest", unit_id: str) -> JsonResponse:
        
        # Set up repository and service
        unit_repository = DjangoRepository()
        service = GetUnitDetailsService(unit_repository)

        # Execute use case
        dto = service.execute(unit_id=unit_id)

        # Return JSON response
        # TODO I should study about this part. It should be flexible enough for different views in the future
        return JsonResponse(asdict(dto), status=200)