import { Component, Input, OnInit } from '@angular/core';
import { MainControllerService } from 'src/app/services/main-controller.service';
import { EventInput, ValueInput } from 'src/app/utils/dataTypes/Value';
import { ValueType } from 'src/app/utils/dataTypes/ValueType';

@Component({
  selector: 'app-phantomValueNode',
  templateUrl: 'phantomValueNode.html',
  styleUrls: ['phantomValueNode.css']
})
export class PhantomValueNode implements OnInit {
  constructor(public mainController: MainControllerService) { }

  @Input() valData: ValueInput;

  hoveringStyle = 'black';
  isHovering: boolean = false;
  valueType: ValueType;

  ngOnInit(): void {
    this.updateType()
  }

  updateType() {
    this.valueType = this.mainController.typeValMan.getType(this.valData.valueType)
  }

  public documentEnter(): void {
    this.isHovering = true;
  }

  public documentLeave(): void {
    this.isHovering = false;
  }
}