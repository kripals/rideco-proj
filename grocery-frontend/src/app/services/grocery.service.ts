import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { environment } from '../../environments/environment';
import {
  CreateGroceryPayload,
  Grocery,
  GroceryItem,
  GroceryItemPayload,
  Item,
  UpdateGroceryItemPayload,
} from '../models';

@Injectable({ providedIn: 'root' })
export class GroceryService {
  private readonly apiUrl = environment.apiUrl;

  constructor(private readonly http: HttpClient) {}

  getItems(): Observable<Item[]> {
    return this.http.get<Item[]>(`${this.apiUrl}/items`);
  }

  getGroceries(): Observable<Grocery[]> {
    return this.http.get<Grocery[]>(`${this.apiUrl}/groceries`);
  }

  addGrocery(grocery: CreateGroceryPayload): Observable<Grocery> {
    return this.http.post<Grocery>(`${this.apiUrl}/groceries`, grocery);
  }

  addItem(groceryId: number, item: GroceryItemPayload): Observable<GroceryItem> {
    return this.http.post<GroceryItem>(`${this.apiUrl}/groceries/${groceryId}/items`, item);
  }

  updateGroceryItem(
    groceryItemId: number,
    changes: UpdateGroceryItemPayload,
  ): Observable<GroceryItem> {
    return this.http.patch<GroceryItem>(
      `${this.apiUrl}/grocery_items/${groceryItemId}`,
      changes,
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
