# from rest_framework.response import Response
# from rest_framework.views import APIView
#
# from devices_management.models import Device
#
#
# class BillOfLoadingView(APIView):
#
#     @staticmethod
#     def get(request):
#         bill_of_loadings = Device.objects.all()
#         return Response(
#             BillOfLoadingGetSerializer(instance=bill_of_loadings, many=True).data
#         )
#
#     @staticmethod
#     def post(request):
#         serializer = BillOfLoadingPostSerializer(data=request.data)
#         if serializer.is_valid():
#             obj = serializer.save(created_by=request.user)
#             BlManager(request.user, bl=obj).addTimeLine(BlManager.CREATION_ACTION)
#             return Response({
#                 "status": True,
#                 "data": BillOfLoadingGetSerializer(instance=obj, many=False).data
#             })
#
#         print(serializer.errors)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class ListBillOfLoading(generics.ListAPIView):
#     search_fields = ['consignee_cellphone', 'bill_number', 'consignee_address']
#     filter_backends = (filters.SearchFilter,)
#     serializer_class = BillOfLoadingGetSerializer
#     queryset = BillOfLoading.objects.all().order_by('-created_at')
#     pagination_class = StandardResultsSetPagination
#
#
# class BillOfLoadingDetail(APIView):
#
#     def get(self, request, pk):
#         try:
#             bill_of_loading = BillOfLoading.objects.get(id=pk)
#         except BillOfLoading.DoesNotExist:
#             return Response("BillOfLoading not found", status=status.HTTP_404_NOT_FOUND)
#         include_charges = self.request.GET.get('include_charges', None)
#         include_timeline = self.request.GET.get('include_timeline', None)
#         print(include_timeline)
#         data = BillOfLoadingGetSerializer(instance=bill_of_loading, many=False).data
#         if include_charges is not None and include_charges == 'true':
#             data['bl_charges'] = BillOfLoadingChargeGetSerializer(
#                 instance=BillOfLoadingCharge.objects.filter(bill_of_loading_id=pk),
#                 many=True
#             ).data
#         if include_timeline is not None and include_timeline == 'true':
#             data['bl_timeline'] = BillOfLoadingTimelineGetSerializer(
#                 instance=BillOfLoadingTimeline.objects.filter(bill_of_loading_id=pk),
#                 many=True
#             ).data
#         return Response(data)
#
#     @staticmethod
#     def put(request, pk):
#         try:
#             bill_of_loading = BillOfLoading.objects.get(id=pk)
#         except BillOfLoading.DoesNotExist:
#             return Response("BillOfLoading not found", status=status.HTTP_404_NOT_FOUND)
#
#         serializer = BillOfLoadingPutSerializer(instance=bill_of_loading, data=request.data)
#         if serializer.is_valid():
#             serializer.save(updated_by=request.user)
#             return Response({
#                 "status": True,
#                 "data": serializer.data
#             })
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
