from fastapi_cloudauth.cognito import (Cognito, CognitoClaims,
                                       CognitoCurrentUser)

from ....utils.config import AWSConfig

get_current_user = CognitoCurrentUser(
    region=AWSConfig.REGION_NAME,
    userPoolId=AWSConfig.COGNITO_USERPOOL_ID,
    client_id=AWSConfig.COGNITO_CLIENT_ID,
)
