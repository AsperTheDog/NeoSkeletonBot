import { Action } from "./dataTypes/Action";
import { Board } from "./dataTypes/Board";
import { User } from "./dataTypes/User";
import { ValueType } from "./dataTypes/ValueType";

export class TemplateManager {
  constructor () {
    this.templateMap = new Map<number, Action>();
  }

  actionTemplates: Action[];
  templateMap: Map<number, Action>;
}

export class BoardManager {
  constructor () {
    this.boards = new Map<string, Board>();
  }

  boards: Map<string, Board>
  boardList: string[];
}

export class TypeValueManager {
  constructor () {

  }

  globalEventList: string[];
  pipelineTypes: string[];
  allowedValues: [number, string][];
  valueTypeMap: Map<number, ValueType>;
}

export class SessionManager {
  constructor () {

  }
  
  usr: User | undefined;
  usrCode: string;
  guilds: {icon: string, id: string, name: string}[] = []
  selectedGuild: string | undefined;
}