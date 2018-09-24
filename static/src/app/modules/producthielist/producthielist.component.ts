import { Component, OnInit } from '@angular/core';
import { ProducthieService } from './producthie.service';

@Component({
  selector: 'app-producthielist',
  templateUrl: './producthielist.component.html',
  styleUrls: ['./producthielist.component.css']
})
export class ProducthielistComponent implements OnInit {

  public producthie = [];

  constructor(private _producthieService: ProducthieService) { }

  ngOnInit() {
    this._producthieService.getProductHie().subscribe( data => this.producthie = data);
  }

}
