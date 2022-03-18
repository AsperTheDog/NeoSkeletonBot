import { ValueType } from "./ValueType";

export class ValueInput {
    constructor (id: number, name: string, valueType: number, nature: string) {
        this.id = id;
        this.name = name;
        this.valueType = valueType;
        this.comboValues = null;
        this.flipped = false;
        this.inColor = "";
        this.fromVariable = false;
        this.nature = nature;
        this.offset = {x: 0, y: 0};
        this.transitionNumber = 0;
    }

    id: number;
    name: string;
    valueType: number;
    nature: string;
    inColor: string;
    fromVariable: boolean;
    flipped : boolean;
    comboValues: string[] | null;
    offset: {x: number, y: number};
    transitionNumber: number;
}

export class EventInput {
    constructor (id:number, name: string, nature: string) {
        this.id = id;
        this.name = name;
        this.flipped = false;
        this.nature = nature;
        this.offset = {x: 0, y: 0};
        this.transitionNumber = 0;
    }

    id: number;
    name: string;
    nature: string;
    flipped : boolean;
    offset: {x: number, y: number};
    transitionNumber: number;
}