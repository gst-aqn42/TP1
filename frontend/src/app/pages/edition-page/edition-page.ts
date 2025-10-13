import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatTableModule } from '@angular/material/table';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { ApiService } from '../../services/api';
import { Event, EventEdition, Article } from '../../models/event.model';

@Component({
  selector: 'app-edition-page',
  imports: [
    CommonModule,
    RouterLink,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatTableModule,
    MatSnackBarModule
  ],
  templateUrl: './edition-page.html',
  styleUrl: './edition-page.scss'
})
export class EditionPage implements OnInit {
  event: Event | null = null;
  edition: EventEdition | null = null;
  articles: Article[] = [];
  loading = true;
  eventSigla: string = '';
  editionYear: number = 0;

  constructor(
    private route: ActivatedRoute,
    private apiService: ApiService,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.eventSigla = params['sigla'];
      this.editionYear = parseInt(params['ano']);
      this.loadEditionDetails();
    });
  }

  loadEditionDetails(): void {
    this.loading = true;

    // Simula busca do evento
    const mockEvents: Event[] = [
      {
        id: '1',
        name: 'Simpósio Brasileiro de Engenharia de Software',
        sigla: 'SBES'
      },
      {
        id: '2',
        name: 'Conferência Brasileira de Software',
        sigla: 'CBS'
      }
    ];

    this.event = mockEvents.find(e =>
      e.sigla?.toLowerCase() === this.eventSigla.toLowerCase()
    ) || null;

    if (this.event) {
      this.loadEdition();
    } else {
      this.loading = false;
    }
  }

  loadEdition(): void {
    if (!this.event) return;

    // Simula busca da edição específica
    const mockEditions: EventEdition[] = [
      {
        id: '1',
        eventId: '1',
        year: 2024,
        numero: 37,
        cidadeSede: 'Curitiba',
        description: '37ª edição do SBES realizada em Curitiba'
      },
      {
        id: '2',
        eventId: '1',
        year: 2023,
        numero: 36,
        cidadeSede: 'Campo Grande',
        description: '36ª edição do SBES realizada em Campo Grande'
      },
      {
        id: '3',
        eventId: '2',
        year: 2024,
        numero: 15,
        cidadeSede: 'São Paulo',
        description: '15ª edição da CBS realizada em São Paulo'
      }
    ];

    this.edition = mockEditions.find(ed =>
      ed.eventId === this.event!.id && ed.year === this.editionYear
    ) || null;

    if (this.edition) {
      this.loadArticles();
    } else {
      this.loading = false;
    }
  }

  loadArticles(): void {
    if (!this.edition) return;

    // Simula busca dos artigos da edição
    const mockArticles: Article[] = [
      {
        id: '1',
        title: 'Metodologias Ágeis em Engenharia de Software: Uma Revisão Sistemática',
        authors: ['João Silva', 'Maria Santos'],
        abstract: 'Esta pesquisa apresenta uma revisão sistemática sobre metodologias ágeis...',
        eventEditionId: '1',
        year: 2024,
        pages: '10-25',
        pdfUrl: 'http://example.com/agile-methods.pdf'
      },
      {
        id: '2',
        title: 'Inteligência Artificial no Desenvolvimento de Software',
        authors: ['Ana Costa', 'Carlos Mendes'],
        abstract: 'Estudo sobre aplicações de IA no ciclo de desenvolvimento...',
        eventEditionId: '1',
        year: 2024,
        pages: '26-41',
        pdfUrl: 'http://example.com/ai-development.pdf'
      },
      {
        id: '3',
        title: 'Qualidade de Software em Projetos Distribuídos',
        authors: ['Pedro Oliveira', 'Lucia Ferreira'],
        abstract: 'Análise de práticas de qualidade em equipes distribuídas...',
        eventEditionId: '2',
        year: 2023,
        pages: '15-30'
      },
      {
        id: '4',
        title: 'Arquitetura de Microsserviços: Padrões e Práticas',
        authors: ['Roberto Santos', 'Ana Silva'],
        abstract: 'Guia prático para implementação de arquiteturas de microsserviços...',
        eventEditionId: '3',
        year: 2024,
        pages: '42-58',
        pdfUrl: 'http://example.com/microservices.pdf'
      }
    ];

    this.articles = mockArticles.filter(article =>
      article.eventEditionId === this.edition!.id
    );

    this.loading = false;
  }

  openPdf(articleId: string): void {
    if (articleId) {
      window.open(`http://localhost:5000/api/artigos/${articleId}/pdf`, '_blank');
    } else {
      this.snackBar.open('PDF não disponível para este artigo.', 'Fechar', {
        duration: 3000
      });
    }
  }
}
