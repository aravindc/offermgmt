import { TestBed } from '@angular/core/testing';

import { ProducthieService } from './producthie.service';

describe('ProducthieService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: ProducthieService = TestBed.get(ProducthieService);
    expect(service).toBeTruthy();
  });
});
