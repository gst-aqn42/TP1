import { Component, OnInit } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { ApiService } from '../../services/api';
import { Article, Event } from '../../models/event.model';

@Component({
  selector: 'app-home',
  imports: [RouterLink, CommonModule, MatCardModule, MatButtonModule, MatIconModule],
  templateUrl: './home.html',
  styleUrl: './home.scss'
})
export class Home implements OnInit {
  topArticles: Article[] = [];
  topEvents: Event[] = [];
  loading = true;

  constructor(
    private apiService: ApiService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.loadTopArticles();
    this.loadTopEvents();
  }

  private loadTopArticles(): void {
    this.apiService.searchArticles('software').subscribe({
      next: (response: any) => {
        const results = response.resultados || [];
        const allArticles = results.map((a: any) => ({
          id: a._id,
          title: a.titulo,
          authors: a.autores?.map((autor: any) => autor.nome || autor) || [],
          abstract: a.resumo || 'Sem resumo disponível',
          year: a.edicao_ano || new Date().getFullYear(),
          eventEditionId: a.edicao_id,
          pdfUrl: a.pdf_path,
          keywords: a.keywords || []
        }));
        this.topArticles = allArticles.slice(0, 5);
      },
      error: (err) => {
        console.error('Erro ao carregar artigos:', err);
        this.topArticles = [];
      }
    });
  }

  private loadTopEvents(): void {
    this.apiService.getEvents().subscribe({
      next: (response: any) => {
        const events = response.eventos || [];
        this.topEvents = events.map((e: any) => ({
          id: e._id,
          name: e.nome,
          sigla: e.sigla,
          description: e.descricao || 'Sem descrição disponível',
          editions: []
        })).slice(0, 5);
        this.loading = false;
      },
      error: (err) => {
        console.error('Erro ao carregar eventos:', err);
        this.topEvents = [];
        this.loading = false;
      }
    });
  }

  navigateToEvent(eventId: string, sigla: string): void {
    this.router.navigate(['/event', sigla]);
  }

  openPdf(articleId: string): void {
    if (articleId) {
      window.open(`http://localhost:5000/api/artigos/${articleId}/pdf`, '_blank');
    }
  }
}
