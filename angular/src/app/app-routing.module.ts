import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Routes, RouterModule } from '@angular/router';
import { AdminComponent } from './admin/admin.component';
import { CustomerComponent } from './customer/customer.component';
import { AddBookComponent } from './add-book/add-book.component';

const routes: Routes = [
  { path: 'admin', component: AdminComponent },
  { path: 'customer', component: CustomerComponent },
  { path: 'add', component: AddBookComponent }
];

@NgModule({
  imports: [
    CommonModule,
    RouterModule.forRoot(routes)
  ],
  exports: [
    RouterModule
  ]
})
export class AppRoutingModule { }
