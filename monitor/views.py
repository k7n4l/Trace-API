from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Endpoint, TestRun
from django.db.models import Count, Avg, Q
from .serializers import EndpointSerializer
from django.shortcuts import get_object_or_404, render
from .test_runner import execute_request

class EndpointListCreateView(generics.ListCreateAPIView):
    queryset = Endpoint.objects.all()
    serializer_class = EndpointSerializer
    
class EndpointDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Endpoint.objects.all()
    serializer_class = EndpointSerializer
    
class HealthyAPIView(generics.GenericAPIView):
    def get(self,request):
        return Response({
            "status" : "healthy",
            "message" : "API is Working" 
        })   
class ClientErrorAPIView(APIView):
    def get(self, request):
        return Response(
            {"error" : "simulated client error"},
            status=400
        )
class ServerErrorAPIView(APIView):
    def get(self, request):
        return Response(
            {"error" : "simulated server error"},
            status=500
        )
    
class RunEndpointTestView(APIView):
    def post(self, request, pk):
        endpoint = get_object_or_404(Endpoint, pk=pk)
        
        url = f"http://127.0.0.1:8000{endpoint.path}"
        
        result = execute_request(endpoint=endpoint, url=url, method=endpoint.method)
        
        return Response(result)
    

class EndpointSummaryView(APIView):
    def get(self, request, pk):
        endpoint = get_object_or_404(Endpoint, pk=pk)

        runs = TestRun.objects.filter(endpoint=endpoint)
        
        stats = runs.aggregate(
            total_runs = Count("id"),
            successful_runs = Count("id", filter = Q(success = True)),
            failed_runs = Count("id", filter = Q(success = False)),
            average_response_time_ms = Avg("response_time_ms")
        )
        
        success_rate = round((stats["successful_runs"]/stats["total_runs"])*100, 2) if stats["total_runs"] > 0 else 0

        return Response({
            "endpoint_id": endpoint.id,
            "total_runs": stats["total_runs"],
            "successful_runs": stats["successful_runs"],
            "failed_runs": stats["failed_runs"],
            "success_rate": success_rate,
            "average_response_time_ms": round(
                stats["average_response_time_ms"] or 0, 2
            )
        })
        
def dashboard(request):
    
    if request.method == "POST":
        name = request.POST.get("name","").strip()
        path = request.POST.get("path", "").strip()
        method = request.POST.get("method", "GET")
        
        if name and path and method in ["GET", "POST"]:
            Endpoint.objects.create(
                name=name,
                path=path,
                method=method
            )
    
    endpoints = Endpoint.objects.all().order_by("-created_at")
    
    return render(request, "monitor/dashboard.html",{
        "endpoints" : endpoints
    })