import re

import whois
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from methods import url_from_origin_url

#1.2. Abnormal Based Features

#   1.2.1. Request URL

def check_external_objects(url):
    # Fetch the webpage content
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return -1

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract all the src attributes from img, video, and audio tags
        src_attributes = [img['src'] for img in soup.find_all('img', src=True)] + \
                         [video['src'] for video in soup.find_all('video', src=True)] + \
                         [audio['src'] for audio in soup.find_all('audio', src=True)]

        # Extract the domain of the webpage
        domain = urlparse(url).netloc
        # Check if each src URL is from a different domain
        external_objects = []
        for src in src_attributes:
            parsed_src = urlparse(src)
            if not ("https://"+domain in parsed_src.path or parsed_src.path[0] == '/'):
                external_objects.append(src)
        url_percentage = (len(external_objects)/len(src_attributes))*100
        if url_percentage < 22:
            return 1
        elif url_percentage>=22 and url_percentage <=61:
            return 0
        else:
            return -1
    except:
        return -1
#   1.2.2. URL of Anchor
def URL_of_Anchor(url):
    # Fetch the webpage content
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return -1

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract all the src attributes from img, video, and audio tags
        src_href=[]
        for a in soup.find_all('a'):
            src_href.append(a.get('href'))

        # Extract the domain of the webpage
        domain = urlparse(url).netloc
        # Check if each src URL is from a different domain
        external_objects = []
        for src in src_href:
            parsed_src = urlparse(src)
            if parsed_src.netloc:
                if not domain.removeprefix("https://").removeprefix("http://").removeprefix("www.") in parsed_src.netloc:
                    external_objects.append(src)
        url_percentage = (len(external_objects)/len(src_href))*100
        if url_percentage < 31:
            return 1
        elif url_percentage>=31 and url_percentage <=67:
            return 0
        else:
            return -1
    except:
        return -1
#   1.2.3. Links in <Meta>, <Script> and <Link> tags
def Links(url): #ftech links in meta, script and link tags
    # Fetch the webpage content
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return -1

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract all the src attributes from img, video, and audio tags
        src_href=[]
        for item in soup.find_all('meta'):
            src_href.append(item.get('content'))
        for item in soup.find_all('link'):
            src_href.append(item.get('href'))

        # Extract the domain of the webpage
        domain = urlparse(url).netloc
        # Check if each src URL is from a different domain
        external_objects = []
        for src in src_href:
            parsed_src = urlparse(src)
            if parsed_src.netloc:
                if not domain.removeprefix("https://").removeprefix("http://").removeprefix("www.") in parsed_src.netloc:
                    external_objects.append(src)
        url_percentage = (len(external_objects)/len(src_href))*100
        if url_percentage < 17:
            return 1
        elif url_percentage>=17 and url_percentage <=81:
            return 0
        else:
            return -1
    except:
        return -1
#   1.2.4. Server Form Handler (SFH)
def detect_empty_or_about_blank(url):
    # Fetch the webpage content
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return -1

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        domain = urlparse(url).netloc

        # Extract all the src attributes from img, video, and audio tags
        forms = soup.find_all('form')
        for form in forms:
            action = form.get('action')
            if action == '' or action.lower() == 'about:blank':
                return -1
            elif url_from_origin_url(url, domain):
                return 1
            else:
                return 0
    except:
        return -1

#   1.2.5. Submitting Information to Email
def detect_mailto_links(url):
    # Fetch the webpage content
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            # Find all anchor elements (links)
            links = soup.find_all('a', href=True)
            mailto_links = []
            for link in links:
                href = link.get('href', '').strip()
                # Check if the link is a mailto link
                if href.startswith('mailto:'):
                    return -1
                else:
                    return 1
    except:
        return -1
#   1.2.6. Abnormal URL
def abnormal_url(url):
    return 1

#   1.3. HTML and JavaScript based Features

#   1.3.1. Website Forwarding
def check_redirects(url):
    try:
        response = requests.head(url, allow_redirects=True)
        num_redirects = len(response.history)
        return num_redirects
    except :
        return -1

def classify_website(url):
    num_redirects = check_redirects(url)
    if num_redirects is not None:
        if num_redirects <= 1:
            return 1
        elif num_redirects >= 2 and num_redirects <= 4:
            return 0
        else:
            return -1
    else:
        return -1

#   1.3.2. Status Bar Customization
def check_status_bar_changes(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            javascript_code = response.text
            # Search for onMouseOver event handlers in JavaScript code
            mouseover_events = re.findall(r'onmouseover\s*=\s*["\']([^"\']+)["\']', javascript_code, re.IGNORECASE)
            for event_handler in mouseover_events:
                if 'window.status' in event_handler:
                    return -1  # JavaScript code changes status bar
            return 1  # No status bar changes found
        else:
            return -1
    except:
        return -1

#   1.3.3. Disabling Right Click
def rightClick(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            javascript_code = response.text
            # Search for onMouseOver event handlers in JavaScript code
            if re.findall(r"event.button ?== ?2", javascript_code, re.IGNORECASE):
                return 1
            else:
                return -1
        else:
            return -1
    except:
        return -1

#   1.3.4. Using Pop-up Window
def check_popups(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            popups = soup.find_all(lambda tag: tag.name == 'div' and tag.get('class') and 'popup' in tag.get('class'))
            for popup in popups:
                popup_content = popup.get_text().strip()
                # Check if the popup contains text related to personal information submission
                if "personal information" in popup_content.lower() or "submit" in popup_content.lower():
                    return -1  # Found suspicious pop-up asking for personal information
            return 1  # No suspicious pop-ups found
        else:
            return -1
    except:
        return -1

#   1.3.5. IFrame Redirection
def check_invisible_iframe(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            iframes = soup.find_all('iframe')
            for iframe in iframes:
                if iframe.get('frameborder') == '0' and iframe.get('style') == 'border:none;':
                    return -1  # Invisible iframe without frame borders found
            return 1  # No such iframe found
        else:
            return -1
    except :
        return -1



#   1.4. Domain based Features

#   1.4.1. Age of Domain
def get_domain_age(domain_name):
    try:
        # Query WHOIS information for the domain
        domain_info = whois.whois(domain_name)

        # Extract creation date
        creation_date = domain_info.creation_date

        # If creation_date is a list, consider the first element (usually the creation date)
        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        # Calculate age
        if isinstance(creation_date, datetime):
            current_date = datetime.now()
            age = current_date - creation_date
            if age.days >= 182:
                return 1
            else:
                return -1
        else:
            return -1  # Unable to determine creation date
    except:
        return -1

#   1.4.2. DNS Record
def DNS_record(domain_name):
    try:
        domain_info = whois.whois(domain_name)
        if(domain_info):
            return 1
        else:
            return -1
    except :
        return -1

#   1.4.3. Website Traffic
def get_global_rank(domain_name):
    url = f"https://www.similarweb.com/website/{domain_name}/"
    response = requests.get(url)

    #print(response.content)
    if response.status_code == 200:
        data = response.json()
        #print(data)
        #global_rank = data.get('globalRank', {}).get('rank', None)
       # if global_rank is not None:
        #    return global_rank'''
    return 1

#   1.4.4. PageRank
def page_link(url):
    return 1

#   1.4.5. Google Index
def is_indexed_by_google(url):
    try:
            # Perform a Google search query
        google_url = f"https://www.google.com/search?q=site:{url}"
        response = requests.get(google_url)
        if response.status_code == 200:
            # Parse the HTML of the search results page
            soup = BeautifulSoup(response.text, 'html.parser')
            # Check if the URL appears in the search results
            search_results = soup.find_all('a')
            for result in search_results:
                if str(result).find(f'{url}'):
                    return 1
            return -1
        else:
            return -1
    except :
        return -1

#   1.4.6. Number of Links Pointing to Page
def number_links_pointing_to_page(url):
    try:
            # Perform a Google search query
        google_url = f"https://www.google.com/search?q=site:{url}"
        response = requests.get(google_url)
        if response.status_code == 200:
            # Parse the HTML of the search results page
            soup = BeautifulSoup(response.text, 'html.parser')
            # Check if the URL appears in the search results
            search_results = soup.find_all('a')
            number_links=0
            for result in search_results:
                if str(result).find(f'{url}'):
                    number_links += 1
                    if(number_links>=3):
                        return 1
            return -1
        else:
            #print("Failed to perform Google search:", response.status_code)
            return -1
    except:
        return -1

#   1.4.7. Statistical-Reports Based Feature
def is_phishing(domain):
    return 0
    try:
        api_url = "http://checkurl.phishtank.com/checkurl/"
        params = {
            "format": "json",
            "url": domain
        }
        response = requests.post(api_url, data=params)
        #print(response)
        if response.status_code == 200:
            data = response.json()
            if data["meta"]["status"] == "success":
                in_database = data["results"]["in_database"]
                if in_database:
                    phishy = data["results"]["phishy"]
                    if phishy:
                        return -1
        return 1
    except:
        return 0


from attrib_part1 import CHECK_ALL
def extract_features(url):
    features_list = []
    features_list += CHECK_ALL(url)
    features_list.append(check_external_objects(url))
    features_list.append(URL_of_Anchor(url))
    features_list.append(Links(url))
    features_list.append(detect_empty_or_about_blank(url))
    features_list.append(detect_mailto_links(url))
    features_list.append(abnormal_url(url))
    features_list.append(classify_website(url))
    features_list.append(check_status_bar_changes(url))
    features_list.append(rightClick(url))
    features_list.append(check_popups(url))
    features_list.append(check_invisible_iframe(url))
    features_list.append(get_domain_age(url))
    features_list.append(DNS_record(url))
    features_list.append(get_global_rank(url))
    features_list.append(page_link(url))
    features_list.append(is_indexed_by_google(url))
    features_list.append(number_links_pointing_to_page(url))
    features_list.append(is_phishing(url))
    return features_list


