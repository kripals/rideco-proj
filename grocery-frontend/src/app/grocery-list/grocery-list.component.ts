import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  FormControl,
  FormGroup,
  NonNullableFormBuilder,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { finalize } from 'rxjs/operators';
import {
  Grocery,
  GroceryItem,
  GroceryItemPayload,
  Item,
} from '../models';
import { GroceryService } from '../services/grocery.service';

type AddItemFormGroup = FormGroup<{
  item_id: FormControl<number>;
  quantity: FormControl<number>;
}>;

@Component({
  selector: 'app-grocery-list',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './grocery-list.component.html',
  styleUrls: ['./grocery-list.component.css'],
})
export class GroceryListComponent implements OnInit {
  groceries: Grocery[] = [];
  loading = false;
  errorMessage = '';
  availableItems: Item[] = [];

  activeAddFor: number | null = null;
  newItemForm: AddItemFormGroup;
  addingItemPending = false;

  private itemBusy = new Set<number>();
  private groceryBusy = new Set<number>();

  constructor(
    private readonly groceryService: GroceryService,
    private readonly fb: NonNullableFormBuilder,
  ) {
    this.newItemForm = this.fb.group({
      item_id: this.fb.control(0, {
        validators: [Validators.required, Validators.min(1)],
      }),
      quantity: this.fb.control(1, {
        validators: [Validators.required, Validators.min(1)],
      }),
    });
  }

  ngOnInit(): void {
    this.loadGroceries();
    this.loadItems();
  }

  loadGroceries(): void {
    this.loading = true;
    this.errorMessage = '';

    this.groceryService.getGroceries().subscribe({
      next: (data) => {
        this.groceries = data;
        this.loading = false;
      },
      error: (err) => {
        console.error('Failed to load groceries', err);
        this.errorMessage = 'Unable to load grocery lists. Please try again later.';
        this.loading = false;
      },
    });
  }

  loadItems(): void {
    this.groceryService.getItems().subscribe({
      next: (data) => (this.availableItems = data),
      error: (err) => console.error('Failed to load items', err),
    });
  }

  trackByGroceryId(_: number, grocery: Grocery): number {
    return grocery.id;
  }

  trackByItemId(_: number, item: GroceryItem): number {
    return item.id;
  }

  isItemProcessing(itemId: number): boolean {
    return this.itemBusy.has(itemId);
  }

  isGroceryProcessing(groceryId: number): boolean {
    return this.groceryBusy.has(groceryId);
  }

  openAddItem(grocery: Grocery): void {
    this.activeAddFor = grocery.id;
    this.newItemForm.reset({ item_id: 0, quantity: 1 });
    this.newItemForm.markAsPristine();
    this.newItemForm.markAsUntouched();
  }

  cancelAddItem(): void {
    this.activeAddFor = null;
    this.addingItemPending = false;
  }

  submitNewItem(grocery: Grocery): void {
    if (this.newItemForm.invalid) {
      this.newItemForm.markAllAsTouched();
      return;
    }

    const value = this.newItemForm.getRawValue();
    const payload: GroceryItemPayload = {
      item_id: Number(value.item_id),
      quantity: Number(value.quantity),
      purchased: false,
    };

    this.errorMessage = '';
    this.addingItemPending = true;
    this.groceryService
      .addItem(grocery.id, payload)
      .pipe(finalize(() => (this.addingItemPending = false)))
      .subscribe({
        next: (created) => {
          grocery.grocery_items = [...grocery.grocery_items, created];
          this.activeAddFor = null;
          this.newItemForm.reset({ item_id: 0, quantity: 1 });
        },
        error: (err) => {
          console.error('Failed to add grocery item', err);
          this.errorMessage =
            'Unable to add the selected item. Please try again.';
        },
      });
  }

  togglePurchased(grocery: Grocery, item: GroceryItem): void {
    if (this.isItemProcessing(item.id)) {
      return;
    }
    this.itemBusy.add(item.id);
    this.errorMessage = '';
    this.groceryService
      .updateGroceryItem(item.id, { purchased: !item.purchased })
      .pipe(finalize(() => this.itemBusy.delete(item.id)))
      .subscribe({
        next: (updated) => {
          this.replaceItemInGrocery(grocery, updated);
        },
        error: (err) => {
          console.error('Failed to update purchased status', err);
          this.errorMessage =
            'Could not update the purchased state. Please retry.';
        },
      });
  }

  changeQuantity(grocery: Grocery, item: GroceryItem, delta: number): void {
    const newQuantity = item.quantity + delta;
    if (newQuantity < 1 || this.isItemProcessing(item.id)) {
      return;
    }
    this.itemBusy.add(item.id);
    this.errorMessage = '';
    this.groceryService
      .updateGroceryItem(item.id, { quantity: newQuantity })
      .pipe(finalize(() => this.itemBusy.delete(item.id)))
      .subscribe({
        next: (updated) => {
          this.replaceItemInGrocery(grocery, updated);
        },
        error: (err) => {
          console.error('Failed to change quantity', err);
          this.errorMessage = 'Unable to change the quantity right now.';
        },
      });
  }

  deleteItem(grocery: Grocery, item: GroceryItem): void {
    if (this.isItemProcessing(item.id)) {
      return;
    }
    if (
      !confirm(
        `Remove ${item.item?.name ?? 'this item'} from grocery list #${grocery.id}?`
      )
    ) {
      return;
    }
    this.itemBusy.add(item.id);
    this.errorMessage = '';
    this.groceryService
      .deleteGroceryItem(item.id)
      .pipe(finalize(() => this.itemBusy.delete(item.id)))
      .subscribe({
        next: () => {
          grocery.grocery_items = grocery.grocery_items.filter(
            (gi) => gi.id !== item.id,
          );
        },
        error: (err) => {
          console.error('Failed to delete grocery item', err);
          this.errorMessage = 'Unable to remove the item. Please try again.';
        },
      });
  }

  deleteGrocery(grocery: Grocery): void {
    if (
      !confirm(
        `Delete grocery list #${grocery.id}? This will remove all of its items.`,
      )
    ) {
      return;
    }
    this.groceryBusy.add(grocery.id);
    this.errorMessage = '';
    this.groceryService
      .deleteGrocery(grocery.id)
      .pipe(finalize(() => this.groceryBusy.delete(grocery.id)))
      .subscribe({
        next: () => {
          this.groceries = this.groceries.filter((g) => g.id !== grocery.id);
        },
        error: (err) => {
          console.error('Failed to delete grocery list', err);
          this.errorMessage =
            'Unable to delete that grocery list. Please try again.';
        },
      });
  }

  getAvailableItemsFor(grocery: Grocery): Item[] {
    const presentIds = new Set(grocery.grocery_items.map((gi) => gi.item_id));
    return this.availableItems.filter((item) => !presentIds.has(item.id));
  }

  private replaceItemInGrocery(grocery: Grocery, updated: GroceryItem): void {
    grocery.grocery_items = grocery.grocery_items.map((gi) =>
      gi.id === updated.id ? updated : gi,
    );
  }
}
