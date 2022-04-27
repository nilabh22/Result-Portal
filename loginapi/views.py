from email import message
from http.client import OK
from pyexpat.errors import messages
from urllib import response
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth import logout
import io
from .models import Student
from .serializers import FileSerializer
from rest_framework.parsers import (
    MultiPartParser,
    FormParser
)
import pandas as pd
from rest_framework import generics
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

# class LoginAPI(KnoxLoginView):
#     permission_classes = (permissions.AllowAny,)

#     def post(self, request, format=None):
#         serializer = AuthTokenSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         login(request, user)
#         return super(LoginAPI, self).post(request, format=None)

# @unauthenticated_user
@api_view(['POST'])
def loginPage(request):
	# if request.user.is_authenticated:
	# 	return redirect('home')
	# else:
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    if request.method == 'POST':
        username = request.data['username']
        password =request.data['password']
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
        else:
            messages.info(request, 'Username OR password is incorrect')
        
    return HttpResponse("OK")


def logoutUser(request):
    logout(request)


class FileUploadView(APIView):

    """Represents file upload view class.
    API endpoint that allows users to be upload a csv file.
    POST: upload file
    """

    parser_classes = (MultiPartParser, FormParser,)

    def post(self, request, *args, **kwargs):
        """Upload the CSV file.
        Then reads it and saves csv data to database.
        Endpoint: /api/patients/file_upload/
        """
        request.data['owner'] = request.user.id
        file_serializer = FileSerializer(data=request.data)
        # Commented code is for debugging only
        # import pdb; pdb.set_trace()
        # print(to_dict['_name'])
        _dict_file_obj = request.data['file'].__dict__

        _csv = _dict_file_obj['_name'].endswith('.csv')

        _excel = _dict_file_obj['_name'].endswith('.xlsx')

        if request.data['file'] is None:
            return Response({"error": "No File Found"},
                            status=status.HTTP_400_BAD_REQUEST)

        if file_serializer.is_valid():
            data = self.request.data.get('file')

            if _csv is True:
                data_set = data.read().decode('UTF-8')
                io_string = io.StringIO(data_set)
                io_string = io.StringIO(data_set)

                csv_file = pd.read_csv(io_string, low_memory=False)
                columns = list(csv_file.columns.values)

                name, department, branch, roll_no, email = columns[0], columns[1], columns[2], columns[3], columns[4]

                instances = [
                    Student(
                        name=row[name],
                        department=row[department],
                        branch=row[branch],
                        roll_no=row[roll_no],
                        email=row[email]
                    )

                    for index, row in csv_file.iterrows()
                ]

                Student.objects.bulk_create(instances)

            elif _excel is True:
                xl = pd.read_excel(data)
                columns = list(xl.columns.values)
                name, department, branch, roll_no, email = columns[0], columns[1],columns[2],columns[3],columns[4]

                instances = [
                    Student(
                        name=row[name],
                        department=row[department],
                        branch=row[branch],
                        roll_no=row[roll_no],
                        email=row[email]
                    )

                    for index, row in xl.iterrows()
                ]

                Student.objects.bulk_create(instances)

            else:
                return Response(data={"err": "Must be *.xlsx or *.csv File."},
                                status=status.HTTP_400_BAD_REQUEST
                                )

            file_serializer.save()
            return Response(
                {"message": "Upload Successfull",
                 "data": file_serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(file_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST
                            )
