import { EventInput, ValueInput } from "./Value";

export class GlobalEvent {
  constructor (name: string, eventOutput: EventInput, output: ValueInput) {
    this.id = 0;  
    this.name = name;
    this.output = output;
    this.eventOutput = eventOutput;
    this.position = {x: 0, y: 0}
    this.cdkPos = {x: 0, y: 0}
  }

  id: number;
  name: string;
  output: ValueInput;
  eventOutput: EventInput;
  cdkPos: {x: number, y: number}
  position: {x: number, y: number}
}