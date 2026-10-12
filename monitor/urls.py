from django.urls import path
from .views import EndpointListCreateView, EndpointDetailView, HealthyAPIView, RunEndpointTestView, EndpointSummaryView, ClientErrorAPIView, ServerErrorAPIView, dashboard

urlpatterns = [
    path('endpoints/',EndpointListCreateView.as_view(),name="endpoint-list-create",),
    path("endpoints/<int:pk>/",EndpointDetailView.as_view(),name="endpoint-detail",),
    path("healthy/",HealthyAPIView.as_view(), name="healthy"),
    path("client-error/",ClientErrorAPIView.as_view(), name="client-error"),
    path("server-error/", ServerErrorAPIView.as_view(), name="server-error"),
    path("endpoints/<int:pk>/run/",RunEndpointTestView.as_view(), name="endpoint-run"),
    path("endpoints/<int:pk>/summary/",EndpointSummaryView.as_view(), name="endpoint-summary"),
    path("",dashboard, name="dashboard"),
]