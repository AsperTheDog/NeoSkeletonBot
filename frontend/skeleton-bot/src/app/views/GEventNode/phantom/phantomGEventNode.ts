import { Component, Input } from '@angular/core';
import { GlobalEvent } from 'src/app/utils/dataTypes/GlobalEvent';

@Component({
  selector: 'app-phantomGEventNode',
  templateUrl: 'phantomGEventNode.html',
  styleUrls: ['phantomGEventNode.css']
})
export class PhantomGEventNode {
  constructor() { }

  @Input() mainData: GlobalEvent;
  
  position = {x: 0, y: 0}

  updatePosition(pos: {x: number, y: number}) {
    this.position = pos;
  }
}