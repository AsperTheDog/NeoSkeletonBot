import { Component } from '@angular/core';
import { MainControllerService } from 'src/app/services/main-controller.service';

@Component({
  selector: 'app-infoModal',
  templateUrl: 'infoModal.html',
  styleUrls: ['infoModal.css']
})
export class InfoModal {
  constructor(public mainController: MainControllerService) {
    
    
  }
}