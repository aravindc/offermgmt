import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ProductHie } from './producthie';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})

export class ProducthieService {
  productHieData: JSON;
  constructor(private httpClient: HttpClient) {}

  getProductHie(): Observable<ProductHie[]> {
    return this.httpClient.get<ProductHie[]>('http://localhost:5000/hiefulltree');
  }
}
