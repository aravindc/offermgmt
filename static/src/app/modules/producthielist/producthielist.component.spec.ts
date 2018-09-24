import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ProducthielistComponent } from './producthielist.component';

describe('ProducthielistComponent', () => {
  let component: ProducthielistComponent;
  let fixture: ComponentFixture<ProducthielistComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ProducthielistComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ProducthielistComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
