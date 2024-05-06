import re
import socket
from urllib.parse import urlparse



#1.1.1.	Using the IP Address
def check_ip_address(inp):
    inp = replace_hex(inp)
    pattern = "((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
    ret = re.search(pattern, inp)
    if ret is None: return 1
    return -1 #inp[ret.start():ret.end()]

def replace_hex(inp : str):
    pattern = r"0[x | %][0-9a-zA-Z]{2}"
    ret = re.findall(pattern,inp)
    for i in ret:
        ind = inp.find(i)
        inp = inp[:ind] + str(int(i,16)) + inp[ind+4:]
    return inp

#1.1.2.	Long URL to Hide the Suspicious Part
def check_string_length(inp):
    if len(inp) < 54:
        return 1
    elif len(inp) >= 54 and len(inp) <= 75:
        return 0  
    else:
        return -1  # feature = Phishing
    
#1.1.3.	Using URL Shortening Services “TinyURL”
def check_url_shortener(inp):
    inp = get_url_domain_name(inp)
    with  open("shortener_list.txt", "r") as file:
        for line in file:
            domain = line.strip()
            if domain in inp:
                return -1
    return 1

def get_url_domain_name(url):
    domain_name = re.sub(r'.*://', "", url)
    return domain_name[:domain_name.find(r'/')]


#1.1.4.	URL’s having “@” Symbol
def check_at_symbol(inp):
    at = ['@','x64']
    for a in at:
        if a in inp : return -1
    return 1

#1.1.5.	Redirecting using “//”
def check_redirecting(inp):
    last_x_position = inp.rfind("x")
    if last_x_position > 7:
        return -1
    else:
        return 1

#1.1.7.	Sub Domain and Multi Sub Domains
def check_sub_domain(inp):
    dot = inp.count(".")
    if dot == 2:
        return 0
    elif dot == 1:
        return 1
    else:
        return -1

def get_domain_name(inp):
    parsed_url = urlparse(inp)
    domain = parsed_url.netloc
    return domain

#1.1.6.	Adding Prefix or Suffix Separated by (-) to the Domain
def check_prefix(inp):
    _ = inp.count("-")
    if _ > 0: return -1
    else: return 1


import ssl
from datetime import datetime
#1.1.8.	HTTPS
def check_https(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.url.startswith("https://")
        else :
            return False
    except :
        return False

# Trusted Certificate Authorities
certificate_authorities = ["GeoTrust", "GoDaddy.com,", "Sectigo Limited", "Thawte", "Comodo", "VeriSign",
    "GlobalSign nv-sa", "Symantec", "Entrust, Inc.", "DigiCert Inc", "RapidSSL", "Let's Encrypt",
    "Trustwave", "Google Trust Services LLC", "SSL.com", "Gandi", "cPanel, Inc.", "AlphaSSL", "Buypass AS-983163327",
    "SwissSign AG", "DHIMYOTIS", "WoTrus CA Limited", "Actalis S.p.A."
]

def get_certificate_info(url:str):

    url = get_domain_name(url)
    try:
        context = ssl.create_default_context()

        with socket.create_connection((url, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=url) as ssock:
                ssock.do_handshake()
                cert = ssock.getpeercert()
        #print(cert)
        issuer = dict(x[0] for x in cert['issuer'])
        issued_by = issuer['organizationName']
        #retreive certificate age
        notAfter = datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
        notBefore = datetime.strptime(cert['notBefore'], "%b %d %H:%M:%S %Y %Z")
        certificate_age = notAfter - notBefore
        if issued_by in certificate_authorities and certificate_age.days >= 365 and check_https(url):
            return 1
        elif issued_by not in certificate_authorities and check_https(url):
            return 0
        else :
            return -1
    except :
        return -1

#1.1.9.	Domain Registration Length
import whois


def getDomainExperiationDateByDays(domain):
    try:
        q = whois.query(domain)
        if isinstance(q.expiration_date, list):
            expiration_date = q.expiration_date[0]
        else:
            expiration_date = q.expiration_date
        if isinstance(q.updated_date, list):
            updated_date = q.updated_date[0]
        else:
            updated_date = q.updated_date

        reg_length = expiration_date - updated_date

        days_to_expire = reg_length.days
        return days_to_expire
    except:
        return None

def check_domain_reg_length(inp):
    days = getDomainExperiationDateByDays(inp)
    if days != None :
        if(days >= 365) : return 1
        else : return -1
    return -1


from bs4 import BeautifulSoup
import requests


#1.1.10.	Favicon
def getFavicon(domain):
    try:
        page = requests.get(domain)
        soup = BeautifulSoup(page.text, features="html.parser")
        icon_link = soup.find("link", rel="shortcut icon")
        if icon_link is None:
            icon_link = soup.find("link", rel="icon")
        if icon_link is None:
            return domain + '/favicon.ico'
        return icon_link["href"]
    except:
        return None


def check_favicon(inp):
    favicon = getFavicon(inp)
    if get_domain_name(inp) == get_domain_name(favicon):
        return 1
    return -1


#1.1.11.	Using Non-Standard Port 

def check_port(inp):
    url = urlparse(inp)
    if url.port is not None and url.port!= 80 and url.port!= 443:
        return -1
    else:
        return 1
    

#1.1.12.	The Existence of “HTTPS” Token in the Domain Part of the URL

def check_fake_http(inp):
    domain = urlparse(inp).netloc
    if 'https' in domain:
        return -1
    else:
        return 1



def CHECK_ALL(inp):
    result_list = []
    result_list.append(check_ip_address(inp))
    result_list.append(check_string_length(inp))
    result_list.append(check_url_shortener(inp))
    result_list.append(check_at_symbol(inp))
    result_list.append(check_redirecting(inp))
    result_list.append(check_prefix(inp))
    result_list.append(check_sub_domain(inp))
    result_list.append(get_certificate_info(inp))
    result_list.append(check_domain_reg_length(inp))
    result_list.append(check_favicon(inp))
    result_list.append(check_port(inp))
    result_list.append(check_fake_http(inp))
    return result_list
