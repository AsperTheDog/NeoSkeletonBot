import { Component, ElementRef, Input, OnInit, ViewChild } from '@angular/core';
import { DragShieldService } from 'src/app/services/dragshield.service';
import { MainControllerService } from 'src/app/services/main-controller.service';
import { Transition } from 'src/app/utils/dataTypes/Transition';
import { EventInput, ValueInput } from 'src/app/utils/dataTypes/Value';
import { ValueType } from 'src/app/utils/dataTypes/ValueType';
import { ActionNode } from '../../ActionNode/actionNode';
import { GEventNode } from '../../GEventNode/GEventNode';
import { PipelineNode } from '../../PipelineNode/PipelineNode';
import { VariableNode } from '../../VariableNode/variableNode';
import { EventNode } from '../event/eventNode';

@Component({
  selector: 'app-valueNode',
  templateUrl: 'valueNode.html',
  styleUrls: ['valueNode.css']
})
export class ValueNode implements OnInit {
  constructor(
    public elRef: ElementRef,
    public mainController: MainControllerService,
    public dragShield: DragShieldService) { }

  @ViewChild('locationRef') arrowOrig: ElementRef;

  @Input() valDataID: number;
  @Input() dragged: boolean = false;

  parentNode: ActionNode | VariableNode | GEventNode | PipelineNode;
  activeTransition: Transition | null = null;
  hoveringStyle = 'black'
  isHovering = false;
  comboTag: string = "";
  valData: ValueInput;
  valueType: ValueType;

  ngOnInit(): void {
    this.valData = this.mainController.boardMan.idMan.get(this.valDataID, this.mainController.sessionMan.getGuild()!)
    this.valueType = this.mainController.typeValMan.getType(this.valData.valueType)
    this.hoveringStyle = this.valueType.color
    if (this.valData.comboValues) {
      this.comboTag = this.valData.comboValues.length + ""
      for (let elem of this.valData.comboValues) {
        this.comboTag += ":" + elem
      }
    }
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

    const sel = window.getSelection()
    if (sel != null) {
      sel.removeAllRanges();
    }

    this.mainController.boardMan.updateBuffer()
    
    this.dragShield.disableDrag();
    const trns = new Transition(
      0,
      this.valData.nature == "out" ? [this.parentNode.mainData.id, this.valData.id] : [],
      this.valData.nature == "out" ? [] : [this.parentNode.mainData.id, this.valData.id],
      this.valueType.color
    )
    this.mainController.boardMan.addTransition(trns, this.mainController.sessionMan.getGuild()!)
    this.mainController.transStartInput = this
    this.activeTransition = trns;
    this.valData.inColor = this.valueType.color
  }

  finishTransition() {
    if (this.activeTransition == null) return;

    const sel = window.getSelection()
    if (sel != null) {
      sel.removeAllRanges();
    }

    this.dragShield.enableDrag();

    const guild = this.mainController.sessionMan.getGuild()
    if (!guild) return;
    
    if (this.mainController.hovering == null) {
      this.mainController.manageInfo("Transition canceled: no destination", true)
      this.mainController.boardMan.removeTransition(guild);
      this.activeTransition = null;
      return;
    }

    if (this.mainController.hovering instanceof EventNode) {
      this.mainController.manageInfo("Transition canceled: cannot connect value to event", true)
      this.mainController.boardMan.removeTransition(guild);
      this.activeTransition = null;
      return;
    }

    var origNode: ValueNode;
    var destNode: ValueNode;

    if (this.valData.nature == "in") {
      origNode = this.mainController.hovering
      destNode = this
    }
    else {
      origNode = this
      destNode = this.mainController.hovering
    }

    if (origNode.valData.nature == destNode.valData.nature) {
      this.mainController.manageInfo("Transition cancelled: must be made between an input and an output", true)
      this.mainController.boardMan.removeTransition(guild);
      this.activeTransition = null;
      return;
    }

    if (!origNode.valueType.compatible.includes(destNode.valueType.id)) {
      this.mainController.manageInfo("Transition canceled: origin and destination are not of compatible types", true)
      this.mainController.boardMan.removeTransition(guild);
      this.activeTransition = null;
      return;
    }

    var futureCombo = destNode.valData.comboValues
    if (origNode.valData.nature == 'out' &&
      origNode.valueType.id == 2 &&
      origNode.parentNode instanceof VariableNode &&
      origNode.parentNode.mainData.comboTag != destNode.comboTag &&
      origNode.parentNode.mainData.comboTag) {

      this.mainController.manageInfo("Transition canceled: Origin has a different combo attached", true)
      this.mainController.boardMan.removeTransition(guild);
      this.activeTransition = null;
      return;
    }

    if (destNode.valData.fromVariable) {
      this.mainController.manageInfo("Transition canceled: Destination is already linked to a variable", true)
      this.mainController.boardMan.removeTransition(guild);
      this.activeTransition = null;
      return;
    }

    if (origNode.parentNode instanceof VariableNode) {
      if (destNode.parentNode instanceof VariableNode){
        this.mainController.manageInfo("Transition canceled: Variables cannot be attached to other variables", true)
        this.mainController.boardMan.removeTransition(guild);
        this.activeTransition = null;
        return;
      }
      if (destNode.valData.transitionNumber != 0 && !(destNode.valData.transitionNumber == 1 && destNode == this)) {
        this.mainController.manageInfo("Transition canceled: Variable origins can only be attached to empty destinations", true)
        this.mainController.boardMan.removeTransition(guild);
        this.activeTransition = null;
        return;
      }
      else {
        destNode.valData.fromVariable = true;
      }
    }

    if (this.activeTransition.destination.length == 0) {
      this.activeTransition.destination = [destNode.parentNode.mainData.id, destNode.valData.id]
      destNode.valData.transitionNumber++;
    }
    if (this.activeTransition.origin.length == 0) {
      this.activeTransition.origin = [origNode.parentNode.mainData.id, origNode.valData.id]
      origNode.valData.transitionNumber++;
    }

    this.mainController.hovering.valData.inColor = this.activeTransition.arrowColor
    //destNode.valData.inColor = origNode.valueType.color

    if (origNode.valueType.id == 2 && origNode.parentNode instanceof VariableNode) {
      var varElem = this.mainController.boardMan.idMan.get(origNode.parentNode.mainData.varAttr, guild)
      var futureCombo = destNode.valData.comboValues
      varElem.possibleValues = futureCombo
      origNode.parentNode.mainData.comboTag = destNode.comboTag
    }

    this.mainController.manageInfo("Transition created: '" + origNode.valData.name + "' to '" + destNode.valData.name + "'", false)
    this.mainController.transStartInput = null
    this.activeTransition = null;
  }


  gEvntUpdateInput() {
    this.valData.preview = (this.parentNode as GEventNode).struct
    this.updateInput()
  }

  updateInput() {
    this.valData.offset = {
      x: this.arrowOrig.nativeElement.getBoundingClientRect().x - this.parentNode.mainRef.nativeElement.getBoundingClientRect().x,
      y: this.arrowOrig.nativeElement.getBoundingClientRect().y - this.parentNode.mainRef.nativeElement.getBoundingClientRect().y
    }
  }

  removeAllTrans() {
    this.mainController.boardMan.updateBuffer()
    this.mainController.manageInfo("Removed all transitions for node '" + this.valData.name + "'", false)
    this.mainController.boardMan.cleanTransitions(this.parentNode.mainData.id, this.mainController.sessionMan.getGuild()!, this.valData)
  }

  reload() {
    this.valData = this.mainController.boardMan.idMan.get(this.valDataID, this.mainController.sessionMan.getGuild()!)
  }
}
