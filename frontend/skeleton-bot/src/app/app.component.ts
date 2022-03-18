import { AfterViewInit, Component, ElementRef, HostListener, OnInit, QueryList, ViewChild, ViewChildren } from '@angular/core';
import { DragShieldService } from './services/dragshield.service';
import { MainControllerService } from './services/main-controller.service';
import { Variable } from './utils/Variable';
import { PhantomVariableNode } from './views/VariableNode/phantom/phantomVariableNode';
import { trigger, style, animate, transition } from '@angular/animations';
import { EventInput, ValueInput } from './utils/Value';
import { ActionNode } from './views/ActionNode/actionNode';
import { VariableNode } from './views/VariableNode/variableNode';
import { GEventNode } from './views/GEventNode/GEventNode';
import { GlobalEvent } from './utils/GlobalEvent';
import { ValueType } from './utils/ValueType';
import { Pipeline } from './utils/Pipeline';
import { PhantomPipelineNode } from './views/PipelineNode/phantom/phantomPipelineNode';
import { VarElement } from './utils/VarElement';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css',],
  animations: [
    trigger(
      'inAnimation',
      [
        transition(
          ':enter',
          [
            style({ height: 100, opacity: 0 }),
            animate('0.5s ease-out',
              style({ height: 100, opacity: 1 }))
          ]
        )
      ]
    ),
    trigger(
      'outAnimation',
      [
        transition(
          ':leave',
          [
            style({ height: 100, opacity: 1 }),
            animate('0.1s ease-in',
              style({ height: 100, opacity: 0 }))
          ]
        )
      ]
    )
  ]
})
export class AppComponent implements OnInit, AfterViewInit {
  constructor(public dragShield: DragShieldService,
    public mainController: MainControllerService,
    private route: ActivatedRoute) {
    this.dragShield.canvas = this;
    this.requestedBoard = "Main";
    this.globalEvents = this.mainController.globalEventList
  }

  @ViewChildren("nodeRef") nodeRefs: QueryList<ActionNode | VariableNode | GEventNode>;
  @ViewChild("board") boardRef: ElementRef;
  @ViewChild("sideBar") sideBar: ElementRef;
  @ViewChild("phantomVar") phantomVar: PhantomVariableNode;
  @ViewChild("phantomPipe") phantomPipe: PhantomPipelineNode;

  requestedBoard: string;
  globalEvents: string[];

  origSize = [20000, 20000]
  dragPos = { x: 0, y: 0 };
  scW = window.innerWidth
  scH = window.innerHeight
  dragDisabled = false
  dragged = false
  draggingNode: boolean = false;
  zooming = false;

  Math = Math
  window = window

  varTypeInput: string = "0";
  varType: ValueType = this.mainController.getType(0);
  varIsConstant: boolean = false;
  varName: string = "";
  varInitialValue: string = "";
  evTypeInput: string = "0";
  evType: string = "init";
  evName: string = "";
  showCaseVar: Variable = new Variable(-1,
    new ValueInput(-1, "set value", -1, "in"),
    new ValueInput(-1, "get value", -1, "out")
  );
  showCaseVarElem: VarElement = new VarElement("", 0, "0")
  showCaseEvent: GlobalEvent = new GlobalEvent("",
    new EventInput(-1, "event output", "out"),
    new ValueInput(-1, "value output", 3, "out")
  );

  showCasePipeline: Pipeline = new Pipeline("", "", null, null);

  @HostListener('document:mousemove', ['$event'])
  public documentMouseMove(event: MouseEvent): void {
    if (this.boardRef && this.boardRef.nativeElement) {
      this.mainController.mouse.offset = {
        x: event.x - this.boardRef.nativeElement.getBoundingClientRect().x,
        y: event.y - this.boardRef.nativeElement.getBoundingClientRect().y
      }
    }
  }

  @HostListener('document:mouseup', ['$event'])
  public documentMouseUp(event: MouseEvent): void {
    if (this.mainController.transStartInput) {
      this.mainController.transStartInput.finishTransition();
    }
  }

  ngOnInit(): void {
    this.route.queryParams
      .subscribe(params => {
        this.mainController.usrCode = params['usrCode'];
        if (this.mainController.usrCode){
          this.mainController.loaded = false
          this.mainController.checkCreds()
        }
      }
    );
    this.updateShowcaseVariable()
    this.updateShowcaseEvent()
    this.dragPos = {
      x: -this.origSize[0] / 2 + this.scW / 2,
      y: -this.origSize[0] / 2 + this.scH / 2
    }
  }

  ngAfterViewInit(): void {
    this.mainController.boardCoords = this.getBoardCoords();
    this.nodeRefs.forEach((node) => { node.updateCoords() })
    this.mainController.spawnLocation = {
      x: this.sideBar.nativeElement.getBoundingClientRect().x,
      y: this.sideBar.nativeElement.getBoundingClientRect().y
    }
  }

  updateDragPos() {
    this.mainController.boardCoords = this.getBoardCoords();
  }

  disableDrag() {
    this.dragDisabled = true;
  }

  enableDrag() {
    this.dragDisabled = false;
  }

  getBoardCoords() {
    return {
      x: this.boardRef.nativeElement.getBoundingClientRect().x,
      y: this.boardRef.nativeElement.getBoundingClientRect().y
    }
  }

  dragEvent() {
    if (!this.dragged) {
      this.dragged = true
    }
  }

  updateShowcaseVariable() {
    const varTypeID = parseInt(this.varTypeInput)
    this.varType = this.mainController.getType(varTypeID)
    this.showCaseVar.input.valueType = this.varType.varInOut[0];
    this.showCaseVar.output.valueType = this.varType.varInOut[1];
    this.showCaseVarElem.valueType = varTypeID;
    this.showCaseVarElem.initialValue = this.varInitialValue;
    this.showCaseVarElem.constant = this.varIsConstant;
    this.showCaseVarElem.name = this.varIsConstant ? "" : this.varName;
    if (this.phantomVar) {
      this.phantomVar.updateType()
    }
  }

  updateShowcaseEvent() {
    this.showCaseEvent.name = this.evType
  }

  updateShowcasePipeline() {
    this.showCasePipeline.type = this.evType
    this.showCasePipeline.name = this.evName
    if (this.evType == 'actionValueInput' || this.evType == 'actionValueOutput') {
      if (!this.showCasePipeline.point) {
        this.showCasePipeline.point = new ValueInput(-1, this.evName, parseInt(this.evTypeInput), this.evType == 'actionValueInput' ? "out" : "in")
      }
      else {
        this.showCasePipeline.point.name = this.evName
        this.showCasePipeline.point.valueType = parseInt(this.evTypeInput)
        this.showCasePipeline.point.nature = this.evType == 'actionValueInput' ? "out" : "in"
      }
      this.showCasePipeline.eventPoint = null
    }
    else {
      if (!this.showCasePipeline.eventPoint) {
        this.showCasePipeline.eventPoint = new EventInput(-1, this.evName, this.evType == 'actionEventInput' ? "out" : "in")
      }
      else {
        this.showCasePipeline.eventPoint.name = this.evName
        this.showCasePipeline.eventPoint.nature = this.evType == 'actionEventInput' ? "out" : "in"
      }
      this.showCasePipeline.point = null
    }
    if (this.phantomPipe) {
      this.phantomPipe.updateType()
    }
  }

  resetShowCase(type: string) {
    if (type == "var") {
      this.showCaseVar = new Variable(-1,
        new ValueInput(-1, "set value", -1, "in"),
        new ValueInput(-1, "get value", -1, "out")
      );
      this.showCaseVarElem = new VarElement("", 0, "0")
      this.updateShowcaseVariable()
    }
    if (type == "event") {
      this.showCaseEvent = new GlobalEvent("",
        new EventInput(-1, "event output", "out"),
        new ValueInput(-1, "value output", 3, "out")
      );
      this.updateShowcaseEvent()
    }
    if (type == "pipeline") {
      this.showCasePipeline = new Pipeline("", "", null, null);
      this.updateShowcasePipeline()
    }
  }

  changeBoard() {
    if (this.requestedBoard != "Main") {
      this.varIsConstant = true
      this.globalEvents = this.mainController.customActionEvents
      this.evType = "actionValueInput"
      this.updateShowcasePipeline()
    }
    else {
      this.varIsConstant = false
      this.evType = "init"
      this.globalEvents = this.mainController.globalEventList
      this.updateShowcaseEvent()
    }
    this.evType = this.globalEvents[0]
    this.updateShowcaseEvent()
    this.updateShowcaseVariable()
    if (this.requestedBoard != "...") {
      this.mainController.changeBoard(this.requestedBoard, false)
    }
    else {
      var newName = prompt("Insert new schematic name")
      if (!newName) return;
      this.mainController.changeBoard(newName, true)
      this.requestedBoard = newName
    }
  }

  deleteBoard() {
    this.requestedBoard = "Main"
    this.mainController.deleteBoard()
  }

  invite() {
    window.open("https://discord.com/api/oauth2/authorize?client_id=682744116143980699&permissions=8&scope=bot", '_blank')!.focus();
  }
}



