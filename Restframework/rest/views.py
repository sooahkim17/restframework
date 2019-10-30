from django.shortcuts import render
from rest_framework import viewsets
from .models import Essay,Album,Files
from .serializers import EssaySerializer,AlbumSerializer,FileSerializer
from rest_framework.filters import SearchFilter
from rest_framework.parsers import MultiPartParser,FormParser
# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    queryset=Essay.objects.all()
    serializer_class=EssaySerializer

    filter_backends=[SearchFilter]
    search_fields=('title','body')

    def perform_create(self,serializers):
        serializers.save(author=self.request.user)
    
    #현재 request보낸 유저
    #self.request.user

    def get_queryset(self):
        qs=super().get_queryset()

        if self.request.user.is_authenticated:
            qs=qs.filter(author=self.request.user)
        else:
            qs=qs.none()

        return qs
class ImgViewSet(viewsets.ModelViewSet):
    queryset=Album.objects.all()
    serializer_class=AlbumSerializer

from rest_framework.response import Response
from rest_framework import status
class FileViewSet(viewsets.ModelViewSet):
    queryset=Files.objects.all()
    serializer_class=FileSerializer

    parser_classes=(MultiPartParser,FormParser)

    def post(self,request,*args,**kwargs):
        serializer=FileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=HTTP_201_CREATED)
        else:
            return Response(serializer.error,status=HTTP_404_BAD_REQUEST)


