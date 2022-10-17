import { atom, selector } from 'recoil';
import { userPool } from '../aws/Cognito';


export type AuthState = {
  isSignedIn: boolean
  signedInUsername: string | null
  accessToken: string | null
}

export const rclStateIsSignedIn = atom<boolean>({
  key: 'auth.is_signed_in',
  default: false,
});
export const rclStateSignedInUsername = atom<string | null>({
  key: 'auth.signed_in_username',
  default: null,
});
export const rclStateAccessToken = atom<string | null>({
  key: 'auth.access_token',
  default: null,
});
export const rclStateGuestMode = atom<boolean>({
  key: 'auth.guest_mode',
  default: false,
});
export const rclSignOut = selector<boolean>({
  key: 'auth.sign_out',
  get: ({ get }) => {
    return !get(rclStateIsSignedIn)
  },
  set: ({ set }, newValue: any) => {
    const cognitoUser = userPool.getCurrentUser()
    if (cognitoUser) {
      cognitoUser.signOut();
      localStorage.clear();
      console.log('signed out');
      set(rclStateIsSignedIn, false);
      set(rclStateSignedInUsername, null);
      set(rclStateAccessToken, null);
    } else {
      localStorage.clear();
      console.log('no user signed in');
    }
    // set(rclStateIsSignedOut, true);
    set(rclStateIsSignedIn, false);
    set(rclStateGuestMode, false);
  },
});
export const rclStateAuth = selector<AuthState>({
  key: 'auth.all_info',
  get: ({ get }) => {
    const isSignedIn = get(rclStateIsSignedIn)
    const signedInUsername = get(rclStateSignedInUsername)
    const accessToken = get(rclStateAccessToken)
    return { isSignedIn, signedInUsername, accessToken }
  },
  set: ({ set }, newValue: any) => {
    set(rclStateIsSignedIn, newValue.isSignedIn);
    set(rclStateSignedInUsername, newValue.signedInUsername);
    set(rclStateAccessToken, newValue.accessToken);
  }
});
