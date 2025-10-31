import { Component } from '@angular/core';
import { GroceryFormComponent } from './grocery-form/grocery-form.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [GroceryFormComponent],
  template: `
    <div class="app-header">
      <h1>Grocery Planner</h1>
      <p>Create and manage your family grocery lists.</p>
    </div>
    <app-grocery-form></app-grocery-form>
  `,
  styleUrls: ['./app.component.css'],
})
export class AppComponent {}
