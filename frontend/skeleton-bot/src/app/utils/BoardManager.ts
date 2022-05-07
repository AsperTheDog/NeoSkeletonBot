import { Action } from "./dataTypes/Action";
import { Board } from "./dataTypes/Board";
import { GlobalEvent } from "./dataTypes/GlobalEvent";
import { MouseData } from "./dataTypes/Mouse";
import { Pipeline } from "./dataTypes/Pipeline";
import { Transition } from "./dataTypes/Transition";
import { ValueInput, EventInput } from "./dataTypes/Value";
import { VarElement } from "./dataTypes/VarElement";
import { Variable } from "./dataTypes/Variable";

class IDManager {
  constructor () {
    this.usedIDs = new Map<number, any>();
  }

  usedIDs: Map<number, Map<number, any>>;

  getID(elem: {id: number}, guild: number) {
    let count = 0;
    if (!this.usedIDs.has(guild)){
      this.usedIDs.set(guild, new Map<number, any>())
    }
    while (this.usedIDs.get(guild)?.has(count)) {
      count++;
    }
    elem.id = count;
    this.usedIDs.get(guild)!.set(count, elem)
  }

  get(id: number | null, guild: number) {
    if (id == null) return;
    if (!this.usedIDs.has(guild)){
      return;
    }
    return this.usedIDs.get(guild)!.get(id)
  }

  set(id: number, guild: number, elem: any){
    if (!this.usedIDs.has(guild)){
      this.usedIDs.set(guild, new Map<number, any>())
    }
    this.usedIDs.get(guild)!.set(id, elem)
  }

  clear() {
    this.usedIDs.clear()
  }

  includeIDs(bd: Board) {
    for (let action of bd.actions) {
      this.set(action.id, bd.guild, action)
      for (let input of action.inputs) {
        this.set(input.id, bd.guild, input)
      }
      for (let output of action.outputs) {
        this.set(output.id, bd.guild, output)
      }
      for (let event of action.events) {
        this.set(event.id, bd.guild, event)
      }
      this.set(action.inputEvent.id, bd.guild, action.inputEvent)
    }
    for (let variable of bd.varInstances) {
      this.set(variable.id, bd.guild, variable)
      this.set(variable.input.id, bd.guild, variable.input)
      this.set(variable.output.id, bd.guild, variable.output)
    }
    for (let variable of bd.variables) {
      this.set(variable.id, bd.guild, variable)
    }
    for (let transition of bd.transitions) {
      this.set(transition.id, bd.guild, transition)
    }
    for (let gEvent of bd.globalEvents) {
      this.set(gEvent.id, bd.guild, gEvent)
      this.set(gEvent.output.id, bd.guild, gEvent.output)
      this.set(gEvent.eventOutput.id, bd.guild, gEvent.eventOutput)
    }
    for (let pipe of bd.pipelines) {
      this.set(pipe.id, bd.guild, pipe)
      if (pipe.point) {
        this.set(pipe.point.id, bd.guild, pipe.point)
      }
      if (pipe.eventPoint) {
        this.set(pipe.eventPoint.id, bd.guild, pipe.eventPoint)
      }
    }
  }

  delete(id: number) {
    this.usedIDs.delete(id)
  }
}

export class BoardManager {
  constructor () {
    this.idMan = new IDManager();
    this.boards = new Map<string, Board>();
    this.undoBuffer = []
    this.redoBuffer = []
  }
  
  idMan: IDManager;

  boards: Map<string, Board>
  boardList: string[];
  activeBoard: Board;
  activeActionName: string;
  undoBuffer: string[];
  redoBuffer: string[];

  getActive(): any {
    return this.activeBoard
  }

  updateVarInstanceRefs(inst: number) {
    const val = this.activeBoard.variables.find((elem) => (elem.id == inst))
    if (!val) return;
    val.references--;
    if (val.references == 0) {
      this.activeBoard.variables.splice(this.activeBoard.variables.indexOf(val), 1)
    }
  }

  createAction(templ: Action, mouse: MouseData, guild: number) {
    const getNewInputs = (templInputs: ValueInput[] | EventInput[], tp: string) => {
      var lst: any[] = [];
      for (let templInput of templInputs) {
        if (tp == "value") {
          var newVal: ValueInput;
          newVal = new ValueInput(0, templInput.name, (templInput as ValueInput).valueType, templInput.nature);
          newVal.comboValues = (templInput as ValueInput).comboValues
          newVal.preview = (templInput as ValueInput).preview
          this.idMan.getID(newVal, guild)
          lst.push(newVal)
        }
        else {
          var newEv: EventInput;
          newEv = new EventInput(0, templInput.name, templInput.nature);
          this.idMan.getID(newEv, guild)
          lst.push(newEv)
        }
      }
      return lst;
    }
    const newAct = new Action(
      0,
      templ.type,
      getNewInputs(templ.inputs, "value"),
      getNewInputs(templ.outputs, "value"),
      getNewInputs(templ.events, "event"),
      getNewInputs([templ.inputEvent], "event")[0]
    )
    this.idMan.getID(newAct, guild)
    this.activeBoard.actions.push(newAct)
    newAct.cdkPos = {
      x: mouse.offset.x - 300,
      y: mouse.offset.y - 70
    }
  }

  createVariable(vr: Variable, vrElem: VarElement, mouse: MouseData, guild: number) {
    const prevVar = vrElem.constant ? undefined : this.activeBoard.variables.find((elem) => (vrElem.name == elem.name))
    this.idMan.getID(vr, guild)
    this.idMan.getID(vr.input, guild)
    this.idMan.getID(vr.output, guild)
    if (prevVar) {
      prevVar.references++;
      vr.varAttr = prevVar.id
    }
    else {
      this.idMan.getID(vrElem, guild)
      this.activeBoard.variables.push(vrElem)
      vrElem.references++;
      vr.varAttr = vrElem.id
    }
    this.activeBoard.varInstances.push(vr)
    vr.cdkPos = {
      x: mouse.offset.x - 300,
      y: mouse.offset.y - 70
    }
  }

  createGlobalEvent(ge: GlobalEvent, mouse: MouseData, guild: number) {
    this.idMan.getID(ge, guild)
    this.idMan.getID(ge.output, guild)
    this.idMan.getID(ge.eventOutput, guild)
    this.activeBoard.globalEvents.push(ge)
    ge.cdkPos = {
      x: mouse.offset.x - 300,
      y: mouse.offset.y - 70
    }
  }

  createPipeline(ge: Pipeline, mouse: MouseData, guild: number) {
    this.idMan.getID(ge, guild)
    if (ge.type == "Event Input" || ge.type == "Event Output") {
      if (ge.type == "Event Input") {
        this.activeBoard.hasEvInput = true
      }
      this.idMan.getID(ge.eventPoint!, guild)
    }
    else {
      this.idMan.getID(ge.point!, guild)
    }
    this.activeBoard.pipelines.push(ge)
    ge.cdkPos = {
      x: mouse.offset.x - 300,
      y: mouse.offset.y - 70
    }
  }

  addTransition(data: Transition, guild: number) {
    this.idMan.getID(data, guild)
    this.activeBoard.transitions.push(data)
    const orig = this.idMan.get(data.origin[1], guild)
    if (orig) orig.transitionNumber++;
    const dest = this.idMan.get(data.destination[1], guild)
    if (dest) dest.transitionNumber++;
  }

  private deleteTransitionPresence(data: Transition, guild: number) {
    const orig = this.idMan.get(data.origin[1], guild)
    if (orig){
      orig.transitionNumber--;
      const origNode = this.idMan.get(data.origin[0], guild)
      if (orig.transitionNumber == 0 && origNode && origNode instanceof Variable){
        var varElem = this.idMan.get(origNode.varAttr, guild)
        origNode.comboTag = null
        varElem.possibleValues = null
      }
    }
    const dest = this.idMan.get(data.destination[1], guild)
    if (dest){
      dest.transitionNumber--;
      if (dest.transitionNumber == 0) {
        dest.fromVariable = false;
      }
    }
    this.idMan.delete(data.id)
  }

  removeTransition(guild: number, data: Transition | null = null) {
    let idx: number;
    if (!data) {
      this.cancelBufferUpdate()
      idx = this.activeBoard.transitions.length - 1
    }
    else {
      idx = this.activeBoard.transitions.indexOf(data)
    }
    const elem = this.activeBoard.transitions.splice(idx, 1)[0]
    this.deleteTransitionPresence(elem, guild)
  }

  cleanTransitions(node: number, guild: number, data: ValueInput | EventInput | null = null) {
    let check: { (trans: Transition): boolean; };
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
        this.deleteTransitionPresence(trans, guild)
        return false;
      }
      return true;
    })
  }

  deleteVar(node: Variable, spl: boolean){
    this.idMan.delete(node.input.id)
    this.updateVarInstanceRefs(node.varAttr)
    if (spl)
      this.activeBoard.varInstances.splice(this.activeBoard.varInstances.indexOf(node), 1)
  }

  deleteAct(node: Action, spl: boolean){
    node.inputs.forEach((input) => { this.idMan.delete(input.id) })
    node.outputs.forEach((input) => { this.idMan.delete(input.id) })
    node.events.forEach((input) => { this.idMan.delete(input.id) })
    this.idMan.delete(node.inputEvent.id)
    if (spl)
      this.activeBoard.actions.splice(this.activeBoard.actions.indexOf(node), 1)
  }

  deleteGEv(node: GlobalEvent, spl: boolean) {
    this.idMan.delete(node.output.id)
    this.idMan.delete(node.eventOutput.id)
    if (spl)
      this.activeBoard.globalEvents.splice(this.activeBoard.globalEvents.indexOf(node), 1)
  }

  deletePipe(node: Pipeline, spl: boolean) {
    if (node.point) {
      this.idMan.delete(node.point.id)
    }
    if (node.eventPoint) {
      this.idMan.delete(node.eventPoint.id)
    }
    if (node.type == "Event Input") {
      this.activeBoard.hasEvInput = false;
    }
    if (spl)
      this.activeBoard.pipelines.splice(this.activeBoard.pipelines.indexOf(node), 1)
  }

  changeBoard(loadBoard: string, isNew: boolean, guild: number) {
    if (isNew) {
      this.boards.set(loadBoard, new Board(loadBoard, guild, [], [], [], [], [], []))
      this.boardList[this.boardList.length - 1] = loadBoard
      this.boardList.push("...")
    }
    this.activeBoard = this.boards.get(loadBoard)!
    this.activeActionName = this.activeBoard.name.replace(new RegExp(" ", 'g'), "")
  }

  clearBoard(name: string) {
    this.emptyBuffer()
    const bd = this.getBoard(name)
    let elemProcess = (iter: any[], lst: any[]) => {
      for (let elem of lst){
        iter.splice(iter.indexOf(elem), 1)
      }
    }
    const elems: [Action[], Variable[], Pipeline[], GlobalEvent[]] = [[], [], [], []]
    for (let act of bd.actions){
      this.deleteAct(act, false)
      elems[0].push(act)
    }
    for (let act of bd.varInstances){
      this.deleteVar(act, false)
      elems[1].push(act)
    }
    for (let act of bd.pipelines){
      this.deletePipe(act, true)
      elems[2].push(act)
    }
    for (let act of bd.globalEvents){
      this.deleteGEv(act, false)
      elems[3].push(act)
    }
    elemProcess(bd.actions, elems[0])
    elemProcess(bd.varInstances, elems[1])
    elemProcess(bd.pipelines, elems[2])
    elemProcess(bd.globalEvents, elems[3])

    bd.variables = []
    bd.transitions = []
  }

  changeVarElems(oldName: string, newName: string, guild: number) {
    const prevVar = this.activeBoard.variables.find((elem) => (oldName == elem.name))!
    this.updateVarInstanceRefs(prevVar.id)
    const newVar = this.activeBoard.variables.find((elem) => (newName == elem.name))!
    if (newVar) {
      newVar.references++;
      return newVar
    }
    const newVInst = new VarElement(newName, prevVar.valueType, prevVar.initialValue)
    this.idMan.getID(newVInst, guild)
    this.activeBoard.variables.push(newVInst)
    newVInst.references++;
    return newVInst
  }

  insertBoards(newBoards: Board[]) {
    this.idMan.clear()
    this.boards.clear()
    newBoards.forEach((bd) => {
      this.boards.set(bd.name, bd)
      this.idMan.includeIDs(bd)
    })
    this.boardList = Array.from(this.boards.keys())
    this.boardList.push("...")
    this.activeBoard = this.boards.get("Main")!
    this.activeActionName = "Main"
  }

  getBoard(name: string): any {
    return this.boards.get(name)
  }

  setBoard(name: string, response: Board) {
    this.clearBoard(name)
    this.idMan.includeIDs(response)
    this.boards.set(name, response)
  }

  updateBuffer() {
    this.undoBuffer.push(JSON.stringify(this.activeBoard))
    if (this.undoBuffer.length > 10){
      this.undoBuffer.splice(0, 1)
    }
    this.redoBuffer = []
  }

  cancelBufferUpdate() {
    this.undoBuffer.splice(this.undoBuffer.length - 1, 1)
  }

  emptyBuffer() {
    this.undoBuffer = []
    this.redoBuffer = []
  }

  undo() {
    const undo = this.undoBuffer.pop()
    if (!undo){
      return
    }
    this.redoBuffer.push(JSON.stringify(this.activeBoard))
    this.activeBoard = JSON.parse(undo)
    this.idMan.includeIDs(this.activeBoard)
  }

  redo() {
    const redo = this.redoBuffer.pop()
    if (!redo){
      return
    }
    this.undoBuffer.push(JSON.stringify(this.activeBoard))
    this.activeBoard = JSON.parse(redo)
    this.idMan.includeIDs(this.activeBoard)
  }
}
