import { Injectable } from '@angular/core';
import {
  FormArray,
  FormControl,
  FormGroup,
  NonNullableFormBuilder,
  Validators,
} from '@angular/forms';
import { GroceryFormValue, GroceryItemFormValue } from './grocery';

export type GroceryItemFormGroup = FormGroup<{
  item_id: FormControl<GroceryItemFormValue['item_id']>;
  quantity: FormControl<GroceryItemFormValue['quantity']>;
  purchased: FormControl<GroceryItemFormValue['purchased']>;
}>;

export type GroceryFormGroup = FormGroup<{
  family_id: FormControl<GroceryFormValue['family_id']>;
  grocery_date: FormControl<GroceryFormValue['grocery_date']>;
  grocery_items: FormArray<GroceryItemFormGroup>;
}>;

@Injectable({ providedIn: 'root' })
export class GroceryFormFactory {
  constructor(private fb: NonNullableFormBuilder) {}

  createList(): GroceryFormGroup {
    return this.fb.group({
      family_id: this.fb.control(1, { validators: [Validators.required] }),
      grocery_date: this.fb.control('', { validators: [Validators.required] }),
      grocery_items: this.fb.array<GroceryItemFormGroup>([
        this.createItem(),
      ]),
    });
  }

  createItem(initial?: Partial<GroceryItemFormValue>): GroceryItemFormGroup {
    return this.fb.group({
      item_id: this.fb.control(initial?.item_id ?? 0, {
        validators: [Validators.required, Validators.min(1)],
      }),
      quantity: this.fb.control(initial?.quantity ?? 1, {
        validators: [Validators.required, Validators.min(1)],
      }),
      purchased: this.fb.control(initial?.purchased ?? false),
    });
  }
}
