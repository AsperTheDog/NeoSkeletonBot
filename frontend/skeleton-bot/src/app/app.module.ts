import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';

import { AppComponent } from './app.component';
import { ActionNode } from './views/ActionNode/actionNode';
import { MaterialExModule } from 'src/material.module';
import { Arrow } from './views/Transition/arrow';
import { VariableNode } from './views/VariableNode/variableNode';
import { FormsModule } from '@angular/forms';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatTabsModule } from '@angular/material/tabs';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { PhantomActionNode } from './views/ActionNode/phantom/phantomActionNode';
import { PhantomVariableNode } from './views/VariableNode/phantom/phantomVariableNode';
import { GEventNode } from './views/GEventNode/GEventNode';
import { PhantomGEventNode } from './views/GEventNode/phantom/phantomGEventNode';
import { ValueNode } from './views/input/value/valueNode';
import { EventNode } from './views/input/event/eventNode';
import { PhantomValueNode } from './views/input/value/phantom/phantomValueNode';
import { PhantomEventNode } from './views/input/event/phantom/phantomEventNode';
import { HttpClientModule } from '@angular/common/http';
import { PipelineNode } from './views/PipelineNode/PipelineNode';
import { PhantomPipelineNode } from './views/PipelineNode/phantom/phantomPipelineNode';
import { CookieModule } from 'ngx-cookie';
import { CustomModal } from './views/customModal/customMoal';
import { InfoModal } from './views/infoModal/infoModal';

@NgModule({
  declarations: [
    AppComponent,
    ActionNode,
    ValueNode,
    EventNode,
    VariableNode,
    Arrow,
    GEventNode,
    PipelineNode,
    PhantomValueNode,
    PhantomEventNode,
    PhantomActionNode,
    PhantomVariableNode,
    PhantomGEventNode,
    PhantomPipelineNode,
    CustomModal,
    InfoModal,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    MaterialExModule,
    FormsModule,
    BrowserAnimationsModule,
    MatExpansionModule,
    MatTabsModule,
    HttpClientModule,
    CookieModule.forRoot()
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
