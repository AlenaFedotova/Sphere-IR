import urllib

urls = open("./data/urls.wikipedia.examined").readlines() + open("./data/urls.wikipedia.general").readlines()

for segment in urls:
    try:
        segment = urllib.unquote(segment).decode('utf8')   
    except UnicodeDecodeError:
        try:
            segment = urllib.unquote(segment).decode('cp1251')
        except UnicodeDecodeError:
            pass
    print segment
