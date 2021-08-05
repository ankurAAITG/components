import requests

def get_from_url(url, typ = 'np', file_write_path = None):
    
    if typ == 'down':
        try:
            with viz_utils.DownloadProgressBar(unit='B', unit_scale=True,
                                               miniters=1, desc=url.split('/')[-1]) as t:
                urllib.request.urlretrieve(url, filename=file_write_path, reporthook=t.update_to)
            return (file_write_path, 200)
        except Exception as e:
            return (None, e)
    
    try:
        response = requests.get(url, stream=True)
    except Exception as e:
        return (None, e)
        
    if response.status_code == 200:
        try:
            if typ == 'raw':
                return (response.content, 200)
            elif typ == 'np':
                im = Image.open(response.raw)
                return (np.array(im, dtype = np.uint8), 200)            
        except Exception as e:
            return (None, e)
    else:
        return (None, response.status_code)