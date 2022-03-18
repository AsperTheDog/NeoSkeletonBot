export class VarElement {
  constructor (name: string, valueType: number, initialValue: string) {
    this.id = -1;
    this.name = name;
      if (this.name == ""){
        this.constant = true;
      }
      else {
        this.constant = false;
      }
      this.valueType = valueType;
      this.initialValue = initialValue;
      this.possibleValues = null;
      this.references = 0;
  }

  id: number;
  name: string;
  constant: boolean;
  valueType: number;
  initialValue: string;
  possibleValues: string[] | null;
  references: number;
}