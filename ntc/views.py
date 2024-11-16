from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from concurrent.futures import ThreadPoolExecutor
from .serializers import (
    SearchQuerySerializer, ServiceCategorySerializer, 
    ServiceSubCategorySerializer, NtcServiceSerializer,
    NtcPackageSerializer, NtcCustomerCareSerializer, NtcFaqSerializer
)
from .models import (
    ServiceCategory, ServiceSubCategory, NtcService,
    NtcPackage, NtcCustomerCare, NtcFaq
)

# Create your views here.

class GlobalSearchView(APIView):
    search_field_mapping = {
        ServiceCategory: ['name', 'description'],
        ServiceSubCategory: ['name', 'description'],
        NtcService: ['name', 'description'],
        NtcPackage: ['name', 'description'],
        NtcCustomerCare: ['name', 'description', 'contact', 'email', 'location', 'address'],
        NtcFaq: ['question', 'answer']
    }

    def get_model_results(self, model, serializer_class, search_query, limit=5):
        query_terms = search_query.split()
        base_query = Q()
        search_fields = self.search_field_mapping.get(model, [])
        
        for term in query_terms:
            field_queries = Q()
            for field in search_fields:
                field_queries |= Q(**{f'{field}__icontains': term})
            base_query |= field_queries
            
        results = model.objects.filter(base_query).distinct()[:limit]
        
        return {
            'model': model.__name__,
            'results': serializer_class(results, many=True).data
        }

    def perform_search(self, search_query):
        search_configs = [
            (ServiceCategory, ServiceCategorySerializer),
            (ServiceSubCategory, ServiceSubCategorySerializer),
            (NtcService, NtcServiceSerializer),
            (NtcPackage, NtcPackageSerializer),
            (NtcCustomerCare, NtcCustomerCareSerializer),
            (NtcFaq, NtcFaqSerializer),
        ]

        with ThreadPoolExecutor(max_workers=6) as executor:
            futures = [
                executor.submit(
                    self.get_model_results,
                    model,
                    serializer_class,
                    search_query
                )
                for model, serializer_class in search_configs
            ]
            
            results = [future.result() for future in futures]

        return [r for r in results if r['results']]

    def get(self, request):
        query = request.GET.get('query', '')
        
        if not query or len(query) < 3:
            return Response(
                {'error': 'Search query must be at least 3 characters long'},
                status=status.HTTP_400_BAD_REQUEST
            )

        results = self.perform_search(query)
        
        return Response({
            'query': query,
            'results': results
        })

    def post(self, request):
        serializer = SearchQuerySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        search_query = serializer.validated_data['query']
        results = self.perform_search(search_query)

        return Response({
            'query': search_query,
            'results': results
        })
