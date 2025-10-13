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
    
    console.log('📖 Article dialog opened with editions:', this.editions);
    console.log('🎯 Selected edition ID:', (data as any).selectedEditionId);

    this.articleForm = this.fb.group({
      eventEditionId: [(data as any).selectedEditionId || '', Validators.required],
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
    console.log('💾 Saving article, form valid:', this.articleForm.valid);
    console.log('📄 Form values:', this.articleForm.value);
    console.log('📎 Selected file:', this.selectedFile);
    
    if (this.articleForm.valid && this.selectedFile) {
      const formData = new FormData();

      // Get the edition ID
      const editionId = this.articleForm.value.eventEditionId;
      
      // Add titulo (title)
      if (this.articleForm.value.title) {
        formData.append('titulo', this.articleForm.value.title);
      }
      
      // Add autores (authors) as JSON array
      if (this.articleForm.value.authors) {
        const authorsArray = this.articleForm.value.authors
          .split(',')
          .map((author: string) => author.trim());
        formData.append('autores', JSON.stringify(authorsArray));
      }
      
      // Add edicao_id (edition ID) - critical field!
      if (editionId) {
        formData.append('edicao_id', editionId);
        console.log('✅ Added edicao_id to FormData:', editionId);
      } else {
        console.error('❌ No edition ID selected!');
      }
      
      // Add resumo (abstract)
      if (this.articleForm.value.abstract) {
        formData.append('resumo', this.articleForm.value.abstract);
      }
      
      // Add keywords as JSON array
      if (this.articleForm.value.keywords) {
        const keywordsArray = this.articleForm.value.keywords
          .split(',')
          .map((keyword: string) => keyword.trim());
        formData.append('keywords', JSON.stringify(keywordsArray));
      }

      // Add PDF file
      formData.append('pdf', this.selectedFile);

      console.log('✅ Closing dialog with FormData');
      this.dialogRef.close(formData);
    } else {
      if (!this.selectedFile) {
        console.log('❌ No PDF file selected');
        alert('Por favor, selecione um arquivo PDF.');
      } else {
        console.log('❌ Form invalid, errors:', this.articleForm.errors);
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
