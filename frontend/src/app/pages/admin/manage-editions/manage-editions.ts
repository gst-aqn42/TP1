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
    this.loadEditions();
  }

  loadEvents(): void {
    // Simula dados de eventos
    this.events = [
      { id: '1', name: 'Simpósio Brasileiro de Engenharia de Software', sigla: 'SBES' },
      { id: '2', name: 'Conferência Brasileira de Software', sigla: 'CBS' }
    ];
  }

  loadEditions(): void {
    // Simula dados de edições
    this.allEditions = [
      {
        id: '1',
        eventId: '1',
        year: 2024,
        numero: 37,
        cidadeSede: 'Curitiba'
      },
      {
        id: '2',
        eventId: '1',
        year: 2023,
        numero: 36,
        cidadeSede: 'Campo Grande'
      },
      {
        id: '3',
        eventId: '2',
        year: 2024,
        numero: 15,
        cidadeSede: 'São Paulo'
      }
    ];

    this.filterEditions();
  }

  filterEditions(): void {
    if (this.selectedEventId) {
      this.dataSource.data = this.allEditions.filter(edition => edition.eventId === this.selectedEventId);
    } else {
      this.dataSource.data = this.allEditions;
    }
  }

  onEventChange(): void {
    this.filterEditions();
  }

  openDialog(data?: EventEdition): void {
    const dialogRef = this.dialog.open(EditionDialog, {
      width: '500px',
      data: {
        edition: data || null,
        events: this.events
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
    editionData.id = Math.random().toString();
    this.allEditions.push(editionData);
    this.filterEditions();
    this.snackBar.open('Edição criada com sucesso!', 'Fechar', {
      duration: 3000,
      panelClass: ['success-snackbar']
    });
  }

  updateEdition(id: string, editionData: EventEdition): void {
    const index = this.allEditions.findIndex(e => e.id === id);
    if (index !== -1) {
      this.allEditions[index] = { ...editionData, id };
      this.filterEditions();
      this.snackBar.open('Edição atualizada com sucesso!', 'Fechar', {
        duration: 3000,
        panelClass: ['success-snackbar']
      });
    }
  }

  deleteEdition(id: string): void {
    const edition = this.allEditions.find(e => e.id === id);
    if (edition && confirm(`Tem certeza que deseja excluir a edição ${edition.numero} de ${edition.year}?`)) {
      this.allEditions = this.allEditions.filter(e => e.id !== id);
      this.filterEditions();
      this.snackBar.open('Edição excluída com sucesso!', 'Fechar', {
        duration: 3000,
        panelClass: ['success-snackbar']
      });
    }
  }

  getEventName(eventId: string): string {
    const event = this.events.find(e => e.id === eventId);
    return event ? event.name : 'Evento não encontrado';
  }
}
