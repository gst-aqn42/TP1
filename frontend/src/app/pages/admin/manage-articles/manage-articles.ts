import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatTableModule, MatTableDataSource } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatSelectModule } from '@angular/material/select';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatTabsModule } from '@angular/material/tabs';
import { MatCardModule } from '@angular/material/card';
import { MatProgressBarModule } from '@angular/material/progress-bar';
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
    MatTooltipModule,
    MatTabsModule,
    MatCardModule,
    MatProgressBarModule
  ],
  templateUrl: './manage-articles.html',
  styleUrl: './manage-articles.scss'
})
export class ManageArticles implements OnInit {
  displayedColumns: string[] = ['titulo', 'autores', 'edicao', 'ano', 'acoes'];
  dataSource = new MatTableDataSource<Article>([]);
  events: Event[] = [];
  editions: EventEdition[] = [];
  selectedEventId: string = '';
  selectedEditionId: string = '';
  allArticles: Article[] = [];
  
  // Batch upload properties
  selectedTab = 0;
  selectedFile: File | null = null;
  isUploading = false;
  @ViewChild('fileInput') fileInput!: ElementRef;

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
      console.log('⚠️ Nenhum evento selecionado, limpando edições');
      this.editions = [];
      return;
    }

    console.log('🔍 Carregando edições para evento:', this.selectedEventId);
    this.apiService.getEditionsByEvent(this.selectedEventId).subscribe({
      next: (editions: any[]) => {
        console.log('📦 Edições recebidas:', editions);
        
        this.editions = editions.map((e: any) => ({
          id: e._id,
          eventId: e.evento_id,
          year: e.ano,
          numero: e.ano,
          cidadeSede: e.local || 'N/A'
        }));
        
        console.log('📋 Edições mapeadas:', this.editions);
        
        if (this.editions.length > 0) {
          this.selectedEditionId = this.editions[0].id!;
          console.log('✅ Edição selecionada automaticamente:', this.selectedEditionId);
          this.loadArticles();
        } else {
          console.log('⚠️ Nenhuma edição encontrada para este evento');
          this.allArticles = [];
          this.dataSource.data = [];
        }
      },
      error: (err) => {
        console.error('❌ Erro ao carregar edições:', err);
        this.snackBar.open('Erro ao carregar edições', 'Fechar', { duration: 3000 });
      }
    });
  }

  loadArticles(): void {
    if (!this.selectedEditionId) {
      console.log('⚠️ Nenhuma edição selecionada, não pode carregar artigos');
      this.dataSource.data = [];
      return;
    }

    console.log('🔍 Carregando artigos para edição:', this.selectedEditionId);
    this.apiService.getArticlesByEdition(this.selectedEditionId).subscribe({
      next: (articles: any[]) => {
        console.log('📦 Artigos recebidos do backend:', articles);
        
        this.allArticles = articles.map((a: any) => ({
          id: a._id,
          title: a.titulo,
          authors: a.autores?.map((autor: any) => autor.nome || autor) || [],
          eventEditionId: a.edicao_id,
          abstract: a.resumo,
          year: this.editions.find(e => e.id === a.edicao_id)?.year || new Date().getFullYear(),
          keywords: a.keywords || []
        }));
        
        console.log('📊 Artigos mapeados:', this.allArticles);
        console.log(`✅ Total de ${this.allArticles.length} artigos carregados`);
        
        this.filterArticles();
      },
      error: (err) => {
        console.error('❌ Erro ao carregar artigos:', err);
        this.snackBar.open('Erro ao carregar artigos', 'Fechar', { duration: 3000 });
        this.allArticles = [];
        this.filterArticles();
      }
    });
  }

  onEventChange(): void {
    console.log('🔄 Evento mudou para:', this.selectedEventId);
    this.selectedEditionId = '';
    this.loadEditions();
  }

  onEditionChange(): void {
    console.log('🔄 Edição mudou para:', this.selectedEditionId);
    this.loadArticles();
  }

  filterArticles(): void {
    console.log('🔍 Filtrando artigos. Total disponível:', this.allArticles.length);
    this.dataSource.data = this.allArticles;
    console.log('📊 Artigos na tabela após filtro:', this.dataSource.data.length);
  }

  getAvailableEditions(): EventEdition[] {
    if (this.selectedEventId) {
      return this.editions.filter(ed => ed.eventId === this.selectedEventId);
    }
    return this.editions;
  }

  openDialog(): void {
    console.log('🔍 Opening article dialog');
    console.log('📋 Available editions:', this.editions);
    console.log('🎯 Selected edition ID:', this.selectedEditionId);
    
    const dialogRef = this.dialog.open(ArticleDialog, {
      width: '600px',
      data: {
        editions: this.editions,
        selectedEditionId: this.selectedEditionId
      }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        console.log('💾 Dialog result:', result);
        this.createArticle(result);
      }
    });
  }

  createArticle(articleData: any): void {
    console.log('📝 Creating article with data:', articleData);
    
    // Check if it's FormData (with PDF) or plain object (without PDF)
    if (articleData instanceof FormData) {
      console.log('📎 FormData detected, using createArticleWithPdf');
      
      // Verify edicao_id is present
      const editionId = articleData.get('edicao_id');
      console.log('🎯 Edition ID from FormData:', editionId);
      
      if (!editionId) {
        console.error('❌ No edition ID in FormData!');
        this.snackBar.open('Erro: Edição não selecionada', 'Fechar', { duration: 3000 });
        return;
      }
      
      this.apiService.createArticleWithPdf(articleData).subscribe({
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
    } else {
      // Plain object without PDF
      console.log('📄 Plain object detected, using createArticle');
      
      const backendData = {
        titulo: articleData.title,
        autores: articleData.authors.map((name: string) => ({ nome: name })),
        edicao_id: articleData.eventEditionId || this.selectedEditionId,
        resumo: articleData.abstract,
        keywords: articleData.keywords || []
      };

      console.log('🚀 Sending to backend:', backendData);

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

  // ========== BATCH UPLOAD METHODS ==========
  
  triggerFileInput(): void {
    this.fileInput.nativeElement.click();
  }

  onFileSelected(event: any): void {
    const file = event.target.files[0];
    if (file) {
      if (file.name.toLowerCase().endsWith('.bib')) {
        this.selectedFile = file;
      } else {
        this.snackBar.open('Por favor, selecione um arquivo .bib válido.', 'Fechar', {
          duration: 3000
        });
        event.target.value = '';
      }
    }
  }

  removeFile(): void {
    this.selectedFile = null;
    if (this.fileInput) {
      this.fileInput.nativeElement.value = '';
    }
  }

  getFileSize(): string {
    if (!this.selectedFile) return '';
    const bytes = this.selectedFile.size;
    if (bytes < 1024) return bytes + ' bytes';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
  }

  onBatchSubmit(): void {
    if (!this.selectedFile) {
      this.snackBar.open('Por favor, selecione um arquivo BibTeX.', 'Fechar', {
        duration: 3000
      });
      return;
    }

    this.isUploading = true;

    const formData = new FormData();
    formData.append('file', this.selectedFile);

    this.apiService.uploadBibtex(formData).subscribe({
      next: (response: any) => {
        this.isUploading = false;
        
        const stats = response.stats;
        const message = `✅ Upload completo!\n` +
          `📊 ${stats.artigos_criados} artigos criados\n` +
          `📅 ${stats.eventos_criados} eventos criados\n` +
          `📖 ${stats.edicoes_criadas} edições criadas\n` +
          (stats.artigos_duplicados > 0 ? `⚠️ ${stats.artigos_duplicados} duplicados ignorados` : '');
        
        this.snackBar.open(message, 'Fechar', {
          duration: 8000
        });
        
        // Reset e recarrega artigos
        this.removeFile();
        this.selectedTab = 0; // Volta para aba de artigos
        this.loadArticles();
      },
      error: (err) => {
        console.error('Erro no upload:', err);
        this.isUploading = false;
        
        const errorMsg = err.error?.error || 'Erro ao processar arquivo BibTeX';
        this.snackBar.open(`❌ ${errorMsg}`, 'Fechar', {
          duration: 5000
        });
      }
    });
  }
}
