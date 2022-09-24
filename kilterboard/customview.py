from django.forms.models import model_to_dict
from rest_framework import generics
from rest_framework.serializers import ModelSerializer
from rest_framework.settings import api_settings


class CreateModelMixin:
    """
    Create a model instance.
    """

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        model = self.perform_create(serializer)
        return model

    def create_response(self, instance):
        serializer = self.get_response_serializer(data=model_to_dict(instance))
        serializer.is_valid(raise_exception=True)
        return serializer

    def perform_create(self, serializer: ModelSerializer):
        return serializer.create(serializer.validated_data)

    def get_success_headers(self, data):
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class GenericAPIView(generics.GenericAPIView):
    response_serializer_class = None

    def get_response_serializer_class(self):
        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method." % self.__class__.__name__
        )

        return self.response_serializer_class

    def get_response_serializer(self, *args, **kwargs):
        response_serializer_class = self.get_response_serializer_class()
        return response_serializer_class(*args, **kwargs)
