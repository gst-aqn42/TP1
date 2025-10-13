import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatTableModule, MatTableDataSource } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatSelectModule } from '@angular/material/select';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../../services/api';
import { Event, EventEdition, Article } from '../../../models/event.model';
import { ArticleDialog } from '../../../components/dialogs/article-dialog/article-dialog';

@Component({
  selector: 'app-manage-articles',
  imports: [
    CommonModule,
    FormsModule,
    MatTableModule,
    MatButtonModule,
    MatIconModule,
    MatSelectModule,
    MatFormFieldModule,
    MatDialogModule,
    MatSnackBarModule
  ],
  templateUrl: './manage-articles.html',
  styleUrl: './manage-articles.scss'
})
export class ManageArticles implements OnInit {
  displayedColumns: string[] = ['titulo', 'autores', 'edicao', 'acoes'];
  dataSource = new MatTableDataSource<Article>([]);
  events: Event[] = [];
  editions: EventEdition[] = [];
  selectedEventId: string = '';
  selectedEditionId: string = '';
  allArticles: Article[] = [];

  constructor(
    private apiService: ApiService,
    private dialog: MatDialog,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.loadEvents();
    this.loadEditions();
    this.loadArticles();
  }

  loadEvents(): void {
    this.events = [
      { id: '1', name: 'Simpósio Brasileiro de Engenharia de Software', sigla: 'SBES' },
      { id: '2', name: 'Conferência Brasileira de Software', sigla: 'CBS' }
    ];
  }

  loadEditions(): void {
    this.editions = [
      {
        id: '1',
        eventId: '1',
        year: 2024,
        numero: 37,
        cidadeSede: 'Curitiba'
      },
      {
        id: '2',
        eventId: '1',
        year: 2023,
        numero: 36,
        cidadeSede: 'Campo Grande'
      },
      {
        id: '3',
        eventId: '2',
        year: 2024,
        numero: 15,
        cidadeSede: 'São Paulo'
      }
    ];
  }

  loadArticles(): void {
    this.allArticles = [
      {
        id: '1',
        title: 'Metodologias Ágeis na Engenharia de Software',
        authors: ['João Silva', 'Maria Santos'],
        eventEditionId: '1',
        abstract: 'Este artigo apresenta uma análise das metodologias ágeis...',
        year: 2024,
        pages: '10-20'
      },
      {
        id: '2',
        title: 'Qualidade de Software em Projetos Distribuídos',
        authors: ['Pedro Oliveira'],
        eventEditionId: '2',
        abstract: 'Estudo sobre garantia de qualidade em equipes distribuídas...',
        year: 2023,
        pages: '45-60'
      },
      {
        id: '3',
        title: 'Inteligência Artificial no Desenvolvimento de Software',
        authors: ['Ana Costa', 'Carlos Mendes'],
        eventEditionId: '3',
        abstract: 'Aplicações de IA no ciclo de desenvolvimento...',
        year: 2024,
        pages: '100-115'
      }
    ];

    this.filterArticles();
  }

  onEventChange(): void {
    this.selectedEditionId = '';
    this.filterArticles();
  }

  onEditionChange(): void {
    this.filterArticles();
  }

  filterArticles(): void {
    let filteredArticles = this.allArticles;

    if (this.selectedEventId) {
      const eventEditions = this.editions.filter(ed => ed.eventId === this.selectedEventId);
      const eventEditionIds = eventEditions.map(ed => ed.id);
      filteredArticles = filteredArticles.filter(article =>
        eventEditionIds.includes(article.eventEditionId!)
      );
    }

    if (this.selectedEditionId) {
      filteredArticles = filteredArticles.filter(article =>
        article.eventEditionId === this.selectedEditionId
      );
    }

    this.dataSource.data = filteredArticles;
  }

  getAvailableEditions(): EventEdition[] {
    if (this.selectedEventId) {
      return this.editions.filter(ed => ed.eventId === this.selectedEventId);
    }
    return this.editions;
  }

  openDialog(): void {
    const dialogRef = this.dialog.open(ArticleDialog, {
      width: '600px',
      data: {
        editions: this.editions
      }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.createArticle(result);
      }
    });
  }

  createArticle(formData: FormData): void {
    // Simula criação de artigo
    const newArticle: Article = {
      id: Math.random().toString(),
      title: formData.get('title') as string,
      authors: JSON.parse(formData.get('authors') as string || '[]'),
      eventEditionId: formData.get('eventEditionId') as string,
      abstract: formData.get('abstract') as string,
      keywords: JSON.parse(formData.get('keywords') as string || '[]'),
      pages: formData.get('pages') as string,
      doi: formData.get('doi') as string,
      year: new Date().getFullYear()
    };

    this.allArticles.push(newArticle);
    this.filterArticles();

    this.snackBar.open('Artigo criado com sucesso!', 'Fechar', {
      duration: 3000,
      panelClass: ['success-snackbar']
    });
  }

  deleteArticle(id: string): void {
    const article = this.allArticles.find(a => a.id === id);
    if (article && confirm(`Tem certeza que deseja excluir o artigo "${article.title}"?`)) {
      this.allArticles = this.allArticles.filter(a => a.id !== id);
      this.filterArticles();
      this.snackBar.open('Artigo excluído com sucesso!', 'Fechar', {
        duration: 3000,
        panelClass: ['success-snackbar']
      });
    }
  }

  getEditionInfo(editionId: string): string {
    const edition = this.editions.find(e => e.id === editionId);
    if (edition) {
      const event = this.events.find(ev => ev.id === edition.eventId);
      return `${event?.sigla} ${edition.year} - Ed. ${edition.numero}`;
    }
    return 'Edição não encontrada';
  }
}
