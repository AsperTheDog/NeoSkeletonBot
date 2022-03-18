import { Component, ElementRef, Input, OnChanges, OnInit, SimpleChanges } from '@angular/core';
import { MainControllerService } from 'src/app/services/main-controller.service';
import { Action } from 'src/app/utils/dataTypes/Action';
import { GlobalEvent } from 'src/app/utils/GlobalEvent';
import { mouseData } from 'src/app/utils/Mouse';
import { Transition } from 'src/app/utils/Transition';
import { EventInput, ValueInput } from 'src/app/utils/Value';
import { Variable } from 'src/app/utils/Variable';

@Component({
  selector: 'app-arrow',
  templateUrl: 'arrow.html',
  styleUrls: ['arrow.css']
})
export class Arrow implements OnChanges {
  constructor(public elRef: ElementRef,
    public mainController: MainControllerService) { }

  @Input() dataID: number;
  @Input() destAddress: number | null;
  @Input() origAddress: number | null;

  data: Transition;
  orig: ValueInput | EventInput | mouseData;
  dest: ValueInput | EventInput | mouseData;
  origParent: Action | Variable | GlobalEvent;
  destParent: Action | Variable | GlobalEvent;
  origIsMouse: boolean = false;
  destIsMouse: boolean = false;
  Math = Math;

  ngOnChanges(changes: SimpleChanges): void {
    if (!this.data){
      this.data = this.mainController.get(this.dataID)
    }
    if ("destAddress" in changes) {
      if (this.data.destination.length != 0) {
        this.destParent = this.mainController.get(this.data.destination[0])!
        this.dest = this.mainController.get(this.data.destination[1])!
        this.destIsMouse = false;
      }
      else{
        this.dest = this.mainController.mouse
        this.destIsMouse = true;
      }
    }
    if ("origAddress" in changes) {
      if (this.data.origin.length != 0) {
        this.origParent = this.mainController.get(this.data.origin[0])!
        this.orig = this.mainController.get(this.data.origin[1])!
        this.origIsMouse = false;
      }
      else{
        this.orig = this.mainController.mouse
        this.origIsMouse = true;
      }
    }
  }

  removeTrans = () => {
    this.mainController.removeTransition(this.data)
  }
  
  getDirs = () => {
    var destPos;
    var origPos;
    if (this.destIsMouse){
      destPos = this.dest.offset
    }
    else{
      destPos = {
        x: this.destParent.position.x + this.dest.offset.x,
        y: this.destParent.position.y + this.dest.offset.y
      }
    }
    if (this.origIsMouse){
      origPos  = this.orig.offset
    }
    else{
      origPos = {
        x: this.origParent.position.x + this.orig.offset.x,
        y: this.origParent.position.y + this.orig.offset.y
      }
    }
    var origDir = 0
    var destDir = 0
    if (this.origIsMouse){
      destDir = ((this.dest as ValueInput | EventInput).nature == "in" != (this.dest as ValueInput | EventInput).flipped) ?
        destPos.x - 200 : 
        destPos.x + 200
      origDir = (destDir + origPos.x) / 2
    }
    else {
      origDir = ((this.orig as ValueInput | EventInput).nature == "in" != (this.orig as ValueInput | EventInput).flipped) ?
        origPos.x - 200 : 
        origPos.x + 200
      if (this.destIsMouse){
        destDir = (origDir + destPos.x) / 2
      }
      else {
        destDir = ((this.dest as ValueInput | EventInput).nature == "in" != (this.dest as ValueInput | EventInput).flipped) ?
          destPos.x - 200 : 
          destPos.x + 200
      }
    }

    return 'M' + origPos.x + ',' + origPos.y + 
          ' C' + origDir + ',' + origPos.y + 
           ' ' + destDir + ',' + destPos.y + 
           ' ' + destPos.x + ',' +  destPos.y
  }
}