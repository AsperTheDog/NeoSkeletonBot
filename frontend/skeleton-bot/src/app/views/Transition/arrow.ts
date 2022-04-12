import { Component, ElementRef, Input, OnChanges, OnInit, SimpleChanges } from '@angular/core';
import { MainControllerService } from 'src/app/services/main-controller.service';
import { Action } from 'src/app/utils/dataTypes/Action';
import { GlobalEvent } from 'src/app/utils/dataTypes/GlobalEvent';
import { MouseData } from 'src/app/utils/dataTypes/Mouse';
import { Transition } from 'src/app/utils/dataTypes/Transition';
import { EventInput, ValueInput } from 'src/app/utils/dataTypes/Value';
import { Variable } from 'src/app/utils/dataTypes/Variable';

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
  orig: ValueInput | EventInput | MouseData;
  dest: ValueInput | EventInput | MouseData;
  origParent: Action | Variable | GlobalEvent;
  destParent: Action | Variable | GlobalEvent;
  origIsMouse: boolean = false;
  destIsMouse: boolean = false;
  Math = Math;

  ngOnChanges(changes: SimpleChanges): void {
    const guild = this.mainController.sessionMan.getGuild()!
    if (!this.data){
      this.data = this.mainController.boardMan.idMan.get(this.dataID, guild)
    }
    if ("destAddress" in changes) {
      if (this.data.destination.length != 0) {
        this.destParent = this.mainController.boardMan.idMan.get(this.data.destination[0], guild)!
        this.dest = this.mainController.boardMan.idMan.get(this.data.destination[1], guild)!
        this.destIsMouse = false;
      }
      else{
        this.dest = this.mainController.mouse
        this.destIsMouse = true;
      }
    }
    if ("origAddress" in changes) {
      if (this.data.origin.length != 0) {
        this.origParent = this.mainController.boardMan.idMan.get(this.data.origin[0], guild)!
        this.orig = this.mainController.boardMan.idMan.get(this.data.origin[1], guild)!
        this.origIsMouse = false;
      }
      else{
        this.orig = this.mainController.mouse
        this.origIsMouse = true;
      }
    }
  }

  removeTrans = () => {
    this.mainController.boardMan.removeTransition(this.mainController.sessionMan.getGuild()!, this.data)
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