import axios from 'axios';
import { Settings } from '../Settings';


class TwitterAPI {

  private host: string;
  private port: number;
  private baseAPI;

  constructor(host?: string, port?: number) {
    this.host = host ? host : Settings.BACKEND_APISERVER_HOST;
    this.port = port ? port : Settings.BACKEND_APISERVER_PORT;
    this.baseAPI = axios.create({
      baseURL: `http://${this.host}:${this.port}/api/v1/twitter`
    });
  }

  async getTweetByUsername(userName: string, count: number = 50) {
    const params: any = {}
    params['count'] = count
    return this.baseAPI.get(`tweet/${userName}`, { params: params })
  }

  async getMediaByUsername(userName: string) {
    const params: any = {}
    params['user_name'] = userName
    return this.baseAPI.get(`media`, { params: params })
  }

  // async getStockprice(
  //   code: number,
  //   year?: number, month?: number, day?: number,
  //   accessToken?: string,
  // ) {
  //   const params: any = {}
  //   if (year) {
  //     params['year'] = year
  //   }
  //   if (month) {
  //     params['month'] = month
  //   }
  //   if (day) {
  //     params['day'] = day
  //   }
  //   return this.baseAPI.get(`stockprice/${code}`, { params: params })
  // }
}

export default TwitterAPI;
