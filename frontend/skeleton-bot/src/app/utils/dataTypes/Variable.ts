import { ValueInput } from "./Value";
import { VarElement } from "./VarElement";

export class Variable {
  constructor (varAttr: number, input: ValueInput, output: ValueInput) {
    this.id = 0;  
    this.varAttr = varAttr;
    this.input = input;
    this.output = output;
    this.cdkPos = {x: 0, y: 0}
    this.position = {x: 0, y: 0}
    this.comboTag = null;
  }

  id: number;
  varAttr: number;
  input: ValueInput;
  output: ValueInput;
  cdkPos: {x: number, y: number}
  position: {x: number, y: number}
  comboTag: string | null
}