import { EventInput, ValueInput } from "./Value";

export class Pipeline {
  constructor (type: string, name: string, point: ValueInput | null, eventPoint: EventInput | null) {
    this.id = 0;  
    this.type = type;
    this.name = name;
    this.point = point;
    this.eventPoint = eventPoint;
    this.position = {x: 0, y: 0}
    this.cdkPos = {x: 0, y: 0}
  }

  id: number;
  type: string;
  name: string;
  point: ValueInput | null;
  eventPoint: EventInput | null;
  cdkPos: {x: number, y: number}
  position: {x: number, y: number}
}