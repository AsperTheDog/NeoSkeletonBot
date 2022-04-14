import { AfterViewInit, Component, ElementRef, Input, OnInit, QueryList, ViewChild, ViewChildren } from '@angular/core';
import { Action } from '../../utils/dataTypes/Action';
import { MainControllerService } from 'src/app/services/main-controller.service';
import { CdkDragEnd } from '@angular/cdk/drag-drop';
import { DragShieldService } from 'src/app/services/dragshield.service';
import { EventInput } from 'src/app/utils/dataTypes/Value';
import { ValueNode } from '../input/value/valueNode';
import { EventNode } from '../input/event/eventNode';

@Component({
  selector: 'app-actionNode',
  templateUrl: 'actionNode.html',
  styleUrls: ['actionNode.css']
})
export class ActionNode implements OnInit, AfterViewInit {
  constructor(
    public mainController: MainControllerService,
    public elRef: ElementRef,
    public dragShield: DragShieldService) { }

  @ViewChild("mainRef") mainRef: ElementRef;
  @ViewChildren("valueRef") valueInOut: QueryList<ValueNode>;
  @ViewChildren("eventRef") eventInOut: QueryList<EventNode>;

  @Input() mainDataID: number;

  mainData: Action = new Action(-1, "", [], [], [], new EventInput(-1, "", ""));

  position = { x: 0, y: 0 }

  ngOnInit(): void {
    this.mainData = this.mainController.boardMan.idMan.get(this.mainDataID, this.mainController.sessionMan.getGuild()!)
    this.position = this.mainData.cdkPos
  }

  ngAfterViewInit(): void {
    this.valueInOut.forEach((inOut) => {
      inOut.parentNode = this
      inOut.updateInput()
    })
    this.eventInOut.forEach((inOut) => {
      inOut.parentNode = this
      inOut.updateInput()
    })
  }

  onDragStart() {
    this.mainController.boardMan.updateBuffer();
    this.dragShield.canvas.draggingNode = true;
  }

  onDragMove() {
    this.updateCoords()
  }


  onDragEnd(event: CdkDragEnd) {
    this.getActionCoords(event)
  }

  updateCoords() {
    this.mainData.position = {
      x: this.mainRef.nativeElement.getBoundingClientRect().x - this.mainController.boardCoords.x,
      y: this.mainRef.nativeElement.getBoundingClientRect().y - this.mainController.boardCoords.y
    }
  }

  getActionCoords(event: CdkDragEnd) {
    this.dragShield.canvas.draggingNode = false
    this.mainData.cdkPos = event.source.getFreeDragPosition()
    this.mainController.checkIfDelete(this.mainData, "action")
  }

  reload() {
    this.mainData = this.mainController.boardMan.idMan.get(this.mainDataID, this.mainController.sessionMan.getGuild()!)
    this.position = this.mainData.cdkPos
    this.valueInOut.forEach((inOut) => {
      inOut.reload()
    })
    this.eventInOut.forEach((inOut) => {
      inOut.reload()
    })
  }
}