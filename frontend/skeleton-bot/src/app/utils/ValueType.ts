export class ValueType {
  constructor (name: string, color: string, compatible: number[], hasInitial: boolean, initial: string) {
    this.id = -1;
    this.name = name;
    this.color = color;
    this.compatible = compatible;
    this.hasInitial = hasInitial;
    if (this.hasInitial){
      this.initial = initial
    }
    else{
      this.initial = ""
    }
  }

  id: number;
  name: string;
  color: string;
  compatible: number[];
  canBeVar: boolean;
  varInOut: number[];
  hasInitial: boolean;
  initial: string;
}