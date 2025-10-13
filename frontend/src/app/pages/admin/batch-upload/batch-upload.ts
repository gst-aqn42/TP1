import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { ApiService } from '../../../services/api';

@Component({
  selector: 'app-batch-upload',
  imports: [
    CommonModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatProgressBarModule,
    MatSnackBarModule
  ],
  templateUrl: './batch-upload.html',
  styleUrl: './batch-upload.scss'
})
export class BatchUpload {
  selectedFile: File | null = null;
  isUploading = false;
  uploadProgress = 0;

  constructor(
    private apiService: ApiService,
    private snackBar: MatSnackBar
  ) {}

  onFileSelected(event: any): void {
    const file = event.target.files[0];
    if (file) {
      // Verifica se é um arquivo .bib
      if (file.name.toLowerCase().endsWith('.bib')) {
        this.selectedFile = file;
      } else {
        this.snackBar.open('Por favor, selecione um arquivo .bib válido.', 'Fechar', {
          duration: 3000,
          panelClass: ['error-snackbar']
        });
        event.target.value = '';
      }
    }
  }

  triggerFileInput(): void {
    const fileInput = document.getElementById('bibtex-upload') as HTMLInputElement;
    fileInput.click();
  }

  onSubmit(): void {
    if (!this.selectedFile) {
      this.snackBar.open('Por favor, selecione um arquivo BibTeX.', 'Fechar', {
        duration: 3000,
        panelClass: ['error-snackbar']
      });
      return;
    }

    this.isUploading = true;
    this.uploadProgress = 50; // Mostra progresso inicial

    const formData = new FormData();
    formData.append('file', this.selectedFile);

    this.apiService.uploadBibtex(formData).subscribe({
      next: (response: any) => {
        this.uploadProgress = 100;
        this.isUploading = false;
        
        const stats = response.stats;
        const message = `✅ Upload completo!\n` +
          `📊 ${stats.artigos_criados} artigos criados\n` +
          `📅 ${stats.eventos_criados} eventos criados\n` +
          `📖 ${stats.edicoes_criadas} edições criadas\n` +
          (stats.artigos_duplicados > 0 ? `⚠️ ${stats.artigos_duplicados} duplicados ignorados` : '');
        
        this.snackBar.open(message, 'Fechar', {
          duration: 8000,
          panelClass: ['success-snackbar']
        });
        
        // Reset
        this.selectedFile = null;
        const fileInput = document.getElementById('bibtex-upload') as HTMLInputElement;
        if (fileInput) fileInput.value = '';
      },
      error: (err) => {
        console.error('Erro no upload:', err);
        this.isUploading = false;
        this.uploadProgress = 0;
        
        const errorMsg = err.error?.error || 'Erro ao processar arquivo BibTeX';
        this.snackBar.open(`❌ ${errorMsg}`, 'Fechar', {
          duration: 5000,
          panelClass: ['error-snackbar']
        });
      }
    });
  }

  removeFile(): void {
    this.selectedFile = null;
    const fileInput = document.getElementById('bibtex-upload') as HTMLInputElement;
    fileInput.value = '';
  }

  getFileSize(): string {
    if (!this.selectedFile) return '';
    const bytes = this.selectedFile.size;
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }
}
