import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-logo',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="relative">
      <i class="pi pi-comments" [ngClass]="iconClass"></i>
      <div class="absolute -top-2 -right-2">
        <i class="pi pi-bolt" [ngClass]="boltClass"></i>
      </div>
    </div>
  `,
  styles: [':host { display: block; }']
})
export class AppLogoComponent {
  @Input() size: 'sm' | 'md' | 'lg' = 'lg';

  get iconClass(): string {
    const sizes = {
      sm: 'text-4xl',
      md: 'text-5xl',
      lg: 'text-6xl'
    };
    return `${sizes[this.size]} text-sky-600`;
  }

  get boltClass(): string {
    const sizes = {
      sm: 'text-lg',
      md: 'text-xl',
      lg: 'text-2xl'
    };
    return `${sizes[this.size]} text-yellow-500`;
  }
} 