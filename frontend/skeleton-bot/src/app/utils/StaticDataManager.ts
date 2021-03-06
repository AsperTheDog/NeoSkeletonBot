import { Action } from "./dataTypes/Action";
import { User } from "./dataTypes/User";
import { ValueType } from "./dataTypes/ValueType";

export class TemplateManager {
  constructor () {
    this.templateMap = new Map<number, Action>();
    this.groups = new Map<string, Action[]>();
  }

  actionTemplates: Action[];
  filteredTemplates: Action[];
  groups: Map<string, Action[]>;
  templateMap: Map<number, Action>;
  filterStr: string = "";
  
  getTemplate(templateID: number) {
    return this.templateMap.get(templateID)!
  }
  
  insertActions(newActions: Action[]) {
    this.actionTemplates = newActions
    this.templateMap.clear()
    this.actionTemplates.forEach((action) => {
      this.templateMap.set(action.id, action)
    })
    this.filteredTemplates = this.actionTemplates
    this.fillGroups()
  }

  updateFilters(){
    this.filteredTemplates = []
    for (let act of this.actionTemplates){
      if (act.type.toLowerCase().includes(this.filterStr.toLowerCase())){
        this.filteredTemplates.push(act)
      }
    }
    this.fillGroups()
  }

  fillGroups(){
    this.groups.clear()
    for (let act of this.filteredTemplates){
      if (!this.groups.has(act.group)){
        this.groups.set(act.group, [])
      }
      this.groups.get(act.group)!.push(act)
    }
  }
}

export class TypeValueManager {
  constructor () {
    this.valueTypeMap = new Map<number, ValueType>();
  }

  globalEventList: {name: string, struct: string}[];
  pipelineTypes: string[];
  allowedValues: [number, string][];
  valueTypeMap: Map<number, ValueType>;

  setGlobalEvents(gEvs: {name: string, struct: string}[]) {
    this.globalEventList = gEvs
  }

  setPipelineTypes(pipes: string[]) {
    this.pipelineTypes = pipes
  }

  setValueTypes(valTypes: ValueType[]) {
    this.allowedValues = [];
    for (let vTempl of valTypes) {
      if (vTempl.canBeVar) {
        this.allowedValues.push([vTempl.id, vTempl.name])
      }
      this.valueTypeMap.set(vTempl.id, vTempl)
    }
  }

  getType(id: number) {
    return this.valueTypeMap.get(id)!
  }

  getStruct(name: string){
    for (let gev of this.globalEventList){
      if (gev.name == name){
        return gev.struct
      }
    }
    return ""
  }
}

export class SessionManager {
  constructor () {

  }
  
  usr: User | undefined;
  usrCode: string;
  guilds: {icon: string, id: number, name: string}[] = []
  selectedGuild: number | undefined;

  sessionIsValid() {
    return this.usr && this.selectedGuild
  }

  getCode(): string {
    return this.usrCode
  }

  setCode(code: any) {
    this.usrCode = code
  }

  getGuild() {
    return this.selectedGuild
  }

  insertGuilds(guilds: {icon: string, id: number, name: string}[]) {
    this.guilds = guilds
    if (this.guilds.length != 0)
      this.selectedGuild = this.guilds[0].id
  }

  insertCreds(creds: {token: string, usr: User}) {
    if (creds.usr.id){
      this.usr = new User(creds.usr.id, creds.usr.avatar, creds.usr.discriminator, creds.usr.username)
    }
    else{
      this.usr = undefined
    }
  }
  
  removeSession() {
    this.usr = undefined;
    this.selectedGuild = undefined;
  }
}