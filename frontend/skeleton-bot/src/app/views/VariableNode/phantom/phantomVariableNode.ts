import { Component, Input, OnInit, ViewChild } from '@angular/core';
import { MainControllerService } from 'src/app/services/main-controller.service';
import { ValueType } from 'src/app/utils/ValueType';
import { VarElement } from 'src/app/utils/VarElement';
import { Variable } from 'src/app/utils/Variable';
import { PhantomValueNode } from '../../input/value/phantom/phantomValueNode';

@Component({
  selector: 'app-phantomVariableNode',
  templateUrl: 'phantomVariableNode.html',
  styleUrls: ['phantomVariableNode.css']
})
export class PhantomVariableNode implements OnInit{
  constructor(public mainController: MainControllerService) { }

  @Input() mainData: Variable;
  @Input() varElem: VarElement;

  @ViewChild("inputRef") input: PhantomValueNode;
  @ViewChild("outputRef") output: PhantomValueNode;
  
  valueType: ValueType
  position = {x: 0, y: 0}

  updateType  ()  {
    this.valueType = this.mainController.getType(this.varElem.valueType)
    this.input.updateType()
    this.output.updateType()
  }

  ngOnInit(): void {
    this.valueType = this.mainController.getType(this.varElem.valueType)
  }

  updatePosition  (pos: {x: number, y: number}) {
    this.position = pos;
  }
}