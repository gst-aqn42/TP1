import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { ApiService } from '../../services/api';
import { Event } from '../../models/event.model';

@Component({
  selector: 'app-events',
  imports: [
    CommonModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatProgressSpinnerModule
  ],
  templateUrl: './events.html',
  styleUrl: './events.scss'
})
export class Events implements OnInit {
  events: Event[] = [];
  loading = true;

  constructor(
    private apiService: ApiService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.loadEvents();
  }

  loadEvents(): void {
    this.loading = true;
    this.apiService.getEvents().subscribe({
      next: (response: any) => {
        const eventsData = response.eventos || [];
        this.events = eventsData.map((e: any) => ({
          id: e._id,
          name: e.nome,
          sigla: e.sigla,
          description: e.descricao || 'Sem descrição disponível',
          editions: []
        }));
        this.loading = false;
      },
      error: (err) => {
        console.error('Erro ao carregar eventos:', err);
        this.events = [];
        this.loading = false;
      }
    });
  }

  navigateToEvent(eventId: string, sigla: string): void {
    this.router.navigate(['/event', sigla]);
  }
}
