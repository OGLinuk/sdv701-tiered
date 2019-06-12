import { Component, OnInit } from '@angular/core';
import { ApiService } from '../api.service';
import { Book } from '../book';

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
    console.log(this.books);
  }

  getBooks(): void {
    this.apiService.Get<Book[]>("/books")
      .subscribe(data => this.books = data);
  }

}
