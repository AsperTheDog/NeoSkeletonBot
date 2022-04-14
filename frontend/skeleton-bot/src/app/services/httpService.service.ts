import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { CookieService } from 'ngx-cookie';
import { Action } from '../utils/dataTypes/Action';
import { Board } from '../utils/dataTypes/Board';
import { User } from '../utils/dataTypes/User';
import { ValueType } from '../utils/dataTypes/ValueType';
import projConfig from '../../../../../configs/config.json';
import extraConfs from 'extraConfigs.json';

@Injectable({
  providedIn: 'root'
})
export class httpService {
  constructor(public http: HttpClient, private cookieService: CookieService) {
    const cookieToken = this.cookieService.get('token')
    this.cookieParam = new HttpParams()
    if (cookieToken){
      this.cookieParam = this.cookieParam.append('token', cookieToken)
    }
    this.backendURL = (extraConfs.https ? "https://" : "http://") + projConfig.rootAddr + ":" + projConfig.backPort.toString() + "/"
    this.loginRef = encodeURIComponent(this.backendURL + "login");
  }

  loginRef: string;
  backendURL: string;
  cookieParam: HttpParams;


  getBoards(guild: number){
    const boardURL = this.backendURL + "boards"
    const payload = this.cookieParam.append('guild', guild)
    return this.http.get<Board[]>(boardURL, {params: payload})
  }
  
  getActions(guild: number){
    const actURL = this.backendURL + "actions"
    const payload = this.cookieParam.append('guild', guild)
    return this.http.get<Action[]>(actURL, {params: payload})
  }

  getGuilds(){
    const guildURL = this.backendURL + "guilds"
    return this.http.get<{icon: string, id: number, name: string}[]>(guildURL, {params: this.cookieParam})
  }

  getCreds(usrCode: string){
    const actURL = this.backendURL + "credentials"
    const payload = this.cookieParam.append('code', usrCode)
    return this.http.get<{token: string, usr: User}>(actURL, {params: payload})
  }

  saveBoard(activeBoard: Board){
    const delURL = this.backendURL + "boards"
    return this.http.post<{status: boolean}>(delURL, activeBoard)
  }

  getBoard(guild: number, name: string){
    const payload = this.cookieParam
    const revURL = this.backendURL + "boards/" + guild + "/" + name
    return this.http.get<Board>(revURL, {params: payload})
  }

  putCookie(name: string, token: string) {
    this.cookieService.put(name, token)
    this.cookieParam = new HttpParams().append('token', token)
  }

  removeCookie() {
    this.cookieService.remove('token')
  }

  deleteBoard(selectedGuild: number, activeBoard: string) {
    const delURL = this.backendURL + "boards/" + selectedGuild + "/" + activeBoard
    return this.http.delete(delURL)
  }

  getGlobalEvents() {
    const delURL = this.backendURL + "globalEvents"
    return this.http.get<{events:string[], customActionEvents:string[]}>(delURL)
  }

  getValueTypes() {
    const delURL = this.backendURL + "valueTypes"
    return this.http.get<ValueType[]>(delURL)
  }
}