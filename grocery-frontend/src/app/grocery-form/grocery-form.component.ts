import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  AbstractControl,
  FormArray,
  FormGroup,
  ReactiveFormsModule,
} from '@angular/forms';
import {
  CreateGroceryPayload,
  GroceryFormFactory,
  GroceryFormGroup,
  GroceryItemFormGroup,
  GroceryItemFormValue,
  GroceryItemPayload,
  Item,
} from '../models';
import { GroceryService } from '../services/grocery.service';

@Component({
  selector: 'app-grocery-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './grocery-form.component.html',
  styleUrls: ['./grocery-form.component.css'],
})
export class GroceryFormComponent implements OnInit {
  groceryForm: GroceryFormGroup;
  availableItems: Item[] = [];
  saveSuccess = false;
  isSubmitting = false;

  constructor(
    private readonly formFactory: GroceryFormFactory,
    private readonly groceryService: GroceryService,
  ) {
    this.groceryForm = this.formFactory.createList();
  }

  ngOnInit(): void {
    this.groceryService.getItems().subscribe({
      next: (data) => (this.availableItems = data),
      error: (err) => console.error('Error fetching items', err),
    });
  }

  get items(): FormArray<GroceryItemFormGroup> {
    return this.groceryForm.controls.grocery_items;
  }

  addItem(): void {
    this.items.push(this.formFactory.createItem());
  }

  removeItem(index: number): void {
    if (this.items.length > 1) {
      this.items.removeAt(index);
    }
  }

  trackByIndex(index: number): number {
    return index;
  }

  isFieldInvalid(field: 'family_id' | 'grocery_date'): boolean {
    const control = this.groceryForm.controls[field];
    return control.invalid && (control.touched || control.dirty);
  }

  isItemFieldInvalid(
    index: number,
    field: 'item_id' | 'quantity' | 'purchased',
  ): boolean {
    const control = this.items.at(index).controls[field];
    return control.invalid && (control.touched || control.dirty);
  }

  private markFormTouched(control: AbstractControl): void {
    control.markAsTouched();
    control.markAsDirty();

    if (control instanceof FormGroup) {
      Object.values(control.controls).forEach((child) =>
        this.markFormTouched(child),
      );
    } else if (control instanceof FormArray) {
      control.controls.forEach((child) => this.markFormTouched(child));
    }
  }

  submitForm(): void {
    if (this.groceryForm.invalid) {
      this.markFormTouched(this.groceryForm);
      return;
    }

    this.isSubmitting = true;
    const formValue = this.groceryForm.getRawValue();

    const payload: CreateGroceryPayload = {
      family_id: Number(formValue.family_id),
      grocery_date: formValue.grocery_date,
      grocery_items: formValue.grocery_items.map<GroceryItemPayload>(
        (item: GroceryItemFormValue) => ({
          item_id: Number(item.item_id),
          quantity: Number(item.quantity),
          purchased: Boolean(item.purchased),
        }),
      ),
    };

    this.groceryService.addGrocery(payload).subscribe({
      next: () => {
        this.saveSuccess = true;
        this.isSubmitting = false;
        this.groceryForm.reset({ family_id: 1, grocery_date: '' });
        this.items.clear();
        this.addItem();
        this.groceryForm.markAsPristine();
        this.groceryForm.markAsUntouched();
        setTimeout(() => (this.saveSuccess = false), 3000);
      },
      error: (err) => {
        this.isSubmitting = false;
        console.error('Error saving grocery:', err);
        alert('Failed to save grocery');
      },
    });
  }
}
