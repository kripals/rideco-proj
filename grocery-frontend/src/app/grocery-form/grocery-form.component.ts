import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  FormArray,
  FormBuilder,
  FormGroup,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import {
  CreateGroceryPayload,
  GroceryItemPayload,
  GroceryService,
  Item,
} from '../services/grocery.service';

@Component({
  selector: 'app-grocery-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './grocery-form.component.html',
  styleUrls: ['./grocery-form.component.css'],
})
export class GroceryFormComponent implements OnInit {
  groceryForm: FormGroup;
  availableItems: Item[] = [];
  saveSuccess = false;
  isSubmitting = false;

  constructor(private fb: FormBuilder, private groceryService: GroceryService) {
    this.groceryForm = this.fb.group({
      family_id: [1, Validators.required],
      grocery_date: ['', Validators.required],
      grocery_items: this.fb.array([this.createItem()]),
    });
  }

  ngOnInit(): void {
    this.groceryService.getItems().subscribe({
      next: (data) => (this.availableItems = data),
      error: (err) => console.error('Error fetching items', err),
    });
  }

  get items(): FormArray {
    return this.groceryForm.get('grocery_items') as FormArray;
  }

  createItem(): FormGroup {
    return this.fb.group({
      item_id: ['', Validators.required],
      quantity: [1, [Validators.required, Validators.min(1)]],
      purchased: [false],
    });
  }

  addItem(): void {
    this.items.push(this.createItem());
  }

  removeItem(index: number): void {
    if (this.items.length > 1) {
      this.items.removeAt(index);
    }
  }

  trackByIndex(index: number): number {
    return index;
  }

  isFieldInvalid(field: string): boolean {
    const control = this.groceryForm.get(field);
    return !!control && control.invalid && (control.touched || control.dirty);
  }

  isItemFieldInvalid(index: number, field: string): boolean {
    const control = (this.items.at(index) as FormGroup).get(field);
    return !!control && control.invalid && (control.touched || control.dirty);
  }

  private markFormTouched(form: FormGroup | FormArray): void {
    Object.values(form.controls).forEach((control) => {
      if (control instanceof FormGroup || control instanceof FormArray) {
        this.markFormTouched(control);
      }
      control.markAsTouched();
      control.markAsDirty();
    });
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
      grocery_items: (formValue.grocery_items ?? []).map(
        (item: GroceryItemPayload) => ({
          item_id: Number(item.item_id),
          quantity: Number(item.quantity),
          purchased: Boolean(item.purchased),
        })
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
