import { HttpInterceptorFn } from '@angular/common/http';
import { isPlatformBrowser } from '@angular/common';
import { inject, PLATFORM_ID } from '@angular/core';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const platformId = inject(PLATFORM_ID);
  
  // Só acessar localStorage se estiver no navegador
  if (isPlatformBrowser(platformId)) {
    const token = localStorage.getItem('admin_token');
    
    // Se tiver token, adicionar no header Authorization
    if (token) {
      req = req.clone({
        setHeaders: {
          Authorization: `Bearer ${token}`
        }
      });
    }
  }
  
  return next(req);
};
