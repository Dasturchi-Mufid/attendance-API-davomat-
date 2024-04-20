from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework import status

from dashboard import models
from . import serializers

@api_view(['GET'])
def staff_list(request):
    queryset = models.Employee.objects.all()
    paginator = PageNumberPagination()
    paginator.page_size = 5

    result_page = paginator.paginate_queryset(queryset, request)
    serializer = serializers.EmployeeListSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['POST','GET'])
def attendance_create(request):
    id=request.data.get('id')
    try:
        models.Attendance.objects.create(employee_id=id)
        return Response({'success':True}, status=status.HTTP_201_CREATED)
    except Exception as err:
        return Response({'success':False, 'exception':f"{err}"}, status=status.HTTP_400_BAD_REQUEST)
