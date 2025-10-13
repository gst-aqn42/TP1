import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';

import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { ApiService } from '../../services/api';
import { Article } from '../../models/event.model';

@Component({
  selector: 'app-search-page',
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatIconModule,
    MatSnackBarModule
  ],
  templateUrl: './search-page.html',
  styleUrl: './search-page.scss'
})
export class SearchPage implements OnInit {
  searchForm: FormGroup;
  searchResults: Article[] = [];
  searchPerformed = false;
  isLoading = false;

  constructor(
    private fb: FormBuilder,
    private apiService: ApiService,
    private snackBar: MatSnackBar
  ) {
    this.searchForm = this.fb.group({
      searchTerm: [''],
      authorFilter: [''],
      eventFilter: ['']
    });
  }

  ngOnInit(): void {
    // Não carrega nada inicialmente - usuário deve fazer busca
  }

  onSearch(): void {
    const { searchTerm, authorFilter, eventFilter } = this.searchForm.value;

    if (!searchTerm || searchTerm.trim() === '') {
      this.snackBar.open('Por favor, insira um termo de busca.', 'Fechar', { duration: 3000 });
      return;
    }

    this.isLoading = true;
    this.searchPerformed = true;

    // Preparar filtros
    const filters: any = {};
    if (authorFilter && authorFilter.trim()) {
      filters.autor = authorFilter.trim();
    }
    if (eventFilter && eventFilter.trim()) {
      filters.evento = eventFilter.trim();
    }

    // Chamar API de busca
    this.apiService.searchArticles(searchTerm.trim(), filters).subscribe({
      next: (response: any) => {
        // Backend retorna { resultados: [...], total: X }
        const results = response.resultados || response || [];
        
        // Mapear resultados do backend para o modelo frontend
        this.searchResults = results.map((a: any) => ({
          id: a._id,
          title: a.titulo,
          authors: a.autores?.map((autor: any) => autor.nome || autor) || [],
          abstract: a.resumo,
          year: a.edicao_ano || a.ano || new Date().getFullYear(),
          eventEditionId: a.edicao_id,
          pdfUrl: a.pdf_path || '',
          keywords: a.keywords || [],
          eventName: a.evento_nome,
          eventSigla: a.evento_sigla
        }));

        this.isLoading = false;
        this.snackBar.open(
          `Busca realizada! ${this.searchResults.length} resultado(s) encontrado(s).`,
          'Fechar',
          { duration: 3000, panelClass: ['success-snackbar'] }
        );
      },
      error: (err) => {
        console.error('Erro na busca:', err);
        this.isLoading = false;
        this.searchResults = [];
        this.snackBar.open('Erro ao realizar busca', 'Fechar', { 
          duration: 3000,
          panelClass: ['error-snackbar']
        });
      }
    });
  }

  clearSearch(): void {
    this.searchForm.reset();
    this.searchResults = [];
    this.searchPerformed = false;
  }

  getEventAndYear(article: Article): string {
    // Usa informações enriquecidas do backend
    const eventSigla = (article as any).eventSigla || '';
    const year = article.year || '';
    
    if (eventSigla && year) {
      return `${eventSigla} ${year}`;
    } else if (year) {
      return `${year}`;
    } else if (eventSigla) {
      return eventSigla;
    }
    
    return 'Informação não disponível';
  }

  openPdf(pdfUrl: string): void {
    if (pdfUrl) {
      window.open(pdfUrl, '_blank');
    } else {
      this.snackBar.open('PDF não disponível para este artigo.', 'Fechar', { duration: 3000 });
    }
  }
}
