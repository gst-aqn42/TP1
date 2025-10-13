import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatTableModule, MatTableDataSource } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatTooltipModule } from '@angular/material/tooltip';
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
    MatSnackBarModule,
    MatTooltipModule
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
    console.log('🔍 Carregando eventos...');
    this.apiService.getEvents().subscribe({
      next: (response: any) => {
        console.log('📦 Resposta do backend:', response);
        // Backend retorna { eventos: [...] }
        const events = response.eventos || [];
        console.log(`✅ Encontrados ${events.length} eventos`);
        
        // Mapear campos do backend para frontend
        this.dataSource.data = events.map((e: any) => ({
          id: e._id,
          name: e.nome,
          sigla: e.sigla,
          description: e.descricao
        }));
        
        console.log('📊 Dados da tabela:', this.dataSource.data);
      },
      error: (err) => {
        console.error('❌ Erro ao carregar eventos:', err);
        this.snackBar.open('Erro ao carregar eventos', 'Fechar', {
          duration: 3000
        });
      }
    });
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
    // Mapear campos para o backend
    const backendData = {
      nome: eventData.name,
      sigla: eventData.sigla,
      descricao: eventData.description
    };

    this.apiService.createEvent(backendData).subscribe({
      next: (response: any) => {
        this.snackBar.open('Evento criado com sucesso!', 'Fechar', {
          duration: 3000,
          panelClass: ['success-snackbar']
        });
        this.loadEvents(); // Recarregar lista
      },
      error: (err) => {
        console.error('Erro ao criar evento:', err);
        this.snackBar.open('Erro ao criar evento', 'Fechar', {
          duration: 3000
        });
      }
    });
  }

  updateEvent(id: string, eventData: Event): void {
    const backendData = {
      nome: eventData.name,
      sigla: eventData.sigla,
      descricao: eventData.description
    };

    this.apiService.updateEvent(id, backendData).subscribe({
      next: () => {
        this.snackBar.open('Evento atualizado com sucesso!', 'Fechar', {
          duration: 3000,
          panelClass: ['success-snackbar']
        });
        this.loadEvents(); // Recarregar lista
      },
      error: (err) => {
        console.error('Erro ao atualizar evento:', err);
        this.snackBar.open('Erro ao atualizar evento', 'Fechar', {
          duration: 3000
        });
      }
    });
  }

  deleteEvent(id: string): void {
    const event = this.dataSource.data.find(e => e.id === id);
    if (event && confirm(`Tem certeza que deseja excluir o evento "${event.name}"?`)) {
      this.apiService.deleteEvent(id).subscribe({
        next: () => {
          this.snackBar.open('Evento excluído com sucesso!', 'Fechar', {
            duration: 3000,
            panelClass: ['success-snackbar']
          });
          this.loadEvents(); // Recarregar lista
        },
        error: (err) => {
          console.error('Erro ao excluir evento:', err);
          this.snackBar.open('Erro ao excluir evento', 'Fechar', {
            duration: 3000
          });
        }
      });
    }
  }
}
