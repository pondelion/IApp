import base64
from datetime import datetime
import os
import json
import pickle
import io
import sys
import urllib
sys.path.append('./yolov5')

import boto3
import requests


DYNAMODB_TABLE_NAME = os.environ['DYNAMODB_TABLE_NAME']
model = None
print('start loading model')
with open('model/model_yolov5s.pkl', mode='rb') as f:
    model = pickle.load(f)
print('done loading model')
s3 = boto3.client('s3')
dynamodb = boto3.client('dynamodb')


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
        tmp_img_filepath = os.path.join(
            '/tmp', os.path.basename(img_url)
        )
        bucket = img_url.strip('s3://').split('/')[0]
        key = '/'.join(img_url.strip('s3://').split('/')[1:])
        s3.download_file(bucket, key, tmp_img_filepath)
        results = model(tmp_img_filepath)
    else:
        raise ValueError(f'Invalid image url : {img_url}')
    return [{
        'label': model.names[int(res[5])],
        'rect': res[:4].astype(str).tolist(),
        'conf': str(res[4]),
    } for res in results.xyxy[0].numpy()]


def detect_image_batch(imgs):
    batch_results = model(imgs)
    return [[{
        'label': model.names[int(res[5])],
        'rect': res[:4].tolist(),
        'conf': res[4],
    } for res in results.numpy()] for results in batch_results.xyxy]


def save_results2dynamodb(results, bucket, file_key):
    print(f'save_results2dynamodb : {results}')
    if DYNAMODB_TABLE_NAME == 'irld-object-detection':
        item = {
            'device_name': file_key.split('/')[0],
            's3_filepath': os.path.join(f's3://{bucket}', file_key),
            'od_result': results,
            'datetime': datetime.now()
        }
        dynamodb.put_item(TableName=DYNAMODB_TABLE_NAME, Item=item)


def detect_object_api(event, context):
    print('detect_object_api')
    print(event)
    if 'image_urls' in event['body']:
        image_urls = event['body']['image_urls']
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
            tmp_img_filepath = os.path.join(
                '/tmp', os.path.basename(key)
            )
            s3.download_file(bucket, key, tmp_img_filepath)
            results = model(tmp_img_filepath)
            results = [{
                'label': model.names[int(res[5])],
                'rect': res[:4].astype(str).tolist(),
                'conf': str(res[4]),
            } for res in results.xyxy[0].numpy()]
            save_results2dynamodb(results, bucket, key)
        except Exception as e:
            print(e)
            raise e
    else:
        raise Exception()
