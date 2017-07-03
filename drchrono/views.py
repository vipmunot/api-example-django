# Create your views here.
import requests
import settings
import refreshtoken
from datetime import datetime
from django.template import Context
from django.http import HttpResponse
from django.core.mail import send_mail
from django.shortcuts import render,redirect
from django.template.loader import get_template
from django.views.generic.base import TemplateView
from django.views.decorators.csrf import csrf_protect, csrf_exempt
patientsrecords = dict()

class mainpage(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(GetHome, self).get_context_data(**kwargs);
        if (settings.ACCESS_TOKEN == None):
            settings.oauth_code = self.request.GET.get('code');
            response = requests.post('https://drchrono.com/o/token/', data={
                'code': settings.oauth_code,
                'grant_type': 'authorization_code',
                'redirect_uri': settings.redirect_uri,
                'client_id': settings.client_id,
                'client_secret': settings.client_secret,
            })
            data = response.json();
            settings.ACCESS_TOKEN = data['access_token']
            settings.REFRESH_TOKEN = data['refresh_token']
            settings.ACCESS_TOKEN_EXPIRES_IN = data['expires_in']
            refreshtoken.countdown_refresh_accesstoken(settings.ACCESS_TOKEN_EXPIRES_IN)
        data = getcurrentuserinfo()
        username = data['username']
        patients = getpatients();
        template = get_template(GetHome.template_name)
        context = {'currentuser': username, "patients_data": patients}
        return context;

def get_home(request):
    template_name = "home.html"

    if (settings.ACCESS_TOKEN == None ):
        settings.oauth_code = request.GET.get('code');
        response = requests.post('https://drchrono.com/o/token/', data={
            'code': settings.oauth_code,
            'grant_type': 'authorization_code',
            'redirect_uri': settings.redirect_uri,
            'client_id': settings.client_id,
            'client_secret': settings.client_secret,
        })
        data = response.json()
        settings.ACCESS_TOKEN = data['access_token']
        settings.REFRESH_TOKEN = data['refresh_token']
        settings.ACCESS_TOKEN_EXPIRES_IN = data['expires_in']
        refreshtoken.countdown_refresh_accesstoken(settings.ACCESS_TOKEN_EXPIRES_IN)
    data = getcurrentuserinfo()
    username = data['username']
    patients = getpatients()
    template = get_template(template_name)
    context = {'currentuser': username,"patients_data":patients}
    html = template.render(Context(context))
    return HttpResponse(html)

def get_access(request):
    link = "https://drchrono.com/o/authorize/?redirect_uri="+settings.redirect_uri+"&response_type=code&client_id="+settings.client_id+"&scope=patients:read";
    context = {'currentuser': 'Anonymous user','authorizelink':link};
    template_name = "index.html"
    template = get_template(template_name)
    html = template.render(Context(context))
    return HttpResponse(html)

def wishpatient(request,id):
    if (settings.ACCESS_TOKEN == None ):
        settings.oauth_code = request.GET.get('code');
        response = requests.post('https://drchrono.com/o/token/', data={
            'code': settings.oauth_code,
            'grant_type': 'authorization_code',
            'redirect_uri': settings.redirect_uri,
            'client_id': settings.client_id,
            'client_secret': settings.client_secret,
        })
        data = response.json()
        settings.ACCESS_TOKEN = data['access_token']
        settings.REFRESH_TOKEN = data['refresh_token']
        settings.ACCESS_TOKEN_EXPIRES_IN = data['expires_in']
        refreshtoken.countdown_refresh_accesstoken(settings.ACCESS_TOKEN_EXPIRES_IN)
    data = getcurrentuserinfo()
    username = data['username']
    patient_data =  patientsrecords[str(id)]
    context = {'currentuser': username,'patient':patient_data}
    template_name = "patientdetails.html"
    template = get_template(template_name)
    html = template.render(Context(context))
    return HttpResponse(html)


def getpatients():
    patients,todaybirth = [],[]
    now=datetime.now()
    patients_url = 'https://drchrono.com/api/patients'
    while patients_url:
        data = requests.get(patients_url, headers={
            'Authorization': 'Bearer %s' % settings.ACCESS_TOKEN,
        }).json();
        patientlist = data['results']
        for each_patient in patientlist:
            if not each_patient['date_of_birth'] == None:
                patientsrecords[str(each_patient['id'])] = each_patient
                patients.append(each_patient)
                t = each_patient['date_of_birth'].split('-')
                if int(t[1]) ==now.month and int(t[2]) == now.day:
                    todaybirth.append(each_patient)
        patients_url = data['next']
        patients = sorted(patients, key=lambda x: (datetime.strptime(str(now.year + 1) + x["date_of_birth"][4:], '%Y-%m-%d') - now).days % 365)

    return patients

def getcurrentuserinfo():
    response = requests.get('https://drchrono.com/api/users/current', headers={
        'Authorization': 'Bearer %s' % settings.ACCESS_TOKEN,
    });
    response.raise_for_status()
    data = response.json()
    return data


@csrf_exempt
def sendEmail(request):
    email = request.POST['email']
    message = request.POST['BirthDayMessage']
    subject = request.POST['subject']
    send_mail(subject, message,settings.EMAIL_HOST_USER,[email],fail_silently=False)
    return redirect('/home')
