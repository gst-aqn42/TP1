import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Event, EventEdition, Article } from '../models/event.model';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private readonly baseUrl = 'http://localhost:5000';

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
  getEditionsByEvent(eventId: string): Observable<EventEdition[]> {
    return this.http.get<EventEdition[]>(`${this.baseUrl}/eventos/${eventId}/edicoes`);
  }

  createEdition(data: Partial<EventEdition>): Observable<EventEdition> {
    return this.http.post<EventEdition>(`${this.baseUrl}/edicoes`, data);
  }

  updateEdition(id: string, data: Partial<EventEdition>): Observable<EventEdition> {
    return this.http.put<EventEdition>(`${this.baseUrl}/edicoes/${id}`, data);
  }

  deleteEdition(id: string): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}/edicoes/${id}`);
  }

  // Artigos
  getArticles(params?: { titulo?: string; autor?: string; evento?: string }): Observable<Article[]> {
    let httpParams = new HttpParams();
    if (params) {
      if (params.titulo) httpParams = httpParams.set('titulo', params.titulo);
      if (params.autor) httpParams = httpParams.set('autor', params.autor);
      if (params.evento) httpParams = httpParams.set('evento', params.evento);
    }
    return this.http.get<Article[]>(`${this.baseUrl}/artigos`, { params: httpParams });
  }

  createArticle(formData: FormData): Observable<Article> {
    return this.http.post<Article>(`${this.baseUrl}/artigos`, formData);
  }

  deleteArticle(id: string): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}/artigos/${id}`);
  }

  uploadBibtex(formData: FormData): Observable<Article[]> {
    return this.http.post<Article[]>(`${this.baseUrl}/artigos/batch`, formData);
  }

  // Inscrições
  subscribeEmail(email: string): Observable<any> {
    return this.http.post(`${this.baseUrl}/inscricoes`, { email });
  }
}
