import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { ApiService } from '../../services/api';

@Component({
  selector: 'app-subscribe-form',
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatSnackBarModule
  ],
  templateUrl: './subscribe-form.html',
  styleUrl: './subscribe-form.scss'
})
export class SubscribeForm {
  subscribeForm: FormGroup;
  isSubmitting = false;

  constructor(
    private fb: FormBuilder,
    private apiService: ApiService,
    private snackBar: MatSnackBar
  ) {
    this.subscribeForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]]
    });
  }

  onSubmit(): void {
    if (this.subscribeForm.valid) {
      this.isSubmitting = true;
      const email = this.subscribeForm.value.email;

      // Simula chamada para API com delay
      setTimeout(() => {
        // Simula sucesso da inscrição
        this.apiService.subscribeEmail(email).subscribe({
          next: () => {
            this.snackBar.open(
              'Inscrição realizada com sucesso! Você receberá notificações sobre novos artigos.',
              'Fechar',
              {
                duration: 5000,
                panelClass: ['success-snackbar']
              }
            );
            this.subscribeForm.reset();
          },
          error: () => {
            this.snackBar.open(
              'Erro ao realizar inscrição. Tente novamente.',
              'Fechar',
              {
                duration: 3000,
                panelClass: ['error-snackbar']
              }
            );
          },
          complete: () => {
            this.isSubmitting = false;
          }
        });
      }, 1000);

    } else {
      this.markFormGroupTouched();
    }
  }

  private markFormGroupTouched(): void {
    Object.keys(this.subscribeForm.controls).forEach(key => {
      const control = this.subscribeForm.get(key);
      control?.markAsTouched();
    });
  }

  getErrorMessage(): string {
    const emailControl = this.subscribeForm.get('email');
    if (emailControl?.hasError('required')) {
      return 'Email é obrigatório';
    }
    if (emailControl?.hasError('email')) {
      return 'Digite um email válido';
    }
    return '';
  }
}
