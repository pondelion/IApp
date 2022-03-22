import base64
from datetime import datetime
import os
import json
import pickle
import io

import boto3
import requests


DYNAMODB_TABLE_NAME = os.environ['DYNAMODB_TABLE_NAME']
model = None
with open('model/model_yolov5s.pkl', mode='rb') as f:
    model = pickle.load(f)
s3 = boto3.client('s3')


def detect_image(img_url: str):
    if img_url.startswith('http'):
        results = model(img_url)
    elif img_url.startswith('data:image'):
        header, encoded = img_url.split(',', 1)
        img = base64.b64decode(encoded)
        img = np.frombuffer(img, dtype=np.uint8)
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
        results = model(img)
    elif img_url.startswith('s3://'):
        tmp_img_filepath = os.path.basename(img_url)
        bucket = img_url.strip('s3://').split('/')[0]
        key = '/'.join(img_url.strip('s3://').split('/')[1:])
        s3.download_file(bucket, key, tmp_img_filepath)
        results = model(tmp_img_filepath)
    else:
        raise ValueError(f'Invalid image url : {img_url}')
    return [{
        'label': model.names[int(res[5])],
        'rect': res[:4].tolist(),
        'conf': res[4],
    } for res in results.xyxy[0].numpy()]


def detect_image_batch(imgs):
    batch_results = model(imgs)
    return [{
        'label': model.names[int(res[5])],
        'rect': res[:4].tolist(),
        'conf': res[4],
    } for res in results.numpy() for results in batch_results.xyxy]


def save_results2dynamodb(results):
    print(results)


def detect_object_api(event, context):
    print('detect_object_api')
    print(event)
    if 'image_urls' in event:
        image_urls = event['image_urls']
        if not isinstance(image_urls, list):
            image_urls = [image_urls]
        results_list = []
        for image_url in image_urls:
            results = detect_image(image_url)
            results_list.append(results)
        return {
            'statusCode': 200,
            'body': json.dumps({
                'pred_results' : results_list
            }),
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': 'true'
            },
        }
    else:
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': 'true'
            },
        }


def detect_object_s3_trigger(event, context):
    print('detect_object_s3_trigger')
    print(event)
    if 'Records' in event and 's3' in event['Records'][0]:
        # triggered from s3 put event
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
        try:
            tmp_img_filepath = os.path.basename(key)
            s3.download_file(bucket, key, tmp_img_filepath)
            results = model(tmp_img_filepath)
            save_results2dynamodb(results)
        except Exception as e:
            print(e)
            raise e
    else:
        raise Exception()
