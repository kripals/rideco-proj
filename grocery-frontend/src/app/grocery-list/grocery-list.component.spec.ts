import { ComponentFixture, TestBed } from '@angular/core/testing';
import { of } from 'rxjs';
import { GroceryListComponent } from './grocery-list.component';
import { GroceryService } from '../services/grocery.service';

describe('GroceryListComponent', () => {
  let component: GroceryListComponent;
  let fixture: ComponentFixture<GroceryListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GroceryListComponent],
      providers: [
        {
          provide: GroceryService,
          useValue: {
            getGroceries: () => of([]),
            getItems: () => of([]),
            addItem: () => of({} as any),
            updateGroceryItem: () => of({} as any),
            deleteGroceryItem: () => of(undefined),
            deleteGrocery: () => of(undefined),
          },
        },
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(GroceryListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
