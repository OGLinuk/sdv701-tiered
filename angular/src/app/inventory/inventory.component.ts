import { Component, OnInit } from '@angular/core';
import { ApiService } from '../api.service';
import { Book } from '../book.model';
import { getLocaleDateTimeFormat } from '@angular/common';

@Component({
  selector: 'app-inventory',
  templateUrl: './inventory.component.html',
  styleUrls: ['./inventory.component.css']
})
export class InventoryComponent implements OnInit {

  books: Book[];

  constructor(private apiService: ApiService) { }

  ngOnInit() {
    this.getBooks();
  }
  
  getBooks(): void {
    this.apiService.Get<Book[]>("/books")
      .subscribe(data => this.books = JSON.parse(data['books']));
  }

  put(name: string, type: string, 
      genre: Int8Array, description: string, 
      price: Float64Array, in_stock: Int32Array, 
      condition: Int8Array): void {
    let book = new Book(name, type, genre, description, price, in_stock, "", condition);
    console.log('BOOK: ', book);
    let route = `/book/${book.name}`;
    this.apiService.Put(route, book)
      .subscribe(data => this.books.push(book));
  }
  
}
