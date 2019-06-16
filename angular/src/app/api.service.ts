import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpResponse } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { tap, catchError } from 'rxjs/operators';
import { Book } from './book.model';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  
  private API_PATH = 'http://localhost:9125'

  private httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*'
    })
  }

  constructor(private http: HttpClient) { }


  Get<T>(path: string): Observable<T> {
    return this.http.get<T>(`${this.API_PATH}${path}`, this.httpOptions)
      .pipe(
        tap(data => console.log('DATA' + (data))),
        catchError(this.handleError<T>('Get'))
      )
  }
 
  private handleError<T> (operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {
 
      // TODO: send the error to remote logging infrastructure
      console.error(error);
 
      // TODO: better job of transforming error for user consumption
      console.log(`${operation} failed: ${error.message}`);
 
      // Let the app keep running by returning an empty result.
      return of(result as T);
    };
  }
}
