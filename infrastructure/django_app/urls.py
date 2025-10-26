from django.urls import path
from . import views


urlpatterns = [
    path(
        # TODO : Make this uuid instead of str later
        "units/<str:unit_id>/",
        views.UnitDetailsView.as_view(),
        name="unit-details",
    ),
]
