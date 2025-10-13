import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { ApiService } from '../../services/api';
import { Article } from '../../models/event.model';

@Component({
  selector: 'app-author-page',
  imports: [
    CommonModule,
    RouterLink,
    MatExpansionModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatSnackBarModule
  ],
  templateUrl: './author-page.html',
  styleUrl: './author-page.scss'
})
export class AuthorPage implements OnInit {
  authorName: string = '';
  articlesByYear: Map<number, Article[]> = new Map();
  loading = true;
  totalArticles = 0;
  years: number[] = [];

  constructor(
    private route: ActivatedRoute,
    private apiService: ApiService,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.authorName = decodeURIComponent(params['nome']);
      this.loadAuthorArticles();
    });
  }

  loadAuthorArticles(): void {
    this.loading = true;

    // Simula busca de artigos do autor
    const mockArticles: Article[] = [
      {
        id: '1',
        title: 'Metodologias Ágeis em Engenharia de Software: Uma Revisão Sistemática',
        authors: ['João Silva', 'Maria Santos'],
        abstract: 'Esta pesquisa apresenta uma revisão sistemática sobre metodologias ágeis aplicadas ao desenvolvimento de software moderno.',
        year: 2024,
        pages: '10-25',
        pdfUrl: 'http://example.com/agile-methods-2024.pdf',
        eventEditionId: '1'
      },
      {
        id: '2',
        title: 'Inteligência Artificial no Desenvolvimento de Software',
        authors: ['Ana Costa', 'Carlos Mendes', 'João Silva'],
        abstract: 'Estudo sobre aplicações de IA no ciclo de desenvolvimento de software.',
        year: 2024,
        pages: '26-41',
        pdfUrl: 'http://example.com/ai-development-2024.pdf',
        eventEditionId: '1'
      },
      {
        id: '3',
        title: 'Padrões de Design em Sistemas Distribuídos',
        authors: ['João Silva', 'Roberto Ferreira'],
        abstract: 'Análise de padrões arquiteturais para sistemas distribuídos de larga escala.',
        year: 2023,
        pages: '45-67',
        pdfUrl: 'http://example.com/design-patterns-2023.pdf',
        eventEditionId: '2'
      },
      {
        id: '4',
        title: 'Qualidade de Software em Equipes Remotas',
        authors: ['Maria Santos', 'João Silva'],
        abstract: 'Estudo sobre práticas de qualidade em equipes de desenvolvimento remoto.',
        year: 2023,
        pages: '100-120',
        eventEditionId: '2'
      },
      {
        id: '5',
        title: 'DevOps e Integração Contínua: Melhores Práticas',
        authors: ['João Silva'],
        abstract: 'Guia prático para implementação de pipelines de CI/CD em projetos de software.',
        year: 2022,
        pages: '200-225',
        pdfUrl: 'http://example.com/devops-2022.pdf',
        eventEditionId: '3'
      },
      {
        id: '6',
        title: 'Segurança em Aplicações Web Modernas',
        authors: ['Carlos Mendes', 'João Silva', 'Ana Costa'],
        abstract: 'Análise de vulnerabilidades e práticas de segurança em aplicações web.',
        year: 2022,
        pages: '150-175',
        eventEditionId: '3'
      }
    ];

    // Filtra artigos que contêm o nome do autor
    const authorArticles = mockArticles.filter(article =>
      article.authors.some(author =>
        author.toLowerCase().includes(this.authorName.toLowerCase())
      )
    );

    // Agrupa artigos por ano
    this.articlesByYear.clear();
    authorArticles.forEach(article => {
      const year = article.year || new Date().getFullYear();
      if (!this.articlesByYear.has(year)) {
        this.articlesByYear.set(year, []);
      }
      this.articlesByYear.get(year)!.push(article);
    });

    // Ordena anos em ordem decrescente
    this.years = Array.from(this.articlesByYear.keys()).sort((a, b) => b - a);
    this.totalArticles = authorArticles.length;

    this.loading = false;
  }

  openPdf(pdfUrl: string): void {
    if (pdfUrl) {
      window.open(pdfUrl, '_blank');
    } else {
      this.snackBar.open('PDF não disponível para este artigo.', 'Fechar', {
        duration: 3000
      });
    }
  }

  getEventInfo(article: Article): string {
    // Simula busca de informações do evento
    const eventMap: { [key: string]: { name: string, year: number } } = {
      '1': { name: 'SBES', year: 2024 },
      '2': { name: 'SBES', year: 2023 },
      '3': { name: 'CBS', year: 2022 }
    };

    const eventInfo = eventMap[article.eventEditionId || ''];
    return eventInfo ? `${eventInfo.name} ${eventInfo.year}` : `${article.year}`;
  }

  getFormattedAuthorName(): string {
    return this.authorName.split('-').map(word =>
      word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
  }
}
