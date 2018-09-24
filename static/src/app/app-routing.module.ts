import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ProducthielistComponent } from './modules/producthielist/producthielist.component';

const routes: Routes = [
  { path: 'prodhie', component: ProducthielistComponent }
];

@NgModule({
  imports: [ RouterModule.forRoot(routes)],
  exports: [ RouterModule ]
})
export class AppRoutingModule { }
