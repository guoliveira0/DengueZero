from django.shortcuts import render, redirect
from .forms import ReportForm
from .models import Report
from geopy.geocoders import Nominatim
from django.db.models import Q

def create_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            if latitude and longitude:
                geolocator = Nominatim(user_agent="denguezero")
                location = geolocator.reverse(f"{latitude}, {longitude}")
                report.location = location.address if location else "Localização desconhecida"
            report.save()
            return render(request, 'reports/report_success.html')
    else:
        form = ReportForm()
    return render(request, 'reports/create_report.html', {'form': form})


def report_success(request):
    return render(request, 'reports/report_success.html')


def home(request):
    query = request.GET.get('q', '')  # Captura o termo de busca
    reports = Report.objects.all()

    # Obter a localização do usuário usando a API
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

    focus_reports = reports.filter(report_type='focus')  # Focos de Dengue
    case_reports = reports.filter(report_type='case')  # Casos de Dengue em Casa

    return render(request, 'reports/home.html', {
        'focus_reports': focus_reports,
        'case_reports': case_reports,
        'query': query,
    })
