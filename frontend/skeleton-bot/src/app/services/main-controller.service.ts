import { Injectable } from '@angular/core';
import valueTypes from '../../assets/json/types.json';
import { MouseData } from '../utils/dataTypes/Mouse';
import { Action } from '../utils/dataTypes/Action';
import { Variable } from '../utils/dataTypes/Variable';
import { GlobalEvent } from '../utils/dataTypes/GlobalEvent';
import { ValueNode } from '../views/input/value/valueNode';
import { EventNode } from '../views/input/event/eventNode';
import { Pipeline } from '../utils/dataTypes/Pipeline';
import { VarElement } from '../utils/dataTypes/VarElement';
import { SessionManager, TemplateManager, TypeValueManager } from '../utils/StaticDataManager';
import { BoardManager } from '../utils/BoardManager';
import { httpService } from './httpService.service';

@Injectable({
  providedIn: 'root'
})
export class MainControllerService {
  constructor(public httpService: httpService) {

    this.templateMan = new TemplateManager();
    this.boardMan = new BoardManager();
    this.typeValMan = new TypeValueManager();
    this.sessionMan = new SessionManager();

    this.typeValMan.setValueTypes(valueTypes.types)

    this.hoveringDelete = false;
    this.spawnLocation = { x: 0, y: 0 }
    this.mouse = new MouseData()

    this.getStaticData()

    this.manageInfo("This is the log, info about your actions will be shown here", false)
  }

  templateMan: TemplateManager;
  boardMan: BoardManager;
  typeValMan: TypeValueManager;
  sessionMan: SessionManager;

  hoveringDelete: boolean;

  spawnLocation: { x: number, y: number }
  boardCoords: { x: number, y: number }

  transStartInput: ValueNode | EventNode | null = null;
  hovering: ValueNode | EventNode | null = null;
  mouse: MouseData;

  infoDisplayText: [string, boolean][] = [
    ["", false], 
    ["", false], 
    ["", false]
  ];

  loaded = true;
  cancelledChange = false;
  requestedBoard = "Main";

  promptData: string = "";
  promptDateData: Date = new Date();
  showModal: boolean = false;
  selectedVar: VarElement;

  showInfoModalType: string = "";
  infoModalActData: Action;

  manageInfo(newText: string, isError: boolean) {
    var currentdate = new Date(); 
  var datetime = (currentdate.getHours() < 10 ? "0" + currentdate.getHours() : currentdate.getHours()) + ":" + 
                 (currentdate.getMinutes() < 10 ? "0" + currentdate.getMinutes() : currentdate.getMinutes()) + ":" +
                 (currentdate.getSeconds() < 10 ? "0" + currentdate.getSeconds() : currentdate.getSeconds());
    this.infoDisplayText.shift()
    this.infoDisplayText.push(["[" + datetime + "] " + newText, isError])
  }

  saveProcess(data: {status: boolean}) {
    if (!this.sessionMan.sessionIsValid()) return;
    let saved = false;
    if (!data.status){
      this.manageInfo("Parse error, could not save board", true)
      saved = false;
    }
    else {
      this.manageInfo("Saved changes", false)
      saved = true;
      
      this.httpService.getActions(this.sessionMan.getGuild()!).subscribe(
        (response) => {
          if (response.length == 0){
            this.logout(false)
            return;
          }
          this.templateMan.insertActions(response)
        },
        (error) => {
          console.log(error);
        }
      )
    }
    return saved
  }

  saveBoard() {
    if (!this.sessionMan.sessionIsValid()) return;
    return this.httpService.saveBoard(this.boardMan.getActive())
  }

  deleteElem(node: Action | Variable | GlobalEvent | Pipeline, type: string, spl:boolean = true) {
    this.boardMan.cleanTransitions(node.id, this.sessionMan.getGuild()!)
    if (type == 'var') {
      this.boardMan.deleteVar(node as Variable, spl)
      this.manageInfo("Deleted variable node", false)
    }
    else if (type == 'action') {
      this.boardMan.deleteAct(node as Action, spl)
      this.manageInfo("Deleted action node", false)
    }
    else if (type == 'event') {
      this.boardMan.deleteGEv(node as GlobalEvent, spl)
      this.manageInfo("Deleted event node", false)
    }
    else if (type == 'pipeline') {
      this.boardMan.deletePipe(node as Pipeline, spl)
      this.manageInfo("Deleted pipeline node", false)
    }
  }

  checkIfDelete(node: Action | Variable | GlobalEvent | Pipeline, type: string) {
    if (!this.hoveringDelete) return;
    this.deleteElem(node, type)
  }

  getNewAction(templateID: number) {
    this.boardMan.updateBuffer()
    const templ = this.templateMan.getTemplate(templateID)
    this.boardMan.createAction(templ, this.mouse, this.sessionMan.getGuild()!)
    this.manageInfo("Created new Action Node of type '" + templ.type + "'", false)
  }

  getNewVariable(vr: Variable, vrElem: VarElement) {
    this.boardMan.updateBuffer()
    this.boardMan.createVariable(vr, vrElem, this.mouse, this.sessionMan.getGuild()!)
    this.manageInfo("Created new Variable Node", false)
  }

  getNewGEvent(ge: GlobalEvent) {
    this.boardMan.updateBuffer()
    this.boardMan.createGlobalEvent(ge, this.mouse, this.sessionMan.getGuild()!)
    this.manageInfo("Created new Global Event Node '" + ge.name + "'", false)
  }

  getNewPipeline(ge: Pipeline) {
    this.boardMan.updateBuffer()
    this.boardMan.createPipeline(ge, this.mouse, this.sessionMan.getGuild()!)
    this.manageInfo("Created new Pipeline Node '" + ge.name + "'", false)
  }

  changeBoard = (loadBoard: string, isNew: boolean, savePrev=true) => {
    if (!this.sessionMan.sessionIsValid()) return;
    this.loaded = false;
    const active = this.boardMan.getActive().name
    if (!savePrev){
      this.boardMan.changeBoard(loadBoard, isNew, this.sessionMan.getGuild()!)
      this.requestedBoard = loadBoard
      this.manageInfo("Loaded new schematic " + active, false)
      this.loaded = true;
      return;
    }

    this.saveBoard()!.subscribe((data) => {
      const saved = this.saveProcess(data)
      if (!saved){
        const confr = confirm("The board could not be saved, do you want to undo changes?")
        if (!confr){
          this.requestedBoard = active
          this.loaded = true;
          return;
        }
        this.revertBoard(active)
      }
      this.boardMan.changeBoard(loadBoard, isNew, this.sessionMan.getGuild()!)
      this.requestedBoard = loadBoard
      this.manageInfo("Loaded new schematic " + loadBoard, false)
      this.loaded = true;
    })
  }

  clearBoard() {
    this.boardMan.updateBuffer()
    if (!this.sessionMan.sessionIsValid()) return;
    const conf = confirm("Are you sure you want to clear the board?")
    if (!conf) return;
    this.boardMan.clearBoard(this.boardMan.getActive().name)
  }

  checkCreds() {
    this.httpService.getCreds(this.sessionMan.getCode()).subscribe(
      (creds) => {
        this.httpService.putCookie('token', creds.token)
        this.sessionMan.insertCreds(creds)
        if (creds.usr.id){
          this.httpService.getGuilds().subscribe(
            (guilds) => {
              this.sessionMan.insertGuilds(guilds)

              this.httpService.getBoards(this.sessionMan.getGuild()!).subscribe(
                (boards) => {
                  this.boardMan.insertBoards(boards)

                  this.httpService.getActions(this.sessionMan.getGuild()!).subscribe(
                    (actions) => {
                      this.templateMan.insertActions(actions)
                      this.loaded = true;
                    },
                    (error) => {
                      console.log(error);
                    }
                  )
                },
                (error) => {console.log(error)}
              )
            },
            (error) => {console.log(error)}
          )
        }
        else{
          this.logout(false)
          this.loaded = true
        }
      },
      (error) => {console.log(error)}
    )
  }

  deleteBoard() {
    if (!this.sessionMan.sessionIsValid()) return;
    var confr = confirm("Are you sure you want to remove this board?")
    if (!confr) return;
    this.loaded = false
    this.httpService.deleteBoard(this.sessionMan.getGuild()!, this.boardMan.getActive().name).subscribe(
      (_) => {
        this.httpService.getBoards(this.sessionMan.getGuild()!).subscribe(
          (boards) => {
            this.boardMan.insertBoards(boards)

            this.httpService.getActions(this.sessionMan.getGuild()!).subscribe(
              (actions) => {
                this.templateMan.insertActions(actions)
                this.changeBoard('Main', false, false)
                this.loaded = true;
              },
              (error) => {
                console.log(error);
              }
            )
          },
          (error) => {console.log(error)}
        )
      },
      (error) => {console.log(error)}
    )
  }

  logout(doConf: boolean) {
    if (doConf){
      const conf = confirm("Are you sure you want to log out? Unsaved progress will be lost")
      if (!conf) return;
    }
    this.httpService.removeCookie()
    this.sessionMan.removeSession()
  }

  changeGuilds() {
    this.loaded = false
    this.httpService.getBoards(this.sessionMan.getGuild()!).subscribe(
      (boards) => {
        this.boardMan.insertBoards(boards)

        this.httpService.getActions(this.sessionMan.getGuild()!).subscribe(
          (actions) => {
            this.templateMan.insertActions(actions)
            this.loaded = true;
          },
          (error) => {
            console.log(error);
          }
        )
      },
      (error) => {console.log(error)}
    )
  }

  getStaticData() {
    this.httpService.getGlobalEvents().subscribe(
      (globalEvents) => {
        this.typeValMan.setGlobalEvents(globalEvents.events)
        this.typeValMan.setPipelineTypes(globalEvents.customActionEvents)
      },
      (error) => {console.log(error)}
    )
    this.httpService.getValueTypes().subscribe(
      (valueTypes) => {
        this.typeValMan.setValueTypes(valueTypes)
      },
      (error) => {console.log(error)}
    )
  }

  revertBoard(name: string) {
    if (!this.sessionMan.sessionIsValid()) return;
    this.httpService.getBoard(this.sessionMan.getGuild()!, name).subscribe(
      (response) => {
        this.boardMan.setBoard(name, response)
      },
      (error) => {
        console.log(error)
      }
    )
  }

  openPrompt(vr: VarElement) {
    this.selectedVar = vr;
    this.promptData = vr.initialValue;
    this.showModal = true;
  }

  updatePrompt() {
    this.selectedVar.initialValue = this.promptData
    this.closePrompt()
  }

  closePrompt() {
    this.showModal = false
  }

  updateInfoModal(act: Action){
    this.infoModalActData = act
    this.showInfoModalType = "action"
  }

  showInfoModalCustom(type: string){
    this.showInfoModalType = type
  }

  closeInfoModal() {
    this.showInfoModalType = ""
  }
}