import { Component, ElementRef, Input, OnInit, ViewChild } from '@angular/core';
import { DragShieldService } from 'src/app/services/dragshield.service';
import { MainControllerService } from 'src/app/services/main-controller.service';
import { Transition } from 'src/app/utils/dataTypes/Transition';
import { EventInput } from 'src/app/utils/dataTypes/Value';
import { ActionNode } from '../../ActionNode/actionNode';
import { GEventNode } from '../../GEventNode/GEventNode';
import { PipelineNode } from '../../PipelineNode/PipelineNode';
import { ValueNode } from '../value/valueNode';

@Component({
  selector: 'app-eventNode',
  templateUrl: 'eventNode.html',
  styleUrls: ['eventNode.css']
})
export class EventNode implements OnInit {
  constructor(
    public elRef: ElementRef,
    public mainController: MainControllerService,
    public dragShield: DragShieldService) { }

  @ViewChild('locationRef') arrowOrig: ElementRef;

  @Input() valDataID: number;
  @Input() dragged: boolean = false;

  parentNode: ActionNode | GEventNode | PipelineNode;
  activeTransition: Transition | null = null;
  isHovering = false;
  valData: EventInput;

  ngOnInit(): void {
    this.valData = this.mainController.boardMan.idMan.get(this.valDataID)
  }

  public documentEnter(): void {
    this.mainController.hovering = this;
    this.isHovering = true;
  }

  public documentLeave(): void {
    this.mainController.hovering = null
    this.isHovering = false;
  }

  createTransition() {
    if (this.activeTransition != null) {
      return;
    }
    if (this.valData.nature == "out" &&
      this.valData.transitionNumber != 0) {
      return;
    }
    const sel = window.getSelection()
    if (sel != null) {
      sel.removeAllRanges();
    }
    this.dragShield.disableDrag();
    const trns = new Transition(
      0,
      this.valData.nature == "out" ? [this.parentNode.mainData.id, this.valData.id] : [],
      this.valData.nature == "out" ? [] : [this.parentNode.mainData.id, this.valData.id],
      'gray'
    )
    this.mainController.boardMan.addTransition(trns)
    this.mainController.transStartInput = this
    this.activeTransition = trns;
  }

  finishTransition() {
    if (this.activeTransition == null) return;

    const sel = window.getSelection()
    if (sel != null) {
      sel.removeAllRanges();
    }

    this.dragShield.enableDrag();

    if (this.mainController.hovering == null) {
      this.mainController.manageInfo("Transition canceled: no destination", true)
      this.mainController.boardMan.removeTransition();
      this.activeTransition = null;
      return;
    }

    if (this.mainController.hovering instanceof ValueNode) {
      this.mainController.manageInfo("Transition canceled: cannot connect event to value", true)
      this.mainController.boardMan.removeTransition();
      this.activeTransition = null;
      return;
    }

    var origNode: EventNode;
    var destNode: EventNode;

    if (this.valData.nature == "in") {
      origNode = this.mainController.hovering
      destNode = this
    }
    else {
      origNode = this
      destNode = this.mainController.hovering
    }

    if (origNode == destNode) {
      this.mainController.boardMan.removeTransition();
      this.activeTransition = null;
      return;
    }

    if (origNode.valData.nature == destNode.valData.nature) {
      this.mainController.manageInfo("Transition cancelled: must be made between an input and an output", true)
      this.mainController.boardMan.removeTransition();
      this.activeTransition = null;
      return;
    }

    if (this.activeTransition.destination.length == 0) {
      this.activeTransition.destination = [destNode.parentNode.mainData.id, destNode.valData.id]
      destNode.valData.transitionNumber++;
    }
    if (this.activeTransition.origin.length == 0) {
      this.activeTransition.origin = [origNode.parentNode.mainData.id, origNode.valData.id]
      origNode.valData.transitionNumber++;
    }

    this.mainController.manageInfo("Transition created: '" + origNode.valData.name + "' to '" + destNode.valData.name + "'", false)
    this.mainController.transStartInput = null
    this.activeTransition = null;
  }

  updateInput() {
    this.valData.offset = {
      x: this.arrowOrig.nativeElement.getBoundingClientRect().x - this.parentNode.mainRef.nativeElement.getBoundingClientRect().x,
      y: this.arrowOrig.nativeElement.getBoundingClientRect().y - this.parentNode.mainRef.nativeElement.getBoundingClientRect().y
    }
  }

  removeAllTrans() {
    this.mainController.manageInfo("Removed all transitions for node '" + this.valData.name + "'", false)
    this.mainController.boardMan.cleanTransitions(this.parentNode.mainData.id, this.valData)
  }
}
