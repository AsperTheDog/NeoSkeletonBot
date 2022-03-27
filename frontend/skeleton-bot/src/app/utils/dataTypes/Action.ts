import { ValueInput, EventInput } from "./Value";

export class Action {
    constructor (id: number, type: string, inputs: ValueInput[], outputs: ValueInput[], events: EventInput[], inputEvent: EventInput) {
        this.type = type;
        this.id = id;
        this.inputs = inputs;
        this.outputs = outputs;
        this.events = events;
        this.inputEvent = inputEvent;
    }
    
    id: number;
    type: string;
    description: string;
    group: string;
    position: {x: number, y: number}
    cdkPos: {x: number, y: number}
    inputs: ValueInput[];
    outputs: ValueInput[];
    events: EventInput[];
    inputEvent: EventInput;
  }