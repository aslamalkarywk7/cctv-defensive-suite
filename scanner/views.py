import re
import requests
import urllib3
import json
import asyncio
from io import BytesIO
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import ScanResult
from .engines import SecurityEngine
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except: PANDAS_AVAILABLE = False

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def index(request):
    """Render main dashboard with last 20 history items"""
    history = ScanResult.objects.all().order_by('-timestamp')[:20]
    return render(request, 'scanner/index.html', {'history': history})

def get_history(request):
    """API for real-time history updates"""
    history = list(ScanResult.objects.all().order_by('-timestamp').values())
    return JsonResponse(history, safe=False)

def run_local_radar(request):
    """Local Area ARP/Socket Radar"""
    engine = SecurityEngine()
    cameras = engine.local_area_radar()
    return JsonResponse({'status': 'success', 'cameras': cameras})

def export_excel(request):
    """Generates military-grade Excel report"""
    if not PANDAS_AVAILABLE: return HttpResponse("Pandas not found on server", status=501)
    results = list(ScanResult.objects.all().values('host', 'port', 'method', 'username', 'password', 'device_info', 'timestamp'))
    if not results: return HttpResponse("No data to export", status=404)
    df = pd.DataFrame(results)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Surveillance_Report')
    output.seek(0)
    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="Karioka_Intel_Report.xlsx"'
    return response

def export_pdf(request):
    """Generates professional PDF audit report"""
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, 750, "Karioaka - Intelligence Surveillance Report")
    p.setFont("Helvetica", 10)
    y = 710
    for res in ScanResult.objects.all().order_by('-timestamp')[:50]:
        p.drawString(100, y, f"TARGET: {res.host}:{res.port} | METHOD: {res.method}")
        p.drawString(100, y-12, f"CREDS: {res.username} / {res.password} | DEVICE: {res.device_info}")
        y -= 40
        if y < 100: p.showPage(); y = 750
    p.showPage(); p.save()
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')

def clear_history(request):
    """Full database wipe for security"""
    if request.method == 'POST':
        ScanResult.objects.all().delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def run_range_scan(request):
    """IP Range Scanner view"""
    if request.method == 'POST':
        start_ip = request.POST.get('start_ip')
        end_ip = request.POST.get('end_ip')
        port = request.POST.get('port', 80)
        engine = SecurityEngine()
        found_ips = engine.scan_ip_range(start_ip, end_ip, port)
        return JsonResponse({'status': 'success', 'ips': found_ips})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def run_silent_radar(request):
    """SSDP/UPnP Background Discovery"""
    engine = SecurityEngine()
    targets = engine.silent_radar_discovery()
    return JsonResponse({'status': 'success', 'ips': targets})

def run_advanced_scan(request):
    """The master exploit & brute force orchestrator"""
    if request.method == 'POST':
        host = request.POST.get('host')
        port_raw = request.POST.get('port')
        mode = request.POST.get('mode', 'full')
        engine = SecurityEngine()
        all_findings = []
        
        # 1. Port Discovery
        ports = [int(p.strip()) for p in port_raw.split(',')] if port_raw else engine.discover_ports(host)
        if not ports: return JsonResponse({'status': 'failed', 'message': 'Target ports are closed or filtered.'})
        
        device_info = engine.fingerprint(host, ports[0], 'http')
        
        # Initialize loop for async operations
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            for p in ports:
                p_int = int(p)
                p_findings = []
                
                # A. CVE Exploitation
                if mode in ['exploit', 'full']:
                    p_findings.extend(engine.exploit_cve_2018_9995(host, p_int))
                
                # B. Async Brute Force (Parallelized)
                if mode in ['brute', 'full'] and not p_findings:
                    p_findings.extend(loop.run_until_complete(engine.async_brute(host, p_int)))
                
                # C. Final Synthesis & AI Eye
                for f in p_findings:
                    eye_data = engine.capture_eye_snapshot(host, p_int, f['user'], f['pass'])
                    
                    ScanResult.objects.create(
                        host=host, port=p_int, protocol='High-Tech',
                        username=f['user'], password=f['pass'],
                        method=f.get('method', 'Secure-Bypass') + (" | " + eye_data['analysis'] if eye_data else ""),
                        device_info=device_info,
                        snapshot=eye_data['base64'] if eye_data else None
                    )
                    all_findings.append(f)
        finally:
            loop.close()

        return JsonResponse({
            'status': 'success', 'host': host, 'device': device_info, 'findings': all_findings
        })
    return JsonResponse({'status': 'failed'}, status=400)
