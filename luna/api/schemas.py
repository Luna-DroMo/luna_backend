from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework import serializers


CustomRequestSchema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'custom_field': openapi.Schema(type=openapi.TYPE_STRING),
    },
    required=['custom_field'],
)

CustomResponseSchema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'result': openapi.Schema(type=openapi.TYPE_STRING),
    },
    required=['result'],
)

schema_view = get_schema_view(
    openapi.Info(
        title="Dropout Prediction API",
        default_version='v1',
        description="API documentation for LUNA",
    ),
    #url='https://mz-bdev.de/',
    public=True,
    permission_classes=(permissions.AllowAny,),
)




