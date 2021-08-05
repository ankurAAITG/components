import io
import boto3
import numpy as np
import pandas as pd
from PIL import Image

def read_object(path, bucket, s3_client = None):
    
    if s3_client is None:
        s3_client = boto3.client('s3')
        
    obj = s3_client.get_object(Bucket = bucket, Key = path)
    
    return obj

def read_csv(path, bucket, s3_client = None):
    
    obj = read_object(path, bucket, s3_client)
    df = pd.read_csv(io.BytesIO(obj['Body'].read()))
    
    return df

def read_txt(path, bucket, s3_client = None):
    
    obj = read_object(path, bucket, s3_client)
    
    return obj['Body'].read()

def read_image(path, bucket, output = 'np', resize_width = None, s3_client = None):
    
    if s3_client is None:
        s3_client = boto3.client('s3')
    
    outfile = io.BytesIO()
    s3_client.download_fileobj(bucket, path, outfile)
    outfile.seek(0)
    img = Image.open(outfile)
    if resize_width is not None:
        wpercent = (resize_width/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((resize_width, hsize), Image.ANTIALIAS)
    
    if output == 'np':
        return np.array(img)
    
    return img
    
    




    
    