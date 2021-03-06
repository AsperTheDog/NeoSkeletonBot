import { AfterViewInit, Component, ElementRef, Input, OnInit, ViewChild } from '@angular/core';
import { MainControllerService } from 'src/app/services/main-controller.service';
import { DragShieldService } from 'src/app/services/dragshield.service';
import { CdkDragEnd } from '@angular/cdk/drag-drop';
import { EventNode } from '../input/event/eventNode';
import { ValueNode } from '../input/value/valueNode';
import { Pipeline } from 'src/app/utils/dataTypes/Pipeline';

@Component({
  selector: 'app-pipelineNode',
  templateUrl: 'pipelineNode.html',
  styleUrls: ['pipelineNode.css']
})
export class PipelineNode implements OnInit, AfterViewInit {
  constructor(
    public mainController: MainControllerService,
    public dragShield: DragShieldService,
    public elRef: ElementRef) { }

  @ViewChild("mainRef") mainRef: ElementRef;
  @ViewChild("valueRef") valueOutput: ValueNode;
  @ViewChild("eventRef") eventOutput: EventNode;

  @Input() mainDataID: number;

  dragDisabled = false;
  position = { x: 0, y: 0 }
  mainData: Pipeline;

  ngOnInit(): void {
    this.mainData = this.mainController.boardMan.idMan.get(this.mainDataID, this.mainController.sessionMan.getGuild()!)
    this.position = this.mainData.cdkPos
  }

  ngAfterViewInit(): void {
    if (this.eventOutput) {
      this.eventOutput.parentNode = this
      this.eventOutput.updateInput()
    }
    if (this.valueOutput) {
      this.valueOutput.parentNode = this
      this.valueOutput.updateInput()
    }
  }

  onDragStart() {
    this.mainController.boardMan.updateBuffer();
    this.dragShield.canvas.draggingNode = true;
  }

  onDragMove() {
    this.updateCoords()
  }

  onDragEnd(event: CdkDragEnd) {
    this.getVarCoords(event)
  }

  updateCoords() {
    this.mainData.position = {
      x: this.mainRef.nativeElement.getBoundingClientRect().x - this.mainController.boardCoords.x,
      y: this.mainRef.nativeElement.getBoundingClientRect().y - this.mainController.boardCoords.y
    }
  }

  getVarCoords(event: CdkDragEnd) {
    this.dragShield.canvas.draggingNode = false;
    this.mainData.cdkPos = event.source.getFreeDragPosition()
    this.mainController.checkIfDelete(this.mainData, "pipeline")
  }

  reload() {
    this.mainData = this.mainController.boardMan.idMan.get(this.mainDataID, this.mainController.sessionMan.getGuild()!)
    this.position = this.mainData.cdkPos
    if (this.eventOutput) {
      this.eventOutput.reload()
    }
    if (this.valueOutput) {
      this.valueOutput.reload()
    }
  }
}