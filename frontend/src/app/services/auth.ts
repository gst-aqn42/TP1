import { Injectable, PLATFORM_ID, inject } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';
import { isPlatformBrowser } from '@angular/common';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private readonly TOKEN_KEY = 'admin_token';
  private readonly baseUrl = 'http://localhost:5000/api';
  private platformId = inject(PLATFORM_ID);

  constructor(
    private router: Router,
    private http: HttpClient
  ) { }

  // Login com username e senha
  login(credentials: { username: string; password: string } | { email: string }): Observable<any> {
    return this.http.post(`${this.baseUrl}/auth/login`, credentials).pipe(
      tap((response: any) => {
        if (response.token && isPlatformBrowser(this.platformId)) {
          localStorage.setItem(this.TOKEN_KEY, response.token);
        }
      })
    );
  }

  logout(): void {
    if (isPlatformBrowser(this.platformId)) {
      localStorage.removeItem(this.TOKEN_KEY);
    }
    this.router.navigate(['/']);
  }

  isAuthenticated(): boolean {
    if (isPlatformBrowser(this.platformId)) {
      const token = localStorage.getItem(this.TOKEN_KEY);
      return token !== null;
    }
    return false;
  }

  getToken(): string | null {
    if (isPlatformBrowser(this.platformId)) {
      return localStorage.getItem(this.TOKEN_KEY);
    }
    return null;
  }
}
