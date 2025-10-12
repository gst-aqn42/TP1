import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatTableModule, MatTableDataSource } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { ApiService } from '../../../services/api';
import { Event } from '../../../models/event.model';
import { EventDialog } from '../../../components/dialogs/event-dialog/event-dialog';

@Component({
  selector: 'app-manage-events',
  imports: [
    CommonModule,
    MatTableModule,
    MatButtonModule,
    MatIconModule,
    MatDialogModule,
    MatSnackBarModule
  ],
  templateUrl: './manage-events.html',
  styleUrl: './manage-events.scss'
})
export class ManageEvents implements OnInit {
  displayedColumns: string[] = ['nome', 'sigla', 'acoes'];
  dataSource = new MatTableDataSource<Event>([]);

  constructor(
    private apiService: ApiService,
    private dialog: MatDialog,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.loadEvents();
  }

  loadEvents(): void {
    // Simulando dados já que não temos backend real
    const mockEvents: Event[] = [
      {
        id: '1',
        name: 'Simpósio Brasileiro de Engenharia de Software',
        sigla: 'SBES',
        description: 'O principal evento de engenharia de software do Brasil'
      },
      {
        id: '2',
        name: 'Conferência Brasileira de Software',
        sigla: 'CBS',
        description: 'Evento focado em inovação em software'
      }
    ];

    this.dataSource.data = mockEvents;
  }

  openDialog(data?: Event): void {
    const dialogRef = this.dialog.open(EventDialog, {
      width: '500px',
      data: data || null
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        if (data) {
          // Modo de edição
          this.updateEvent(data.id!, result);
        } else {
          // Modo de criação
          this.createEvent(result);
        }
      }
    });
  }

  createEvent(eventData: Event): void {
    // Simula criação
    eventData.id = Math.random().toString();
    this.dataSource.data = [...this.dataSource.data, eventData];
    this.snackBar.open('Evento criado com sucesso!', 'Fechar', {
      duration: 3000,
      panelClass: ['success-snackbar']
    });
  }

  updateEvent(id: string, eventData: Event): void {
    // Simula atualização
    const index = this.dataSource.data.findIndex(e => e.id === id);
    if (index !== -1) {
      this.dataSource.data[index] = { ...eventData, id };
      this.dataSource.data = [...this.dataSource.data];
      this.snackBar.open('Evento atualizado com sucesso!', 'Fechar', {
        duration: 3000,
        panelClass: ['success-snackbar']
      });
    }
  }

  deleteEvent(id: string): void {
    const event = this.dataSource.data.find(e => e.id === id);
    if (event && confirm(`Tem certeza que deseja excluir o evento "${event.name}"?`)) {
      this.dataSource.data = this.dataSource.data.filter(e => e.id !== id);
      this.snackBar.open('Evento excluído com sucesso!', 'Fechar', {
        duration: 3000,
        panelClass: ['success-snackbar']
      });
    }
  }
}
