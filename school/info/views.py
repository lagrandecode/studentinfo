from django.shortcuts import render
from django.http import HttpResponse
from .forms import StudentForm
from .models import Student
import requests
import io
import uuid
from datetime import datetime
from django.contrib import messages


# Create your views here.




BASE_URL = 'https://kc.kobotoolbox.org'
SUMISSION_URL = f'{BASE_URL}/api/v1/submissions'
TOKEN = '6fb29d8015dc136cba3558590282ddab7f2b24a5'



def format_openrosa_datetime():
    return datetime.now().isoformat('T', 'milliseconds')


def create_xml_submission(data, _uuid):
    xml_data = f'''
    <aKH8BtV5L6AqYcJ4SJFdYP id="aKH8BtV5L6AqYcJ4SJFdYP" version="1 ({datetime.now():%Y-%m-%d %H:%M:%S})">
        <formhub>
            <uuid>9c6a7057627b409cac37e9f989678d08</uuid>
        </formhub>
        <start>{format_openrosa_datetime()}</start>
        <end>{format_openrosa_datetime()}</end>

        <first_name>{data['first_name']}</first_name>
        <last_name>{data['last_name']}</last_name>
        <school_class>{data['school_class']}</school_class>
        <gender>{data['gender']}</gender>
        <age>{data['age']}</age>


        <__version__>vM2s7ZM7a5E9eH3moaqZRE</__version__>
        <meta>
            <instanceID>uuid:{_uuid}</instanceID>
        </meta>
    </aKH8BtV5L6AqYcJ4SJFdYP>
    '''
    return xml_data.encode()

def addStudent(request):
    success = None  # Initialize the success variable
    error = None  # Initialize the error variable

    if request.method == 'POST':
        studentform = StudentForm(request.POST)
        if studentform.is_valid():
            first_name = studentform.cleaned_data['first_name']
            last_name = studentform.cleaned_data['last_name']
            school_class = studentform.cleaned_data['school_class']
            gender = studentform.cleaned_data['gender']
            age = studentform.cleaned_data['age']
            studentform.save()

            _uuid = str(uuid.uuid4())
            data = {
                'first_name': first_name,
                'last_name': last_name,
                'school_class': school_class,
                'gender': gender,
                'age': age,
            }

            file_tuple = (_uuid, io.BytesIO(create_xml_submission(data, _uuid)))
            files = {'xml_submission_file': file_tuple}
            headers = {'Authorization': f'Token {TOKEN}'}
            res = requests.post(SUMISSION_URL, files=files, headers=headers)
            if res.status_code == 201:
                success = 'successful'
                messages.info(request, 'Success')
            else:
                error = 'error'
                messages.error(request, 'Something went wrong')
            studentform = StudentForm()

    else:
        studentform = StudentForm()

    return render(request, 'addstudent.html', {'form': studentform, 'success': success, 'error': error})



#fetch api to display the data on the table 

def showstudent(request):
    # Define the API token and URL
    import json
    api_token = '6fb29d8015dc136cba3558590282ddab7f2b24a5'
    api_url = 'https://kc.kobotoolbox.org/api/v1/data/1635156?format=json'

    # Set the Authorization header with the API token
    headers = {
        'Authorization': f'Token {api_token}'
    }

    # Make an HTTP GET request to the API
    response = requests.get(api_url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        api = json.loads(response.content)
        context = {
            'api': api
        }
        print(response.content)
        return render(request, 'show.html', context)
    else:
        # Handle the case where the request was not successful
        error_message = 'Failed to retrieve data from the API.'
        return render(request, 'show.html',context)
