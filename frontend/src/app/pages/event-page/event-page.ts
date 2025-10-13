import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatDividerModule } from '@angular/material/divider';
import { ApiService } from '../../services/api';
import { Event, EventEdition } from '../../models/event.model';

@Component({
  selector: 'app-event-page',
  imports: [
    CommonModule,
    RouterLink,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatDividerModule
  ],
  templateUrl: './event-page.html',
  styleUrl: './event-page.scss'
})
export class EventPage implements OnInit {
  event: Event | null = null;
  editions: EventEdition[] = [];
  loading = true;
  eventSigla: string = '';

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private apiService: ApiService
  ) {}

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.eventSigla = params['sigla'];
      this.loadEventDetails();
    });
  }

  loadEventDetails(): void {
    this.loading = true;

    // Simula busca do evento por sigla
    const mockEvents: Event[] = [
      {
        id: '1',
        name: 'Simpósio Brasileiro de Engenharia de Software',
        sigla: 'SBES',
        description: 'O SBES é o principal evento científico da área de Engenharia de Software no Brasil, sendo promovido anualmente pela Sociedade Brasileira de Computação (SBC).'
      },
      {
        id: '2',
        name: 'Conferência Brasileira de Software',
        sigla: 'CBS',
        description: 'A CBS é uma conferência dedicada à inovação em software e tecnologias emergentes.'
      }
    ];

    this.event = mockEvents.find(e =>
      e.sigla?.toLowerCase() === this.eventSigla.toLowerCase()
    ) || null;

    if (this.event) {
      this.loadEditions();
    } else {
      this.loading = false;
    }
  }

  loadEditions(): void {
    if (!this.event) return;

    // Simula busca das edições do evento
    const mockEditions: EventEdition[] = [
      {
        id: '1',
        eventId: '1',
        year: 2024,
        numero: 37,
        cidadeSede: 'Curitiba',
        description: '37ª edição do SBES realizada em Curitiba'
      },
      {
        id: '2',
        eventId: '1',
        year: 2023,
        numero: 36,
        cidadeSede: 'Campo Grande',
        description: '36ª edição do SBES realizada em Campo Grande'
      },
      {
        id: '3',
        eventId: '1',
        year: 2022,
        numero: 35,
        cidadeSede: 'Uberlândia',
        description: '35ª edição do SBES realizada em Uberlândia'
      },
      {
        id: '4',
        eventId: '2',
        year: 2024,
        numero: 15,
        cidadeSede: 'São Paulo',
        description: '15ª edição da CBS realizada em São Paulo'
      },
      {
        id: '5',
        eventId: '2',
        year: 2023,
        numero: 14,
        cidadeSede: 'Rio de Janeiro',
        description: '14ª edição da CBS realizada no Rio de Janeiro'
      }
    ];

    this.editions = mockEditions
      .filter(edition => edition.eventId === this.event!.id)
      .sort((a, b) => b.year - a.year); // Ordena por ano decrescente

    this.loading = false;
  }

  navigateToEdition(edition: EventEdition): void {
    this.router.navigate(['/eventos', this.eventSigla, edition.year]);
  }
}
