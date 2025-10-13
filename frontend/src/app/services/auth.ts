import { Injectable } from '@angular/core';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private readonly TOKEN_KEY = 'admin_token';
  private readonly ADMIN_CREDENTIALS = {
    username: 'admin',
    password: 'admin'
  };

  constructor(private router: Router) { }

  login(credentials: { username: string; password: string }): boolean {
    if (credentials.username === this.ADMIN_CREDENTIALS.username &&
        credentials.password === this.ADMIN_CREDENTIALS.password) {
      // Gera um token falso para simular autenticação
      const fakeToken = btoa(`${credentials.username}:${Date.now()}`);
      localStorage.setItem(this.TOKEN_KEY, fakeToken);
      return true;
    }
    return false;
  }

  logout(): void {
    localStorage.removeItem(this.TOKEN_KEY);
    this.router.navigate(['/']);
  }

  isAuthenticated(): boolean {
    const token = localStorage.getItem(this.TOKEN_KEY);
    return token !== null;
  }

  getToken(): string | null {
    return localStorage.getItem(this.TOKEN_KEY);
  }
}
