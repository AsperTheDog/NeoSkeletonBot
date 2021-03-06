import { AfterViewInit, Component, ElementRef, HostListener, OnInit, QueryList, ViewChild, ViewChildren } from '@angular/core';
import { DragShieldService } from './services/dragshield.service';
import { MainControllerService } from './services/main-controller.service';
import { Variable } from './utils/dataTypes/Variable';
import { PhantomVariableNode } from './views/VariableNode/phantom/phantomVariableNode';
import { trigger, style, animate, transition } from '@angular/animations';
import { EventInput, ValueInput } from './utils/dataTypes/Value';
import { ActionNode } from './views/ActionNode/actionNode';
import { VariableNode } from './views/VariableNode/variableNode';
import { GEventNode } from './views/GEventNode/GEventNode';
import { GlobalEvent } from './utils/dataTypes/GlobalEvent';
import { ValueType } from './utils/dataTypes/ValueType';
import { Pipeline } from './utils/dataTypes/Pipeline';
import { PhantomPipelineNode } from './views/PipelineNode/phantom/phantomPipelineNode';
import { VarElement } from './utils/dataTypes/VarElement';
import { ActivatedRoute } from '@angular/router';
import { PipelineNode } from './views/PipelineNode/PipelineNode';
import { Arrow } from './views/Transition/arrow';

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
  }

  @ViewChildren("nodeRef") nodeRefs: QueryList<ActionNode | VariableNode | GEventNode | PipelineNode>;
  @ViewChildren("arrowRef") arrowRefs: QueryList<Arrow>;
  @ViewChild("board") boardRef: ElementRef;
  @ViewChild("sideBar") sideBar: ElementRef;
  @ViewChild("phantomVar") phantomVar: PhantomVariableNode;
  @ViewChild("phantomPipe") phantomPipe: PhantomPipelineNode;

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
  varType: ValueType = this.mainController.typeValMan.getType(0);
  varIsConstant: boolean = false;
  varName: string = "";
  varInitialValue: string = "";
  evTypeInput: string = "0";
  evType: string = "on message received";
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
      this.mainController.transStartInput = null
    }
  }

  @HostListener('window:keydown',['$event'])
  onKeyPress($event: KeyboardEvent) {
    if(($event.ctrlKey || $event.metaKey) && $event.key == 'z'){
      this.mainController.boardMan.undo()
      this.nodeRefs.forEach(c => c.reload());
      this.arrowRefs.forEach(c => c.reload());
    }
    if(($event.ctrlKey || $event.metaKey) && $event.key == 'y'){
      this.mainController.boardMan.redo()
      this.nodeRefs.forEach(c => c.reload());
      this.arrowRefs.forEach(c => c.reload());
    }
  }

  ngOnInit(): void {
    this.route.queryParams
      .subscribe(params => {
        this.mainController.sessionMan.setCode(params['usrCode'])
        if (this.mainController.sessionMan.getCode()){
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
    this.varType = this.mainController.typeValMan.getType(varTypeID)
    this.showCaseVar.input.valueType = this.varType.varInOut[0];
    this.showCaseVar.output.valueType = this.varType.varInOut[1];
    if (this.showCaseVarElem.valueType != varTypeID){
      this.varInitialValue = ""
    }
    this.showCaseVarElem.valueType = varTypeID;
    this.showCaseVarElem.initialValue = this.varInitialValue;
    this.showCaseVarElem.constant = this.varIsConstant || this.varType.mustBeConst;
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
    if (this.evType == 'Value Input' || this.evType == 'Value Output') {
      if (!this.showCasePipeline.point) {
        this.showCasePipeline.point = new ValueInput(-1, this.evName, parseInt(this.evTypeInput), this.evType == 'Value Input' ? "out" : "in")
      }
      else {
        this.showCasePipeline.point.name = this.evName
        this.showCasePipeline.point.valueType = parseInt(this.evTypeInput)
        this.showCasePipeline.point.nature = this.evType == 'Value Input' ? "out" : "in"
      }
      this.showCasePipeline.eventPoint = null
    }
    else {
      if (!this.showCasePipeline.eventPoint) {
        this.showCasePipeline.eventPoint = new EventInput(-1, this.evName, this.evType == 'Event Input' ? "out" : "in")
      }
      else {
        this.showCasePipeline.eventPoint.name = this.evName
        this.showCasePipeline.eventPoint.nature = this.evType == 'Event Input' ? "out" : "in"
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
    if (this.mainController.requestedBoard != "Main") {
      this.varIsConstant = true
      this.evType = "Value Input"
      this.updateShowcasePipeline()
    }
    else {
      this.varIsConstant = false
      this.evType = "init"
      this.updateShowcaseEvent()
    }
    this.updateShowcaseEvent()
    this.updateShowcaseVariable()
    if (this.mainController.requestedBoard != "...") {
      this.mainController.changeBoard(this.mainController.requestedBoard, false)
    }
    else {
      var newName = prompt("Insert new schematic name")
      if (!newName){
        this.mainController.requestedBoard = this.mainController.boardMan.getActive().name
        return;
      }
      this.mainController.changeBoard(newName, true)
    }
  }

  invite() {
    window.open(this.mainController.httpService.inviteRef, '_blank')!.focus();
  }

  save() {
    this.mainController.saveBoard()!.subscribe((data) => {
      this.mainController.saveProcess(data)
    })
  }
}



