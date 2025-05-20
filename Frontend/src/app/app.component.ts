import {
  Component,
  CUSTOM_ELEMENTS_SCHEMA,
  inject,
  OnInit,
} from '@angular/core';
import { RouterModule } from '@angular/router';
import { MenuItem } from 'primeng/api';
import { Menubar } from 'primeng/menubar';
import { CommonModule, NgIf } from '@angular/common';
import { SplitterModule } from 'primeng/splitter';
import { ButtonModule } from 'primeng/button';
import { ToastModule } from 'primeng/toast';
import { AppLogoComponent } from './shared/components/app-logo/app-logo.component';
import { InputContainerComponent } from './search-bar/input-container.component';
@Component({
  imports: [
    RouterModule,
    Menubar,
    CommonModule,
    SplitterModule,
    ButtonModule,
    NgIf,
    ToastModule,
    AppLogoComponent,
    InputContainerComponent
  ],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
})
export class AppComponent implements OnInit {
  public items: MenuItem[] | undefined;

  ngOnInit() {
    this.items = [];
  }

  public showDialog() {}
}
