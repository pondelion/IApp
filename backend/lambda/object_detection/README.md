
## Deploy

```bash
$ set -o allexport
$ source .env
$ set +o allexport
```

- Create repository

```bash
$ aws ecr create-repository --repository-name iapp-lambda-object-detection
```

- Docker CLI Authentication

```bash
$ sudo aws ecr get-login-password --region ap-northeast-1 | sudo docker login --username AWS --password-stdin ${ECR_RESISTORY_ID}.dkr.ecr.ap-northeast-1.amazonaws.com
```

- build

```bash
$ sudo docker build -t iapp-lambda-object-detection -f docker/Dockerfile .
```

- Tagging

```bash
$ sudo docker tag iapp-lambda-object-detection:latest ${ECR_RESISTORY_ID}.dkr.ecr.ap-northeast-1.amazonaws.com/iapp-lambda-object-detection:latest
```

- Push to ECR

```bash
$ sudo docker push ${ECR_RESISTORY_ID}.dkr.ecr.ap-northeast-1.amazonaws.com/iapp-lambda-object-detection:latest
```

- test

```bash
$ TOKEN=***
$ curl -X POST https://********.execute-api.ap-northeast-1.amazonaws.com/dev/api/v1/detect_object -H "Authorization: ${TOKEN}" -d "{'image_urls': ['https://ultralytics.com/images/zidane.jpg']}"
```
