import { Action } from "./Action";
import { GlobalEvent } from "./GlobalEvent";
import { Pipeline } from "./Pipeline";
import { Transition } from "./Transition";
import { VarElement } from "./VarElement";
import { Variable } from "./Variable";

export class Board {
  constructor(name: string, guild: number, actions: Action[], variables: VarElement[], varInstances: Variable[], transitions: Transition[], globalEvents: GlobalEvent[], pipelines: Pipeline[]) {
    this.name = name;
    this.guild = guild;
    this.actions = actions;
    this.variables = variables;
    this.varInstances = varInstances;
    this.transitions = transitions;
    this.globalEvents = globalEvents;
    this.pipelines = pipelines;
    this.hasEvInput = false;
  }

  name: string;
  guild: number;
  actions: Action[];
  variables: VarElement[];
  varInstances: Variable[];
  transitions: Transition[];
  globalEvents: GlobalEvent[];
  pipelines: Pipeline[];
  hasEvInput: boolean;
}