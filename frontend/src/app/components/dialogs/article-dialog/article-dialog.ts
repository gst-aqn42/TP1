import { Component, Inject, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialogModule } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { CommonModule } from '@angular/common';
import { EventEdition } from '../../../models/event.model';

interface ArticleDialogData {
  editions: EventEdition[];
}

@Component({
  selector: 'app-article-dialog',
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatDialogModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatButtonModule,
    MatIconModule
  ],
  templateUrl: './article-dialog.html',
  styleUrl: './article-dialog.scss'
})
export class ArticleDialog implements OnInit {
  articleForm: FormGroup;
  editions: EventEdition[];
  selectedFile: File | null = null;

  constructor(
    private fb: FormBuilder,
    private dialogRef: MatDialogRef<ArticleDialog>,
    @Inject(MAT_DIALOG_DATA) public data: ArticleDialogData
  ) {
    this.editions = data.editions;

    this.articleForm = this.fb.group({
      eventEditionId: ['', Validators.required],
      title: ['', Validators.required],
      authors: ['', Validators.required],
      abstract: [''],
      keywords: [''],
      pages: [''],
      doi: ['']
    });
  }

  ngOnInit(): void {}

  onFileSelected(event: any): void {
    const file = event.target.files[0];
    if (file && file.type === 'application/pdf') {
      this.selectedFile = file;
    } else {
      alert('Por favor, selecione um arquivo PDF válido.');
      event.target.value = '';
    }
  }

  onSave(): void {
    if (this.articleForm.valid && this.selectedFile) {
      const formData = new FormData();

      // Adiciona todos os campos do formulário
      Object.keys(this.articleForm.value).forEach(key => {
        const value = this.articleForm.value[key];
        if (value) {
          if (key === 'authors') {
            // Converte string de autores em array
            formData.append(key, JSON.stringify(value.split(',').map((author: string) => author.trim())));
          } else if (key === 'keywords') {
            // Converte string de keywords em array
            formData.append(key, JSON.stringify(value.split(',').map((keyword: string) => keyword.trim())));
          } else {
            formData.append(key, value);
          }
        }
      });

      // Adiciona o arquivo PDF
      formData.append('pdf', this.selectedFile);

      this.dialogRef.close(formData);
    } else {
      if (!this.selectedFile) {
        alert('Por favor, selecione um arquivo PDF.');
      }
    }
  }

  onCancel(): void {
    this.dialogRef.close();
  }

  getEditionLabel(edition: EventEdition): string {
    return `${edition.year} - Edição ${edition.numero} (${edition.cidadeSede})`;
  }
}
