import { Injectable } from '@angular/core';
import { AppComponent } from '../app.component';

@Injectable({
  providedIn: 'root'
})
export class DragShieldService {
  constructor() { }

  canvas: AppComponent;

  disableDrag() {
    this.canvas?.disableDrag();
  }

  enableDrag() {
    this.canvas?.enableDrag();
  }
}