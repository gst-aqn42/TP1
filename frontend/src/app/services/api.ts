import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Event, EventEdition, Article } from '../models/event.model';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private readonly baseUrl = 'http://localhost:5000/api';

  constructor(private http: HttpClient) { }

  // Eventos
  getEvents(): Observable<Event[]> {
    return this.http.get<Event[]>(`${this.baseUrl}/eventos`);
  }

  createEvent(data: Partial<Event>): Observable<Event> {
    return this.http.post<Event>(`${this.baseUrl}/eventos`, data);
  }

  updateEvent(id: string, data: Partial<Event>): Observable<Event> {
    return this.http.put<Event>(`${this.baseUrl}/eventos/${id}`, data);
  }

  deleteEvent(id: string): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}/eventos/${id}`);
  }

  // Edições
  getEditionsByEvent(eventId: string): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/edicoes/evento/${eventId}`);
  }

  createEdition(data: any): Observable<any> {
    return this.http.post<any>(`${this.baseUrl}/edicoes/`, data);
  }

  updateEdition(id: string, data: any): Observable<any> {
    return this.http.put<any>(`${this.baseUrl}/edicoes/${id}`, data);
  }

  deleteEdition(id: string): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}/edicoes/${id}`);
  }

  // Artigos
  getArticlesByEdition(editionId: string): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/artigos/edicao/${editionId}`);
  }

  createArticle(data: any): Observable<any> {
    return this.http.post<any>(`${this.baseUrl}/artigos/`, data);
  }

  createArticleWithPdf(formData: FormData): Observable<any> {
    return this.http.post<any>(`${this.baseUrl}/artigos/`, formData);
  }

  updateArticle(id: string, data: any): Observable<any> {
    return this.http.put<any>(`${this.baseUrl}/artigos/${id}`, data);
  }

  deleteArticle(id: string): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}/artigos/${id}`);
  }

  uploadPdfToArticle(articleId: string, formData: FormData): Observable<any> {
    return this.http.post<any>(`${this.baseUrl}/artigos/${articleId}/upload-pdf`, formData);
  }

  // Batch Upload
  uploadBibtex(formData: FormData): Observable<any> {
    return this.http.post<any>(`${this.baseUrl}/batch/upload-bibtex`, formData);
  }

  // Busca
  searchArticles(query: string, filters?: any): Observable<any[]> {
    let params = new HttpParams().set('q', query);
    
    if (filters) {
      if (filters.autor) params = params.set('autor', filters.autor);
      if (filters.evento) params = params.set('evento', filters.evento);
    }
    
    return this.http.get<any[]>(`${this.baseUrl}/artigos/busca`, { params });
  }

  // Inscrições
  subscribeEmail(email: string): Observable<any> {
    return this.http.post(`${this.baseUrl}/inscricoes`, { email });
  }
}
