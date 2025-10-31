import { ComponentFixture, TestBed } from '@angular/core/testing';
import { of } from 'rxjs';

import { GroceryFormComponent } from './grocery-form.component';
import { GroceryService } from '../services/grocery.service';

describe('GroceryFormComponent', () => {
  let component: GroceryFormComponent;
  let fixture: ComponentFixture<GroceryFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GroceryFormComponent],
      providers: [
        {
          provide: GroceryService,
          useValue: {
            getItems: () => of([]),
            addGrocery: () => of({} as any),
          },
        },
      ],
    })
    .compileComponents();

    fixture = TestBed.createComponent(GroceryFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
