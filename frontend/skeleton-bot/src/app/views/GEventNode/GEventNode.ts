import { AfterViewInit, Component, ElementRef, Input, OnInit, ViewChild } from '@angular/core';
import { MainControllerService } from 'src/app/services/main-controller.service';
import { DragShieldService } from 'src/app/services/dragshield.service';
import { CdkDragEnd } from '@angular/cdk/drag-drop';
import { GlobalEvent } from 'src/app/utils/dataTypes/GlobalEvent';
import { EventNode } from '../input/event/eventNode';
import { ValueNode } from '../input/value/valueNode';

@Component({
  selector: 'app-GEventNode',
  templateUrl: 'GEventNode.html',
  styleUrls: ['GEventNode.css']
})
export class GEventNode implements OnInit, AfterViewInit {
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
  mainData: GlobalEvent;
  struct: string;

  ngOnInit(): void {
    this.mainData = this.mainController.boardMan.idMan.get(this.mainDataID, this.mainController.sessionMan.getGuild()!)
    this.struct = this.mainController.typeValMan.getStruct(this.mainData.name)
    this.position = this.mainData.cdkPos
  }

  ngAfterViewInit(): void {
    this.eventOutput.parentNode = this
    this.eventOutput.updateInput()
    this.valueOutput.parentNode = this
    this.valueOutput.gEvntUpdateInput()
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
      x: Math.round(this.mainRef.nativeElement.getBoundingClientRect().x - this.mainController.boardCoords.x),
      y: Math.round(this.mainRef.nativeElement.getBoundingClientRect().y - this.mainController.boardCoords.y)
    }
  }

  getVarCoords(event: CdkDragEnd) {
    this.dragShield.canvas.draggingNode = false;
    this.mainData.cdkPos = event.source.getFreeDragPosition()
    this.mainController.checkIfDelete(this.mainData, "event")
  }

  reload() {
    this.mainData = this.mainController.boardMan.idMan.get(this.mainDataID, this.mainController.sessionMan.getGuild()!)
    this.position = this.mainData.cdkPos
    this.eventOutput.reload()
    this.valueOutput.reload()
  }
}