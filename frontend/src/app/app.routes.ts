 import { Routes } from '@angular/router';
import { Home } from './pages/home/home';
import { SearchPage } from './pages/search-page/search-page';
import { LoginPage as AdminLoginPage } from './pages/admin/login-page/login-page';
import { AdminLayout } from './layouts/admin-layout/admin-layout';
import { ManageEvents as AdminManageEvents } from './pages/admin/manage-events/manage-events';
import { ManageEditions as AdminManageEditions } from './pages/admin/manage-editions/manage-editions';
import { ManageArticles as AdminManageArticles } from './pages/admin/manage-articles/manage-articles';
import { BatchUpload as AdminBatchUpload } from './pages/admin/batch-upload/batch-upload';
import { EventPage } from './pages/event-page/event-page';
import { EditionPage } from './pages/edition-page/edition-page';
import { AuthorPage } from './pages/author-page/author-page';
import { MainLayout } from './layouts/main-layout/main-layout';
import { authGuard } from './guards/auth-guard';

export const routes: Routes = [
  {
    path: '',
    component: MainLayout,
    children: [
      { path: '', redirectTo: '/home', pathMatch: 'full' },
      { path: 'home', component: Home },
      { path: 'pesquisa', component: SearchPage },
      { path: 'eventos/:sigla', component: EventPage },
      { path: 'eventos/:sigla/:ano', component: EditionPage },
      { path: 'autores/:nome', component: AuthorPage }
    ]
  },
  { path: 'admin/login', component: AdminLoginPage },
  {
    path: 'admin',
    component: AdminLayout,
    canActivate: [authGuard],
    children: [
      { path: '', redirectTo: 'eventos', pathMatch: 'full' },
      { path: 'eventos', component: AdminManageEvents },
      { path: 'edicoes', component: AdminManageEditions },
      { path: 'artigos', component: AdminManageArticles },
      { path: 'artigos/batch', component: AdminBatchUpload }
    ]
  },
  { path: '**', redirectTo: '/home' }
];
