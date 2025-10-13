import { Component } from '@angular/core';
import { SubscribeForm } from '../subscribe-form/subscribe-form';
import { MatToolbarModule } from '@angular/material/toolbar';

@Component({
  selector: 'app-footer',
  imports: [SubscribeForm, MatToolbarModule],
  templateUrl: './footer.html',
  styleUrl: './footer.scss'
})
export class Footer {

}
