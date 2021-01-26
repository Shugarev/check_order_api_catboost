from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from evaluation.dataset_tester import DatasetTester
from .utils import get_data_to_create_order, get_profile_config, validate_data


@api_view(['POST'])
def get_order_probability(request):
    validate, message = validate_data(request)
    if not validate:
        return Response(message, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    profile_config = get_profile_config(request)
    order_data_convert = get_data_to_create_order(request)
    try:
        probability = DatasetTester.run_one_order(profile_config, order_data_convert)
    except Exception as e:
        raise ValidationError(e)
    return Response({"probability": probability}, status=status.HTTP_200_OK)
