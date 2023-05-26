import uuid
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


def generate_unique_number(initial_letter):
    unique_number = F"{initial_letter}{str(uuid.uuid4().hex[:9]).upper()}"

    return unique_number
