import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { AuthService } from '../../../services/auth';

@Component({
  selector: 'app-login-page',
  imports: [
    ReactiveFormsModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatSnackBarModule
  ],
  templateUrl: './login-page.html',
  styleUrl: './login-page.scss'
})
export class LoginPage {
  loginForm: FormGroup;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router,
    private snackBar: MatSnackBar
  ) {
    this.loginForm = this.fb.group({
      username: ['', Validators.required],
      password: ['', Validators.required]
    });
  }

  onSubmit(): void {
    if (this.loginForm.valid) {
      const credentials = {
        username: this.loginForm.value.username,
        password: this.loginForm.value.password
      };

      // Usar API real de autenticação
      this.authService.login(credentials).subscribe({
        next: (response: any) => {
          console.log('Login bem-sucedido:', response);
          
          this.snackBar.open('Login realizado com sucesso!', 'Fechar', {
            duration: 3000,
            panelClass: ['success-snackbar']
          });
          
          // Redirecionar para admin
          setTimeout(() => {
            this.router.navigate(['/admin/eventos']);
          }, 500);
        },
        error: (err) => {
          console.error('Erro no login:', err);
          const errorMessage = err.error?.error || 'Erro ao fazer login. Use admin/admin';
          
          this.snackBar.open(errorMessage, 'Fechar', {
            duration: 5000,
            panelClass: ['error-snackbar']
          });
        }
      });
    }
  }
}
