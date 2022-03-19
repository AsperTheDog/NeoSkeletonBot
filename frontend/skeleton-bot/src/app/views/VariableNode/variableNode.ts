import { AfterViewInit, Component, ElementRef, Input, OnInit, ViewChild } from '@angular/core';
import { MainControllerService } from 'src/app/services/main-controller.service';
import { Variable } from 'src/app/utils/dataTypes/Variable';
import { DragShieldService } from 'src/app/services/dragshield.service';
import { CdkDragEnd, CdkDragMove, CdkDragStart } from '@angular/cdk/drag-drop';
import { ValueInput } from 'src/app/utils/dataTypes/Value';
import { ValueType } from 'src/app/utils/dataTypes/ValueType';
import { ValueNode } from '../input/value/valueNode';
import { VarElement } from 'src/app/utils/dataTypes/VarElement';

@Component({
  selector: 'app-variableNode',
  templateUrl: 'variableNode.html',
  styleUrls: ['variableNode.css']
})
export class VariableNode implements OnInit, AfterViewInit {
  constructor(
    public mainController: MainControllerService,
    public dragShield: DragShieldService,
    public elRef: ElementRef) {
    this.mainData = new Variable(-1,
      new ValueInput(-1, "set value", -1, "in"),
      new ValueInput(-1, "get value", -1, "out")
    );
  }

  @ViewChild("mainRef") mainRef: ElementRef;
  @ViewChild("inputRef") input: ValueNode;
  @ViewChild("outputRef") output: ValueNode;

  @Input() mainDataID: number;

  dragDisabled = false;
  position = { x: 0, y: 0 }
  mainData: Variable;
  valueType: ValueType;

  varAttr: VarElement;
  varName: string;

  ngOnInit(): void {
    this.mainData = this.mainController.boardMan.idMan.get(this.mainDataID)
    this.varAttr = this.mainController.boardMan.idMan.get(this.mainData.varAttr)
    this.valueType = this.mainController.typeValMan.getType(this.varAttr.valueType)
    this.mainData.input.valueType = this.valueType.varInOut[0]
    this.mainData.output.valueType = this.valueType.varInOut[1]
    this.position = this.mainData.cdkPos
    this.varName = this.varAttr.name
  }

  ngAfterViewInit(): void {
    this.input.parentNode = this
    this.input.updateInput()
    this.output.parentNode = this
    this.output.updateInput()
  }

  onDragStart() {
    this.dragShield.canvas.draggingNode = true;
  }

  onDragMove() {
    this.updateCoords()
  }

  disableDrag() {
    this.dragDisabled = true;
    this.dragShield.disableDrag();
  }

  enableDrag() {
    this.dragDisabled = false;
    this.dragShield.enableDrag();
  }

  updateCoords() {
    this.mainData.position = {
      x: this.mainRef.nativeElement.getBoundingClientRect().x - this.mainController.boardCoords.x,
      y: this.mainRef.nativeElement.getBoundingClientRect().y - this.mainController.boardCoords.y
    }
  }

  getVarCoords(event: CdkDragEnd) {
    this.dragShield.canvas.draggingNode = false
    this.mainData.cdkPos = event.source.getFreeDragPosition()
    this.mainController.checkIfDelete(this.mainData, "var")
  }

  checkVariableName() {
    if (this.varName == ""){
      this.varName = this.varAttr.name;
      return;
    }
    if (this.varAttr.name == this.varName) return;
    var newVar = this.mainController.boardMan.changeVarElems(this.varAttr.name, this.varName)
    this.mainData.varAttr = newVar.id
    this.varAttr = newVar
  }
}