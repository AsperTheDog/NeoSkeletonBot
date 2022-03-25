import { Component } from '@angular/core';
import { MainControllerService } from 'src/app/services/main-controller.service';

@Component({
  selector: 'app-customModal',
  templateUrl: 'customModal.html',
  styleUrls: ['customModal.css']
})
export class CustomModal {
  constructor(public mainController: MainControllerService) {
    
    
  }
}