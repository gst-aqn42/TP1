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
  allArticles: Article[] = [];

  constructor(
    private fb: FormBuilder,
    private apiService: ApiService,
    private snackBar: MatSnackBar
  ) {
    this.searchForm = this.fb.group({
      searchTerm: ['']
    });

    // Carrega todos os artigos ao inicializar o componente
    this.loadAllArticles();
  }

  ngOnInit(): void {
    this.loadAllArticles();
  }

  private loadAllArticles(): void {
    // Simula todos os artigos disponíveis
    this.allArticles = [
      {
        id: '1',
        title: 'Metodologias Ágeis em Engenharia de Software',
        authors: ['João Silva', 'Maria Santos'],
        abstract: 'Este artigo apresenta uma análise das metodologias ágeis aplicadas ao desenvolvimento de software...',
        year: 2024,
        pages: '10-20',
        pdfUrl: 'http://example.com/agile-methods.pdf',
        eventEditionId: '1'
      },
      {
        id: '2',
        title: 'Qualidade de Software em Projetos Distribuídos',
        authors: ['Pedro Oliveira'],
        abstract: 'Estudo sobre garantia de qualidade em equipes de desenvolvimento distribuídas...',
        year: 2023,
        pages: '45-67',
        pdfUrl: 'http://example.com/quality-distributed.pdf',
        eventEditionId: '2'
      },
      {
        id: '3',
        title: 'Inteligência Artificial no Desenvolvimento de Software',
        authors: ['Ana Costa', 'Carlos Mendes', 'João Silva'],
        abstract: 'Aplicações de IA no ciclo de desenvolvimento de software moderno...',
        year: 2024,
        pages: '100-115',
        pdfUrl: 'http://example.com/ai-development.pdf',
        eventEditionId: '1'
      },
      {
        id: '4',
        title: 'Arquitetura de Microsserviços: Boas Práticas',
        authors: ['Roberto Ferreira', 'Maria Santos'],
        abstract: 'Guia prático para implementação de arquiteturas baseadas em microsserviços...',
        year: 2023,
        pages: '200-220',
        eventEditionId: '3'
      },
      {
        id: '5',
        title: 'DevOps e Integração Contínua',
        authors: ['Lucas Almeida', 'Sandra Silva'],
        abstract: 'Estratégias de DevOps para melhorar a entrega de software...',
        year: 2024,
        pages: '78-95',
        pdfUrl: 'http://example.com/devops-ci.pdf',
        eventEditionId: '2'
      },
      {
        id: '6',
        title: 'Testes Automatizados em Aplicações Web',
        authors: ['Marcos Pereira'],
        abstract: 'Técnicas e ferramentas para automação de testes em aplicações web...',
        year: 2023,
        pages: '156-178',
        pdfUrl: 'http://example.com/automated-tests.pdf',
        eventEditionId: '1'
      },
      {
        id: '7',
        title: 'Segurança em Aplicações Mobile',
        authors: ['Patricia Lima', 'Fernando Costa'],
        abstract: 'Principais vulnerabilidades e práticas de segurança em apps móveis...',
        year: 2024,
        pages: '230-250',
        pdfUrl: 'http://example.com/mobile-security.pdf',
        eventEditionId: '3'
      },
      {
        id: '8',
        title: 'Machine Learning aplicado à Engenharia de Software',
        authors: ['Rafael Santos', 'Ana Costa'],
        abstract: 'Como ML pode auxiliar no desenvolvimento e manutenção de software...',
        year: 2024,
        pages: '300-320',
        pdfUrl: 'http://example.com/ml-software-eng.pdf',
        eventEditionId: '2'
      }
    ];

    // Exibe todos os artigos inicialmente
    this.searchResults = [...this.allArticles];
  }

  onSearch(): void {
    const { searchTerm } = this.searchForm.value;

    if (!searchTerm || searchTerm.trim() === '') {
      this.snackBar.open('Por favor, insira um termo de busca.', 'Fechar', { duration: 3000 });
      return;
    }

    // Simula busca em todos os campos
    this.simulateSearch(searchTerm.trim());
  }

  private simulateSearch(searchTerm: string): void {
    this.searchPerformed = true;

    // Filtra resultados baseado na busca em todos os campos
    this.searchResults = this.allArticles.filter(article => {
      const term = searchTerm.toLowerCase();

      // Busca no título
      const titleMatch = article.title.toLowerCase().includes(term);

      // Busca nos autores
      const authorMatch = article.authors.some(author =>
        author.toLowerCase().includes(term)
      );

      // Busca no evento (simula busca por nome do evento)
      const eventMatch = 
        (article.eventEditionId === '1' && (term.includes('sbes') || term.includes('simpósio brasileiro'))) ||
        (article.eventEditionId === '2' && (term.includes('cbs') || term.includes('conferência brasileira'))) ||
        (article.eventEditionId === '3' && (term.includes('wts') || term.includes('workshop'))) ||
        term.includes('software') || term.includes('engenharia');

      // Busca no abstract
      const abstractMatch = article.abstract?.toLowerCase().includes(term) || false;

      // Retorna true se encontrou match em qualquer campo
      return titleMatch || authorMatch || eventMatch || abstractMatch;
    });

    this.snackBar.open(
      `Busca realizada! ${this.searchResults.length} resultado(s) encontrado(s).`,
      'Fechar',
      { duration: 3000 }
    );
  }

  clearSearch(): void {
    this.searchForm.reset();
    this.searchResults = [...this.allArticles];
    this.searchPerformed = false;
  }

  getEventAndYear(article: Article): string {
    // Simula busca de informações do evento
    const eventMap: { [key: string]: { name: string, year: number } } = {
      '1': { name: 'SBES', year: 2024 },
      '2': { name: 'SBES', year: 2023 },
      '3': { name: 'CBS', year: 2024 }
    };

    const eventInfo = eventMap[article.eventEditionId || ''];
    return eventInfo ? `${eventInfo.name} ${eventInfo.year}` : `${article.year}`;
  }

  openPdf(pdfUrl: string): void {
    if (pdfUrl) {
      window.open(pdfUrl, '_blank');
    } else {
      this.snackBar.open('PDF não disponível para este artigo.', 'Fechar', { duration: 3000 });
    }
  }
}
