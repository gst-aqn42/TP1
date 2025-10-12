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
    this.uploadProgress = 0;

    // Simula upload com progress
    const formData = new FormData();
    formData.append('bibtex', this.selectedFile);

    // Simula progresso de upload
    const progressInterval = setInterval(() => {
      this.uploadProgress += Math.random() * 20;
      if (this.uploadProgress >= 100) {
        this.uploadProgress = 100;
        clearInterval(progressInterval);

        // Simula finalização do upload
        setTimeout(() => {
          this.isUploading = false;
          this.uploadProgress = 0;
          this.selectedFile = null;

          // Reset do input file
          const fileInput = document.getElementById('bibtex-upload') as HTMLInputElement;
          fileInput.value = '';

          this.snackBar.open('Arquivo BibTeX processado com sucesso! Artigos importados.', 'Fechar', {
            duration: 5000,
            panelClass: ['success-snackbar']
          });
        }, 500);
      }
    }, 200);
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
