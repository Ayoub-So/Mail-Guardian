
def url_from_origin_url(url,domain):
    #url = url.removeprefix("https://").removeprefix("http://").removeprefix("www.")
    parsed_url = urlparse(url)
    if domain in parsed_url.netloc or parsed_url.netloc == '':
        return 1
    else:
        return 0
