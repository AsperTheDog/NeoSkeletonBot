import { Injectable } from '@angular/core';
import globalEventList from '../../assets/json/globalEvents.json';
import valueTypes from '../../assets/json/types.json';
import { Board } from '../utils/dataTypes/Board';
import { mouseData } from '../utils/dataTypes/Mouse';
import { Transition } from '../utils/dataTypes/Transition';
import { EventInput, ValueInput } from '../utils/dataTypes/Value';
import { Action } from '../utils/dataTypes/Action';
import { Variable } from '../utils/dataTypes/Variable';
import { GlobalEvent } from '../utils/dataTypes/GlobalEvent';
import { ValueType } from '../utils/dataTypes/ValueType';
import { ValueNode } from '../views/input/value/valueNode';
import { EventNode } from '../views/input/event/eventNode';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Pipeline } from '../utils/dataTypes/Pipeline';
import { VarElement } from '../utils/dataTypes/VarElement';
import { User } from '../utils/dataTypes/User';
import { CookieService } from 'ngx-cookie';

@Injectable({
  providedIn: 'root'
})
export class MainControllerService {
  constructor(public http: HttpClient, private cookieService: CookieService) {
    this.boards = new Map<string, Board>();
    this.usedIDs = new Map<number, any>();
    this.templateMap = new Map<number, Action>();
    this.valueTypeMap = new Map<number, ValueType>();

    this.globalEventList = globalEventList.events;
    this.pipelineTypes = globalEventList.customActionEvents;
    this.hoveringDelete = false;
    this.spawnLocation = { x: 0, y: 0 }
    this.mouse = new mouseData()

    this.allowedValues = [];
    for (let vTempl of valueTypes.types) {
      if (vTempl.canBeVar) {
        this.allowedValues.push([vTempl.id, vTempl.name])
      }
      this.valueTypeMap.set(vTempl.id, vTempl)
    }

    const cookieToken = this.cookieService.get('token')
    this.cookieParam = new HttpParams()
    if (cookieToken){
      this.cookieParam = this.cookieParam.append('token', cookieToken)
    }
  }

  usedIDs: Map<number, any>;
  boards: Map<string, Board>
  templateMap: Map<number, Action>;
  valueTypeMap: Map<number, ValueType>;

  globalEventList: string[];
  pipelineTypes: string[];
  actionTemplates: Action[];
  allowedValues: [number, string][];

  activeBoard: Board;
  boardList: string[];

  hoveringDelete: boolean;

  spawnLocation: { x: number, y: number }
  boardCoords: { x: number, y: number }

  transStartInput: ValueNode | EventNode | null = null;
  hovering: ValueNode | EventNode | null = null;
  mouse: mouseData;

  infoDisplayText: [string, boolean][] = [["", false], ["", false], ["This is the log, info about your actions will be shown here", false]];
  hasEvInput = false;

  backendURL: string = "https://freechmod.ddns.net:12546/";
  cookieParam: HttpParams;

  usr: User | undefined;
  usrCode: string;
  guilds: {icon: string, id: string, name: string}[] = []
  selectedGuild: string | undefined;

  loaded = true;
  cancelledChange = false;
  requestedBoard = "Main";

  manageInfo(newText: string, isError: boolean) {
    this.infoDisplayText.shift()
    this.infoDisplayText.push([newText, isError])
  }

  get(id: number | null) {
    if (id == null) return;
    return this.usedIDs.get(id)
  }

  getType(id: number) {
    return this.valueTypeMap.get(id)!
  }

  addTransition(data: Transition) {
    this.getID(data)
    this.activeBoard.transitions.push(data)
    const orig = this.get(data.origin[1])
    if (orig) orig.transitionNumber++;
    const dest = this.get(data.destination[1])
    if (dest) dest.transitionNumber++;
  }

  removeTransition(data: Transition | null = null) {
    var idx = -1;
    if (!data) {
      idx = this.activeBoard.transitions.length - 1
    }
    else {
      idx = this.activeBoard.transitions.indexOf(data)
    }
    const elem = this.activeBoard.transitions.splice(idx, 1)[0]
    const orig = this.get(elem.origin[1])
    if (orig) orig.transitionNumber--;
    const dest = this.get(elem.destination[1])
    if (dest) {
      dest.transitionNumber--;
      if (dest.transitionNumber == 0) {
        dest.fromVariable = false;
      }
    }

    this.usedIDs.delete(elem.id)
  }

  cleanTransitions(node: number, data: ValueInput | EventInput | null = null) {
    var check: { (trans: Transition): boolean; };
    if (data) {
      if (data.nature == "in") {
        check = (trans: Transition) => (data.id == trans.destination[1])
      }
      else {
        check = (trans: Transition) => (data.id == trans.origin[1])
      }
    }
    else {
      check = (trans: Transition) => (node == trans.origin[0] || node == trans.destination[0])
    }

    this.activeBoard.transitions = this.activeBoard.transitions.filter((trans) => {
      if (check(trans)) {
        const orig = this.get(trans.origin[1])
        if (orig) orig.transitionNumber--;
        const dest = this.get(trans.destination[1])
        if (dest) dest.transitionNumber--;
        this.usedIDs.delete(trans.id)
        return false;
      }
      return true;
    })
  }

  saveProcess(data: {status: boolean}) {
    let saved = false;
    if (!data.status){
      this.manageInfo("Parse error, could not save board", true)
      saved = false;
    }
    else {
      this.manageInfo("Saved changes", false)
      saved = true;
    }
    this.retrieveActions()
    return saved
  }

  save() {
    if (!this.usr || !this.selectedGuild) return;
    return this.http.post<{status: boolean}>(this.backendURL + "saveBoard", this.activeBoard)
  }

  getID(elem: Action | Variable | GlobalEvent | ValueInput | EventInput | Transition | Pipeline | VarElement) {
    var count = 0;
    while (this.usedIDs.has(count)) {
      count++;
    }
    elem.id = count;
    this.usedIDs.set(count, elem)
  }

  checkVarInstance(inst: number) {
    const val = this.activeBoard.variables.find((elem) => (elem.id == inst))
    if (!val) return;
    val.references--;
    if (val.references == 0) {
      this.activeBoard.variables.splice(this.activeBoard.variables.indexOf(val), 1)
    }
  }

  deleteElem(node: Action | Variable | GlobalEvent | Pipeline, type: string, spl:boolean = true) {
    this.cleanTransitions(node.id)
    if (type == 'var') {
      node = (node as Variable)
      this.usedIDs.delete(node.input.id)
      this.activeBoard.varInstances.splice(this.activeBoard.varInstances.indexOf(node), 1)
      this.checkVarInstance(node.varAttr)
      this.manageInfo("Deleted variable node", false)
    }
    else if (type == 'action') {
      node = (node as Action)
      node.inputs.forEach((input) => { this.usedIDs.delete(input.id) })
      node.outputs.forEach((input) => { this.usedIDs.delete(input.id) })
      node.events.forEach((input) => { this.usedIDs.delete(input.id) })
      this.usedIDs.delete(node.inputEvent.id)
      this.activeBoard.actions.splice(this.activeBoard.actions.indexOf(node), 1)
      this.manageInfo("Deleted action node", false)
    }
    else if (type == 'event') {
      node = (node as GlobalEvent)
      this.usedIDs.delete(node.output.id)
      this.usedIDs.delete(node.eventOutput.id)
      this.activeBoard.globalEvents.splice(this.activeBoard.globalEvents.indexOf(node), 1)
      this.manageInfo("Deleted event node", false)
    }
    else if (type == 'pipeline') {
      node = (node as Pipeline)
      if (node.point) {
        this.usedIDs.delete(node.point.id)
      }
      if (node.eventPoint) {
        this.usedIDs.delete(node.eventPoint.id)
      }
      if (spl){
        this.activeBoard.pipelines.splice(this.activeBoard.pipelines.indexOf(node), 1)
      }
      this.manageInfo("Deleted pipeline node", false)
      if (node.type == "actionEventInput") {
        this.hasEvInput = false;
      }
    }
  }

  checkIfDelete(node: Action | Variable | GlobalEvent | Pipeline, type: string) {
    if (!this.hoveringDelete) return;
    this.deleteElem(node, type)
  }

  getNewAction(templateID: number) {
    const getNewInputs = (templInputs: ValueInput[] | EventInput[], tp: string) => {
      var lst: any[] = [];
      for (let templInput of templInputs) {
        if (tp == "value") {
          var newVal: ValueInput;
          newVal = new ValueInput(0, templInput.name, (templInput as ValueInput).valueType, templInput.nature);
          newVal.comboValues = (templInput as ValueInput).comboValues
          this.getID(newVal)
          lst.push(newVal)
        }
        else {
          var newEv: EventInput;
          newEv = new EventInput(0, templInput.name, templInput.nature);
          this.getID(newEv)
          lst.push(newEv)
        }
      }
      return lst;
    }
    const templ = this.templateMap.get(templateID)!
    const newAct = new Action(
      0,
      templ.type,
      getNewInputs(templ.inputs, "value"),
      getNewInputs(templ.outputs, "value"),
      getNewInputs(templ.events, "event"),
      getNewInputs([templ.inputEvent], "event")[0]
    )
    this.getID(newAct)
    this.activeBoard.actions.push(newAct)
    newAct.cdkPos = {
      x: this.mouse.offset.x - 300,
      y: this.mouse.offset.y - 70
    }
    this.manageInfo("Created new Action Node of type '" + templ.type + "'", false)
  }

  getNewVariable(vr: Variable, vrElem: VarElement) {
    const prevVar = vrElem.constant ? undefined : this.activeBoard.variables.find((elem) => (vrElem.name == elem.name))
    this.getID(vr)
    this.getID(vr.input)
    this.getID(vr.output)
    if (prevVar) {
      prevVar.references++;
      vr.varAttr = prevVar.id
    }
    else {
      this.getID(vrElem)
      this.activeBoard.variables.push(vrElem)
      vrElem.references++;
      vr.varAttr = vrElem.id
    }
    this.activeBoard.varInstances.push(vr)
    vr.cdkPos = {
      x: this.mouse.offset.x - 300,
      y: this.mouse.offset.y - 70
    }
    this.manageInfo("Created new Variable Node", false)
  }

  getNewGEvent(ge: GlobalEvent) {
    this.getID(ge)
    this.getID(ge.output)
    this.getID(ge.eventOutput)
    this.activeBoard.globalEvents.push(ge)
    ge.cdkPos = {
      x: this.mouse.offset.x - 300,
      y: this.mouse.offset.y - 70
    }
    this.manageInfo("Created new Global Event Node '" + ge.name + "'", false)
  }

  getNewPipeline(ge: Pipeline) {
    this.getID(ge)
    if (ge.type == "actionEventInput" || ge.type == "actionEventOutput") {
      if (ge.type == "actionEventInput") {
        this.hasEvInput = true
      }
      this.getID(ge.eventPoint!)
    }
    else {
      this.getID(ge.point!)
    }
    this.activeBoard.pipelines.push(ge)
    ge.cdkPos = {
      x: this.mouse.offset.x - 300,
      y: this.mouse.offset.y - 70
    }
    this.manageInfo("Created new Pipeline Node '" + ge.name + "'", false)
  }

  changeBoard = (loadBoard: string, isNew: boolean, savePrev=true) => {
    const changeProcess = () => {
      if (isNew) {
        this.boards.set(loadBoard, new Board(loadBoard, this.selectedGuild!, [], [], [], [], [], []))
        this.boardList[this.boardList.length - 1] = loadBoard
        this.boardList.push("...")
      }
      this.activeBoard = this.boards.get(loadBoard)!
      if (loadBoard != "Main" && this.activeBoard.pipelines.find((elem) => (elem.type == "actionEventInput"))) {
        this.hasEvInput = true
      }
      else {
        this.hasEvInput = false
      }
      this.requestedBoard = this.activeBoard.name
      this.manageInfo("Loaded new schematic " + this.activeBoard.name, false)
    }

    if (!savePrev){
      changeProcess()
    }
    else{
      this.save()!.subscribe((data) => {
        const saved = this.saveProcess(data)
        if (!saved){
          const confr = confirm("The board could not be saved, do you want to undo changes?")
          if (!confr){
            this.requestedBoard = this.activeBoard.name
            return;
          }
          this.revertBoard(this.activeBoard.name)
        }
        changeProcess()
      })
    }
  }

  clearBoard() {
    if (!this.usr || !this.selectedGuild) return;
    const conf = confirm("Are you sure you want to clear the board?")
    if (!conf) return;
    const elems: [Action[], Variable[], Pipeline[], GlobalEvent[]] = [[], [], [], []]
    for (let act of this.activeBoard.actions){
      this.deleteElem(act, "action", false)
      elems[0].push(act)
    }
    for (let vr of this.activeBoard.varInstances){
      this.deleteElem(vr, "var", false)
      elems[1].push(vr)
    }
    for (let pipe of this.activeBoard.pipelines){
      this.deleteElem(pipe, "pipeline", false)
      elems[2].push(pipe)
    }
    for (let ev of this.activeBoard.globalEvents){
      this.deleteElem(ev, "event", false)
      elems[3].push(ev)
    }
    for (let elem of elems[0]){
      this.activeBoard.actions.splice(this.activeBoard.actions.indexOf(elem), 1)
    }
    for (let elem of elems[1]){
      this.activeBoard.varInstances.splice(this.activeBoard.varInstances.indexOf(elem), 1)
    }
    for (let elem of elems[2]){
      this.activeBoard.pipelines.splice(this.activeBoard.pipelines.indexOf(elem), 1)
    }
    for (let elem of elems[3]){
      this.activeBoard.globalEvents.splice(this.activeBoard.globalEvents.indexOf(elem), 1)
    }
    this.activeBoard.variables = []
    this.activeBoard.transitions = []
  }

  includeIDs(bd: Board) {
    for (let action of bd.actions) {
      this.usedIDs.set(action.id, action)
      for (let input of action.inputs) {
        this.usedIDs.set(input.id, input)
      }
      for (let output of action.outputs) {
        this.usedIDs.set(output.id, output)
      }
      for (let event of action.events) {
        this.usedIDs.set(event.id, event)
      }
      this.usedIDs.set(action.inputEvent.id, action.inputEvent)
    }
    for (let variable of bd.varInstances) {
      this.usedIDs.set(variable.id, variable)
      this.usedIDs.set(variable.input.id, variable.input)
      this.usedIDs.set(variable.output.id, variable.output)
    }
    for (let variable of bd.variables) {
      this.usedIDs.set(variable.id, variable)
    }
    for (let transition of bd.transitions) {
      this.usedIDs.set(transition.id, transition)
    }
    for (let gEvent of bd.globalEvents) {
      this.usedIDs.set(gEvent.id, gEvent)
      this.usedIDs.set(gEvent.output.id, gEvent.output)
      this.usedIDs.set(gEvent.eventOutput.id, gEvent.eventOutput)
    }
    for (let pipe of bd.pipelines) {
      this.usedIDs.set(pipe.id, pipe)
      if (pipe.point) {
        this.usedIDs.set(pipe.point.id, pipe.point)
      }
      if (pipe.eventPoint) {
        this.usedIDs.set(pipe.eventPoint.id, pipe.eventPoint)
      }
    }
  }

  changeVarElems(oldName: string, newName: string) {
    const prevVar = this.activeBoard.variables.find((elem) => (oldName == elem.name))!
    this.checkVarInstance(prevVar.id)
    const newVar = this.activeBoard.variables.find((elem) => (newName == elem.name))!
    if (newVar) {
      newVar.references++;
      return newVar
    }
    const newVInst = new VarElement(newName, prevVar.valueType, prevVar.initialValue)
    this.getID(newVInst)
    this.activeBoard.variables.push(newVInst)
    newVInst.references++;
    return newVInst
  }

  retrieveBoards() {
    if (!this.selectedGuild) return;
    const boardURL = this.backendURL + "boards"
    const payload = this.cookieParam.append('guild', this.selectedGuild)
    this.http.get<Board[]>(boardURL, {params: payload}).subscribe(
      (response) => {
        this.usedIDs.clear()
        this.boards.clear()
        response.forEach((bd) => {
          this.boards.set(bd.name, bd)
          this.includeIDs(bd)
        })
        this.boardList = Array.from(this.boards.keys())
        this.boardList.push("...")
        this.activeBoard = this.boards.get("Main")!
        this.retrieveActions()
      },
      (error) => {
        console.log(error);
      }
    )
  }

  retrieveActions() {
    if (!this.selectedGuild) return;
    const actURL = this.backendURL + "actions"
    const payload = this.cookieParam.append('guild', this.selectedGuild)
    this.http.get<Action[]>(actURL, {params: payload}).subscribe(
      (response) => {
        this.actionTemplates = response
        this.templateMap.clear()
        this.actionTemplates.forEach((action) => {
          this.templateMap.set(action.id, action)
        })
    
        this.loaded = true;
      },
      (error) => {
        console.log(error);
      }
    )
  }

  checkCreds() {
    const actURL = this.backendURL + "checkCreds"
    const payload = this.cookieParam.append('code', this.usrCode)
    this.http.get<{token: string, usr: User}>(actURL, {params: payload}).subscribe(
      (response) => {
        this.cookieService.put('token', response.token)
        this.cookieParam = new HttpParams().append('token', response.token)
        if (response.usr.id){
          this.usr = new User(response.usr.id, response.usr.avatar, response.usr.discriminator, response.usr.username)

          const guildURL = this.backendURL + "getGuilds"
          this.http.get<{icon: string, id: string, name: string}[]>(guildURL, {params: this.cookieParam}).subscribe(
            (response2) => {
              this.guilds = response2
              if (this.guilds.length != 0)
                this.selectedGuild = this.guilds[0].id
              this.retrieveBoards()
            },
            (error) => {
              console.log(error);
            }
          )
        }
        else{
          this.usr = undefined
          this.loaded = true
        }
      },
      (error) => {
        console.log(error);
      }
    )
  }

  deleteBoard() {
    if (!this.usr || !this.selectedGuild) return;
    var confr = confirm("Are you sure you want to remove this board?")
    if (!confr) return;
    const delURL = this.backendURL + "deleteBoard/" + this.selectedGuild + "/" + this.activeBoard.name
    this.changeBoard('Main', false, false)
    this.http.delete(delURL).subscribe(
      (response) => {
        this.retrieveBoards()
      },
      (error) => {
        console.log(error);
      }
    )
  }

  logout() {
    this.cookieService.remove('token')
    this.usr = undefined;
    this.selectedGuild = undefined;
  }

  changeGuilds() {
    this.loaded = false
    this.retrieveBoards()
  }

  revertBoard(name: string) {
    if (!this.selectedGuild) return;
    const payload = this.cookieParam.append('guild', this.selectedGuild).append('name', name)
    const revURL = this.backendURL + "revertBoard"
    this.http.get<Board>(revURL, {params: payload}).subscribe(
      (response) => {
        this.boards.set(name, response)
        console.log(this.boards.get(name))
      },
      (error) => {
        console.log(error)
      }
    )
  }
}