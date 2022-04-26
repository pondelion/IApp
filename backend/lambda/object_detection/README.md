
## Deploy

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

```bash
$ sudo -E sls deploy
```

- test


```bash
$ aws cognito-idp admin-initiate-auth --user-pool-id ${COGNITO_USER_POOL_ID} --client-id ${COGNITO_CLIENT_ID} --auth-flow ADMIN_NO_SRP_AUTH --auth-parameters USERNAME=${COGNITO_USERNAME},PASSWORD=${COGNITO_PASSWORD}
```

```bash
$ TOKEN=***
$ OBJECT_DETECT_URL=https://********.execute-api.ap-northeast-1.amazonaws.com/dev/api/v1/detect_object
$ curl -X POST ${OBJECT_DETECT_URL} -H "Authorization: ${TOKEN}" -H "Content-Type: application/json" -d "{'image_urls': ['https://ultralytics.com/images/zidane.jpg']}"
```
