import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

export interface Item {
  id: number;
  name: string;
  item_type_id: number;
}

export interface GroceryItemPayload {
  item_id: number;
  quantity: number;
  purchased?: boolean;
}

export interface UpdateGroceryItemPayload {
  item_id?: number;
  quantity?: number;
  purchased?: boolean;
}

export interface CreateGroceryPayload {
  family_id: number;
  grocery_date: string;
  grocery_items: GroceryItemPayload[];
}

export interface GroceryItem {
  id: number;
  grocery_id: number;
  item_id: number;
  quantity: number;
  purchased: boolean;
  created_at: string;
  item?: Item;
}

export interface Grocery {
  id: number;
  family_id: number;
  grocery_date: string;
  created_at: string;
  grocery_items: GroceryItem[];
}

@Injectable({
  providedIn: 'root'
})

export class GroceryService {
  private apiUrl = 'http://localhost:8000/api/v1'; // change if needed

  constructor(private http: HttpClient) {}

  getItems(): Observable<Item[]> {
    return this.http.get<Item[]>(`${this.apiUrl}/items`);
  }

  // Get all groceries
  getGroceries(): Observable<Grocery[]> {
    return this.http.get<Grocery[]>(`${this.apiUrl}/groceries`);
  }

  // Create a new grocery
  addGrocery(grocery: CreateGroceryPayload): Observable<Grocery> {
    return this.http.post<Grocery>(`${this.apiUrl}/groceries`, grocery);
  }

  // Add grocery item to existing grocery
  addItem(groceryId: number, item: GroceryItemPayload): Observable<GroceryItem> {
    return this.http.post<GroceryItem>(`${this.apiUrl}/groceries/${groceryId}/items`, item);
  }

  updateGroceryItem(
    groceryItemId: number,
    changes: UpdateGroceryItemPayload
  ): Observable<GroceryItem> {
    return this.http.patch<GroceryItem>(
      `${this.apiUrl}/grocery_items/${groceryItemId}`,
      changes
    );
  }

  deleteGroceryItem(groceryItemId: number): Observable<void> {
    return this.http
      .delete<{ status: string }>(`${this.apiUrl}/grocery_items/${groceryItemId}`)
      .pipe(map(() => undefined));
  }

  deleteGrocery(groceryId: number): Observable<void> {
    return this.http
      .delete<{ status: string }>(`${this.apiUrl}/groceries/${groceryId}`)
      .pipe(map(() => undefined));
  }
}
