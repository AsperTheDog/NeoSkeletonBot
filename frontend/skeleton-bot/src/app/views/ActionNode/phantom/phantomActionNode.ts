import { Component, Input } from '@angular/core';
import { Action } from './../../../utils/Action';

@Component({
  selector: 'app-phantomActionNode',
  templateUrl: 'phantomActionNode.html',
  styleUrls: ['phantomActionNode.css']
})
export class PhantomActionNode {
  constructor() { }

  @Input() mainData: Action;

  position = { x: 0, y: 0 }

  updatePosition(pos: { x: number, y: number }) {
    this.position = pos;
  }
}