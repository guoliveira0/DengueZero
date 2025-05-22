from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ReportForm
from .models import Report
from geopy.geocoders import Nominatim
from django.db.models import Q
from django.contrib.auth import authenticate, login


ALLOWED_EMAILS = ['luiz@sistemasaude.com.br', 'luiz@centrozoonoses.com.br']

def create_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            # Capturar latitude e longitude do POST
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            if latitude and longitude:
                report.latitude = latitude
                report.longitude = longitude
                # Usar geopy para converter coordenadas em endereço
                geolocator = Nominatim(user_agent="denguezero")
                location = geolocator.reverse(f"{latitude}, {longitude}")
                report.location = location.address if location else "Localização desconhecida"
            report.save()
            return redirect('report_success')
    else:
        form = ReportForm()
    return render(request, 'reports/create_report.html', {'form': form})


def report_success(request):
    return render(request, 'reports/report_success.html')


def home(request):
    query = request.GET.get('q', '')  # Captura o termo de busca
    reports = Report.objects.all()

    # Obter a localização do usuário usando os parâmetros da URL
    user_latitude = request.GET.get('latitude')
    user_longitude = request.GET.get('longitude')

    if user_latitude and user_longitude:
        geolocator = Nominatim(user_agent="denguezero")
        location = geolocator.reverse(f"{user_latitude}, {user_longitude}")
        if location:
            user_location = location.address
            # Filtrar relatórios com base na localização
            reports = reports.filter(location__icontains=user_location)

    if query:
        reports = reports.filter(
            Q(title__icontains=query) | Q(location__icontains=query)
        )

    focus_reports = reports.filter(report_type='focus', status='open')  # Focos de Dengue Abertos
    resolved_reports = reports.filter(report_type='focus', status='resolved')  # Focos de Dengue Resolvidos
    case_reports = reports.filter(report_type='case')  # Casos de Dengue em Casa

    return render(request, 'reports/home.html', {
        'focus_reports': focus_reports,
        'resolved_reports': resolved_reports,
        'case_reports': case_reports,
        'query': query,
        
        
        
    })


@login_required
@user_passes_test(lambda u: u.is_staff)  # Apenas usuários com permissão de staff
def change_status(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    if report.status == 'open':
        report.status = 'resolved'
    else:
        report.status = 'open'
    report.save()
    return redirect('home')  # Redireciona para a página principal


def custom_login(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username in ALLOWED_EMAILS:
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                error = "Senha incorreta."
        else:
            error = "Usuário não autorizado."
    return render(request, 'reports/login.html', {'error': error})

@login_required
def sua_view_restrita(request):
    # código da view
    return render(request, 'reports/sua_template.html')
