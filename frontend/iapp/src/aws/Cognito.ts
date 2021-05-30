import {
  CognitoUserPool,
} from 'amazon-cognito-identity-js';
import awsConfiguration from './Config';


export const userPool = new CognitoUserPool({
  UserPoolId: awsConfiguration.USER_POOL_ID,
  ClientId: awsConfiguration.CLIENT_ID,
})
