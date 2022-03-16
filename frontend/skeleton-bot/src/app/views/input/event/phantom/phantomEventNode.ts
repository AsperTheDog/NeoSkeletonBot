import { Component, Input } from '@angular/core';
import { EventInput, ValueInput } from 'src/app/utils/Value';

@Component({
  selector: 'app-phantomEventNode',
  templateUrl: 'phantomEventNode.html',
  styleUrls: ['phantomEventNode.css']
})
export class PhantomEventNode {
  constructor() { }

  @Input() valData: EventInput;

  hoveringStyle = 'black';
  isHovering: boolean = false;

  public documentEnter(): void {
    this.isHovering = true;
  }

  public documentLeave(): void {
    this.isHovering = false;
  }

  updateType() {}
}