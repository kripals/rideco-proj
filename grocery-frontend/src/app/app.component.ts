import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { GroceryFormComponent } from './grocery-form/grocery-form.component';
import { GroceryListComponent } from './grocery-list/grocery-list.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, GroceryFormComponent, GroceryListComponent],
  template: `
    <div class="app-header">
      <h1>Grocery Planner</h1>
      <p>Create and manage your family grocery lists.</p>
    </div>

    <nav class="app-nav">
      <button
        type="button"
        [class.active]="activeView === 'planner'"
        (click)="setView('planner')"
      >
        Planner
      </button>
      <button
        type="button"
        [class.active]="activeView === 'lists'"
        (click)="setView('lists')"
      >
        Saved Lists
      </button>
    </nav>

    <section class="app-content">
      <app-grocery-form *ngIf="activeView === 'planner'"></app-grocery-form>
      <app-grocery-list *ngIf="activeView === 'lists'"></app-grocery-list>
    </section>
  `,
  styleUrls: ['./app.component.css'],
})
export class AppComponent {
  activeView: 'planner' | 'lists' = 'planner';

  setView(view: 'planner' | 'lists'): void {
    this.activeView = view;
  }
}
