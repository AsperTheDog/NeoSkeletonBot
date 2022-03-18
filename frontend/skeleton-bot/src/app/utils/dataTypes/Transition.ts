import { Type } from "@angular/core";

export class Transition {
  constructor(
    id: number,
    origin: number[],
    destination: number[],
    arrowColor: string) {
      this.id = id;
      this.origin = origin;
      this.destination = destination;
      this.arrowColor = arrowColor;
  }

  id: number;
  origin: number[];
  destination: number[];
  arrowColor: string;
}