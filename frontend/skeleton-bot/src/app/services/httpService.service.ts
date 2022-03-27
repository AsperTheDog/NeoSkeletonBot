import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { CookieService } from 'ngx-cookie';
import { AppComponent } from '../app.component';
import { Action } from '../utils/dataTypes/Action';
import { Board } from '../utils/dataTypes/Board';
import { User } from '../utils/dataTypes/User';
import { ValueType } from '../utils/dataTypes/ValueType';

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
  }

  backendURL: string = "https://freechmod.ddns.net:12546/";
  cookieParam: HttpParams;


  getBoards(guild: string){
    const boardURL = this.backendURL + "boards"
    const payload = this.cookieParam.append('guild', guild)
    return this.http.get<Board[]>(boardURL, {params: payload})
  }
  
  getActions(guild: string){
    const actURL = this.backendURL + "actions"
    const payload = this.cookieParam.append('guild', guild)
    return this.http.get<Action[]>(actURL, {params: payload})
  }

  getGuilds(){
    const guildURL = this.backendURL + "getGuilds"
    return this.http.get<{icon: string, id: string, name: string}[]>(guildURL, {params: this.cookieParam})
  }

  getCreds(usrCode: string){
    const actURL = this.backendURL + "checkCreds"
    const payload = this.cookieParam.append('code', usrCode)
    return this.http.get<{token: string, usr: User}>(actURL, {params: payload})
  }

  saveBoard(activeBoard: Board){
    return this.http.post<{status: boolean}>(this.backendURL + "saveBoard", activeBoard)
  }

  getBoard(guild: string, name: string){
    const payload = this.cookieParam.append('guild', guild).append('name', name)
    const revURL = this.backendURL + "revertBoard"
    return this.http.get<Board>(revURL, {params: payload})
  }

  putCookie(name: string, token: string) {
    this.cookieService.put(name, token)
    this.cookieParam = new HttpParams().append('token', token)
  }

  removeCookie(name: string) {
    this.cookieService.remove('token')
  }

  deleteBoard(selectedGuild: string, activeBoard: string) {
    const delURL = this.backendURL + "deleteBoard/" + selectedGuild + "/" + activeBoard
    return this.http.delete(delURL)
  }

  getGlobalEvents() {
    const delURL = this.backendURL + "getGlobalEvents"
    return this.http.get<{events:string[], customActionEvents:string[]}>(delURL)
  }

  getValueTypes() {
    const delURL = this.backendURL + "getValueTypes"
    return this.http.get<ValueType[]>(delURL)
  }
}