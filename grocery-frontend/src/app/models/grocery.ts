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

export interface GroceryItemFormValue {
  item_id: number;
  quantity: number;
  purchased: boolean;
}

export interface GroceryFormValue {
  family_id: number;
  grocery_date: string;
  grocery_items: GroceryItemFormValue[];
}
