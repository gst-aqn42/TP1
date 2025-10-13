import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatTableModule, MatTableDataSource } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatSelectModule } from '@angular/material/select';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../../services/api';
import { Event, EventEdition } from '../../../models/event.model';
import { EditionDialog } from '../../../components/dialogs/edition-dialog/edition-dialog';

@Component({
  selector: 'app-manage-editions',
  imports: [
    CommonModule,
    FormsModule,
    MatTableModule,
    MatButtonModule,
    MatIconModule,
    MatSelectModule,
    MatFormFieldModule,
    MatDialogModule,
    MatSnackBarModule
  ],
  templateUrl: './manage-editions.html',
  styleUrl: './manage-editions.scss'
})
export class ManageEditions implements OnInit {
  displayedColumns: string[] = ['ano', 'numero', 'cidadeSede', 'acoes'];
  dataSource = new MatTableDataSource<EventEdition>([]);
  events: Event[] = [];
  selectedEventId: string = '';
  allEditions: EventEdition[] = [];

  constructor(
    private apiService: ApiService,
    private dialog: MatDialog,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.loadEvents();
  }

  loadEvents(): void {
    this.apiService.getEvents().subscribe({
      next: (response: any) => {
        const events = response.eventos || [];
        this.events = events.map((e: any) => ({
          id: e._id,
          name: e.nome,
          sigla: e.sigla,
          description: e.descricao
        }));
        
        // Se houver eventos, seleciona o primeiro
        if (this.events.length > 0) {
          this.selectedEventId = this.events[0].id!;
          this.loadEditions();
        }
      },
      error: (err) => {
        console.error('Erro ao carregar eventos:', err);
        this.snackBar.open('Erro ao carregar eventos', 'Fechar', { duration: 3000 });
      }
    });
  }

  loadEditions(): void {
    if (!this.selectedEventId) {
      this.dataSource.data = [];
      return;
    }

    this.apiService.getEditionsByEvent(this.selectedEventId).subscribe({
      next: (editions: any[]) => {
        // Mapear campos do backend para frontend
        this.allEditions = editions.map((e: any) => ({
          id: e._id,
          eventId: e.evento_id,
          year: e.ano,
          numero: e.ano, // Usar ano como número também
          cidadeSede: e.local || 'N/A'
        }));
        this.filterEditions();
      },
      error: (err) => {
        console.error('Erro ao carregar edições:', err);
        this.snackBar.open('Erro ao carregar edições', 'Fechar', { duration: 3000 });
        this.allEditions = [];
        this.filterEditions();
      }
    });
  }

  filterEditions(): void {
    if (this.selectedEventId) {
      this.dataSource.data = this.allEditions.filter(edition => edition.eventId === this.selectedEventId);
    } else {
      this.dataSource.data = this.allEditions;
    }
  }

  onEventChange(): void {
    this.loadEditions();
  }

  openDialog(data?: EventEdition): void {
    const dialogRef = this.dialog.open(EditionDialog, {
      width: '500px',
      data: {
        edition: data || null,
        events: this.events,
        selectedEventId: this.selectedEventId
      }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        if (data) {
          this.updateEdition(data.id!, result);
        } else {
          this.createEdition(result);
        }
      }
    });
  }

  createEdition(editionData: EventEdition): void {
    // Mapear campos para o backend
    const backendData = {
      evento_id: editionData.eventId || this.selectedEventId,
      ano: editionData.year,
      local: editionData.cidadeSede
    };

    this.apiService.createEdition(backendData).subscribe({
      next: (response: any) => {
        this.snackBar.open('Edição criada com sucesso!', 'Fechar', {
          duration: 3000,
          panelClass: ['success-snackbar']
        });
        this.loadEditions();
      },
      error: (err) => {
        console.error('Erro ao criar edição:', err);
        this.snackBar.open('Erro ao criar edição', 'Fechar', { duration: 3000 });
      }
    });
  }

  updateEdition(id: string, editionData: EventEdition): void {
    const backendData = {
      ano: editionData.year,
      local: editionData.cidadeSede
    };

    this.apiService.updateEdition(id, backendData).subscribe({
      next: () => {
        this.snackBar.open('Edição atualizada com sucesso!', 'Fechar', {
          duration: 3000,
          panelClass: ['success-snackbar']
        });
        this.loadEditions();
      },
      error: (err) => {
        console.error('Erro ao atualizar edição:', err);
        this.snackBar.open('Erro ao atualizar edição', 'Fechar', { duration: 3000 });
      }
    });
  }

  deleteEdition(id: string): void {
    const edition = this.allEditions.find(e => e.id === id);
    if (edition && confirm(`Tem certeza que deseja excluir a edição de ${edition.year}?`)) {
      this.apiService.deleteEdition(id).subscribe({
        next: () => {
          this.snackBar.open('Edição excluída com sucesso!', 'Fechar', {
            duration: 3000,
            panelClass: ['success-snackbar']
          });
          this.loadEditions();
        },
        error: (err) => {
          console.error('Erro ao excluir edição:', err);
          this.snackBar.open('Erro ao excluir edição', 'Fechar', { duration: 3000 });
        }
      });
    }
  }

  getEventName(eventId: string): string {
    const event = this.events.find(e => e.id === eventId);
    return event ? event.name : 'Evento não encontrado';
  }
}
