import { Component, Input, ViewChild } from '@angular/core';
import { Pipeline } from 'src/app/utils/dataTypes/Pipeline';
import { PhantomEventNode } from '../../input/event/phantom/phantomEventNode';
import { PhantomValueNode } from '../../input/value/phantom/phantomValueNode';

@Component({
  selector: 'app-phantomPipelineNode',
  templateUrl: 'phantomPipelineNode.html',
  styleUrls: ['phantomPipelineNode.css']
})
export class PhantomPipelineNode {
  constructor() { }

  @Input() mainData: Pipeline;
  
  @ViewChild("valueRef") vRef: PhantomValueNode;
  @ViewChild("eventRef") eRef: PhantomEventNode;

  position = {x: 0, y: 0}

  updateType() {
    if (this.vRef){
      this.vRef.updateType()
    }
    if (this.eRef){
      this.eRef.updateType()
    }
  }

  updatePosition(pos: {x: number, y: number}) {
    this.position = pos;
  }
}