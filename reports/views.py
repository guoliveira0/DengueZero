from django.shortcuts import render, redirect
from .forms import ReportForm
from .models import Report
from geopy.geocoders import Nominatim
from django.db.models import Q

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
