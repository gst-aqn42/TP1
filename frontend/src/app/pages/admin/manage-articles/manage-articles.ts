import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatTableModule, MatTableDataSource } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatSelectModule } from '@angular/material/select';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatTooltipModule } from '@angular/material/tooltip';
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
    MatSnackBarModule,
    MatTooltipModule
  ],
  templateUrl: './manage-articles.html',
  styleUrl: './manage-articles.scss'
})
export class ManageArticles implements OnInit {
  displayedColumns: string[] = ['titulo', 'autores', 'edicao', 'pdf', 'acoes'];
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
  }

  loadEvents(): void {
    this.apiService.getEvents().subscribe({
      next: (response: any) => {
        const events = response.eventos || [];
        this.events = events.map((e: any) => ({
          id: e._id,
          name: e.nome,
          sigla: e.sigla
        }));
        
        if (this.events.length > 0) {
          this.selectedEventId = this.events[0].id!;
          this.loadEditions();
        }
      },
      error: (err) => {
        console.error('Erro ao carregar eventos:', err);
        this.snackBar.open('Erro ao carregar eventos', 'Fechar', { duration: 3000 });
      }
    });
  }

  loadEditions(): void {
    if (!this.selectedEventId) {
      this.editions = [];
      return;
    }

    this.apiService.getEditionsByEvent(this.selectedEventId).subscribe({
      next: (editions: any[]) => {
        this.editions = editions.map((e: any) => ({
          id: e._id,
          eventId: e.evento_id,
          year: e.ano,
          numero: e.ano,
          cidadeSede: e.local || 'N/A'
        }));
        
        if (this.editions.length > 0) {
          this.selectedEditionId = this.editions[0].id!;
          this.loadArticles();
        } else {
          this.allArticles = [];
          this.dataSource.data = [];
        }
      },
      error: (err) => {
        console.error('Erro ao carregar edições:', err);
        this.snackBar.open('Erro ao carregar edições', 'Fechar', { duration: 3000 });
      }
    });
  }

  loadArticles(): void {
    if (!this.selectedEditionId) {
      this.dataSource.data = [];
      return;
    }

    this.apiService.getArticlesByEdition(this.selectedEditionId).subscribe({
      next: (articles: any[]) => {
        this.allArticles = articles.map((a: any) => ({
          id: a._id,
          title: a.titulo,
          authors: a.autores?.map((autor: any) => autor.nome || autor) || [],
          eventEditionId: a.edicao_id,
          abstract: a.resumo,
          year: this.editions.find(e => e.id === a.edicao_id)?.year || new Date().getFullYear(),
          keywords: a.keywords || []
        }));
        this.filterArticles();
      },
      error: (err) => {
        console.error('Erro ao carregar artigos:', err);
        this.snackBar.open('Erro ao carregar artigos', 'Fechar', { duration: 3000 });
        this.allArticles = [];
        this.filterArticles();
      }
    });
  }

  onEventChange(): void {
    this.selectedEditionId = '';
    this.loadEditions();
  }

  onEditionChange(): void {
    this.loadArticles();
  }

  filterArticles(): void {
    this.dataSource.data = this.allArticles;
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
        editions: this.editions,
        selectedEditionId: this.selectedEditionId
      }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.createArticle(result);
      }
    });
  }

  createArticle(articleData: any): void {
    const backendData = {
      titulo: articleData.title,
      autores: articleData.authors.map((name: string) => ({ nome: name })),
      edicao_id: articleData.eventEditionId || this.selectedEditionId,
      resumo: articleData.abstract,
      keywords: articleData.keywords || []
    };

    this.apiService.createArticle(backendData).subscribe({
      next: () => {
        this.snackBar.open('Artigo criado com sucesso!', 'Fechar', {
          duration: 3000,
          panelClass: ['success-snackbar']
        });
        this.loadArticles();
      },
      error: (err) => {
        console.error('Erro ao criar artigo:', err);
        this.snackBar.open('Erro ao criar artigo', 'Fechar', { duration: 3000 });
      }
    });
  }

  deleteArticle(id: string): void {
    const article = this.allArticles.find(a => a.id === id);
    if (article && confirm(`Tem certeza que deseja excluir o artigo "${article.title}"?`)) {
      this.apiService.deleteArticle(id).subscribe({
        next: () => {
          this.snackBar.open('Artigo excluído com sucesso!', 'Fechar', {
            duration: 3000,
            panelClass: ['success-snackbar']
          });
          this.loadArticles();
        },
        error: (err) => {
          console.error('Erro ao excluir artigo:', err);
          this.snackBar.open('Erro ao excluir artigo', 'Fechar', { duration: 3000 });
        }
      });
    }
  }

  editArticle(article: Article): void {
    const dialogRef = this.dialog.open(ArticleDialog, {
      width: '600px',
      data: {
        editions: this.editions,
        selectedEditionId: article.eventEditionId,
        article: article // Passa o artigo para edição
      }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.updateArticle(article.id!, result);
      }
    });
  }

  updateArticle(id: string, articleData: any): void {
    const backendData = {
      titulo: articleData.title,
      autores: articleData.authors.map((name: string) => ({ nome: name })),
      edicao_id: articleData.eventEditionId,
      resumo: articleData.abstract,
      keywords: articleData.keywords || []
    };

    this.apiService.updateArticle(id, backendData).subscribe({
      next: () => {
        this.snackBar.open('Artigo atualizado com sucesso!', 'Fechar', {
          duration: 3000,
          panelClass: ['success-snackbar']
        });
        this.loadArticles();
      },
      error: (err) => {
        console.error('Erro ao atualizar artigo:', err);
        this.snackBar.open('Erro ao atualizar artigo', 'Fechar', { duration: 3000 });
      }
    });
  }

  uploadPdf(articleId: string): void {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.pdf';
    
    input.onchange = (event: any) => {
      const file = event.target.files[0];
      if (file && file.type === 'application/pdf') {
        const formData = new FormData();
        formData.append('pdf', file);
        
        this.apiService.uploadPdfToArticle(articleId, formData).subscribe({
          next: () => {
            this.snackBar.open('PDF enviado com sucesso!', 'Fechar', {
              duration: 3000,
              panelClass: ['success-snackbar']
            });
            this.loadArticles();
          },
          error: (err) => {
            console.error('Erro ao enviar PDF:', err);
            this.snackBar.open('Erro ao enviar PDF', 'Fechar', { duration: 3000 });
          }
        });
      } else {
        this.snackBar.open('Por favor, selecione um arquivo PDF válido', 'Fechar', {
          duration: 3000
        });
      }
    };
    
    input.click();
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
