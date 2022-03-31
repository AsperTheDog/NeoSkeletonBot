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

  usedIDs: Map<number, any>;

  getID(elem: {id: number}) {
    let count = 0;
    while (this.usedIDs.has(count)) {
      count++;
    }
    elem.id = count;
    this.usedIDs.set(count, elem)
  }

  get(id: number | null) {
    if (id == null) return;
    return this.usedIDs.get(id)
  }

  clear() {
    this.usedIDs.clear()
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

  delete(id: number) {
    this.usedIDs.delete(id)
  }
}

export class BoardManager {
  constructor () {
    this.idMan = new IDManager();
    this.boards = new Map<string, Board>();
  }
  
  idMan: IDManager;

  boards: Map<string, Board>
  boardList: string[];
  activeBoard: Board;

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

  createAction(templ: Action, mouse: MouseData) {
    const getNewInputs = (templInputs: ValueInput[] | EventInput[], tp: string) => {
      var lst: any[] = [];
      for (let templInput of templInputs) {
        if (tp == "value") {
          var newVal: ValueInput;
          newVal = new ValueInput(0, templInput.name, (templInput as ValueInput).valueType, templInput.nature);
          newVal.comboValues = (templInput as ValueInput).comboValues
          this.idMan.getID(newVal)
          lst.push(newVal)
        }
        else {
          var newEv: EventInput;
          newEv = new EventInput(0, templInput.name, templInput.nature);
          this.idMan.getID(newEv)
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
    this.idMan.getID(newAct)
    this.activeBoard.actions.push(newAct)
    newAct.cdkPos = {
      x: mouse.offset.x - 300,
      y: mouse.offset.y - 70
    }
  }

  createVariable(vr: Variable, vrElem: VarElement, mouse: MouseData) {
    const prevVar = vrElem.constant ? undefined : this.activeBoard.variables.find((elem) => (vrElem.name == elem.name))
    this.idMan.getID(vr)
    this.idMan.getID(vr.input)
    this.idMan.getID(vr.output)
    if (prevVar) {
      prevVar.references++;
      vr.varAttr = prevVar.id
    }
    else {
      this.idMan.getID(vrElem)
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

  createGlobalEvent(ge: GlobalEvent, mouse: MouseData) {
    this.idMan.getID(ge)
    this.idMan.getID(ge.output)
    this.idMan.getID(ge.eventOutput)
    this.activeBoard.globalEvents.push(ge)
    ge.cdkPos = {
      x: mouse.offset.x - 300,
      y: mouse.offset.y - 70
    }
  }

  createPipeline(ge: Pipeline, mouse: MouseData) {
    this.idMan.getID(ge)
    if (ge.type == "Event Input" || ge.type == "Event Output") {
      if (ge.type == "Event Input") {
        this.activeBoard.hasEvInput = true
      }
      this.idMan.getID(ge.eventPoint!)
    }
    else {
      this.idMan.getID(ge.point!)
    }
    this.activeBoard.pipelines.push(ge)
    ge.cdkPos = {
      x: mouse.offset.x - 300,
      y: mouse.offset.y - 70
    }
  }

  addTransition(data: Transition) {
    this.idMan.getID(data)
    this.activeBoard.transitions.push(data)
    const orig = this.idMan.get(data.origin[1])
    if (orig) orig.transitionNumber++;
    const dest = this.idMan.get(data.destination[1])
    if (dest) dest.transitionNumber++;
  }

  private deleteTransitionPresence(data: Transition) {
    const orig = this.idMan.get(data.origin[1])
    if (orig) orig.transitionNumber--;
    const dest = this.idMan.get(data.destination[1])
    if (dest){
      dest.transitionNumber--;
      if (dest.transitionNumber == 0) {
        dest.fromVariable = false;
      }
    }
    this.idMan.delete(data.id)
  }

  removeTransition(data: Transition | null = null) {
    let idx: number;
    if (!data) {
      idx = this.activeBoard.transitions.length - 1
    }
    else {
      idx = this.activeBoard.transitions.indexOf(data)
    }
    const elem = this.activeBoard.transitions.splice(idx, 1)[0]
    this.deleteTransitionPresence(elem)
  }

  cleanTransitions(node: number, data: ValueInput | EventInput | null = null) {
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
        this.deleteTransitionPresence(trans)
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
  }

  clearBoard(name: string) {
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

  changeVarElems(oldName: string, newName: string) {
    const prevVar = this.activeBoard.variables.find((elem) => (oldName == elem.name))!
    this.updateVarInstanceRefs(prevVar.id)
    const newVar = this.activeBoard.variables.find((elem) => (newName == elem.name))!
    if (newVar) {
      newVar.references++;
      return newVar
    }
    const newVInst = new VarElement(newName, prevVar.valueType, prevVar.initialValue)
    this.idMan.getID(newVInst)
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
  }

  getBoard(name: string): any {
    return this.boards.get(name)
  }

  setBoard(name: string, response: Board) {
    this.clearBoard(name)
    this.idMan.includeIDs(response)
    this.boards.set(name, response)
  }
}
