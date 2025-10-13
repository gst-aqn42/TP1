import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { Event } from '../../models/event.model';
import { ApiService } from '../../services/api';

@Component({
  selector: 'app-manage-events',
  imports: [
    CommonModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatSnackBarModule
  ],
  templateUrl: './manage-events.html',
  styleUrl: './manage-events.scss'
})
export class ManageEvents implements OnInit {
  events: Event[] = [];

  constructor(
    private apiService: ApiService,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.loadEvents();
  }

  loadEvents(): void {
    // Simula carregamento de eventos
    this.events = [
      {
        id: '1',
        name: 'Simpósio Brasileiro de Engenharia de Software',
        description: 'SBES - O principal evento de engenharia de software do Brasil'
      },
      {
        id: '2',
        name: 'Conferência Brasileira de Software',
        description: 'CBS - Evento focado em inovação em software'
      }
    ];
  }

  showCreateDialog(): void {
    this.snackBar.open('Funcionalidade de criação será implementada em breve!', 'Fechar', {
      duration: 3000,
      panelClass: ['info-snackbar']
    });
  }

  editEvent(event: Event): void {
    this.snackBar.open(`Editando evento: ${event.name}`, 'Fechar', {
      duration: 3000,
      panelClass: ['info-snackbar']
    });
  }

  deleteEvent(eventId: string): void {
    const eventToDelete = this.events.find(e => e.id === eventId);
    if (eventToDelete) {
      if (confirm(`Tem certeza que deseja excluir o evento "${eventToDelete.name}"?`)) {
        this.events = this.events.filter(e => e.id !== eventId);
        this.snackBar.open('Evento excluído com sucesso!', 'Fechar', {
          duration: 3000,
          panelClass: ['success-snackbar']
        });
      }
    }
  }
}
