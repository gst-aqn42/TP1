import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatDividerModule } from '@angular/material/divider';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { ApiService } from '../../services/api';
import { Event, EventEdition } from '../../models/event.model';

@Component({
  selector: 'app-event-page',
  imports: [
    CommonModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatDividerModule,
    MatProgressSpinnerModule
  ],
  templateUrl: './event-page.html',
  styleUrl: './event-page.scss'
})
export class EventPage implements OnInit {
  event: Event | null = null;
  editions: EventEdition[] = [];
  loading = true;
  eventSigla: string = '';
  
  // Estatísticas
  totalArticles = 0;
  firstEditionYear: number | null = null;
  lastEditionYear: number | null = null;
  uniqueLocations = 0;
  editionYearsRange = '';

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

    // Buscar todos os eventos e filtrar pela sigla
    this.apiService.getEvents().subscribe({
      next: (response: any) => {
        const eventos = response.eventos || [];
        const eventoEncontrado = eventos.find((e: any) => 
          e.sigla?.toLowerCase() === this.eventSigla.toLowerCase()
        );

        if (eventoEncontrado) {
          this.event = {
            id: eventoEncontrado._id,
            name: eventoEncontrado.nome,
            sigla: eventoEncontrado.sigla,
            description: eventoEncontrado.descricao || 'Sem descrição disponível'
          };
          this.loadEditions(this.event.id!);
        } else {
          console.error('Evento não encontrado:', this.eventSigla);
          this.event = null;
          this.loading = false;
        }
      },
      error: (err) => {
        console.error('Erro ao carregar evento:', err);
        this.event = null;
        this.loading = false;
      }
    });
  }

  loadEditions(eventId: string): void {
    // Buscar edições do evento
    this.apiService.getEditions().subscribe({
      next: (response: any) => {
        const todasEdicoes = response.edicoes || [];
        
        // Filtrar edições do evento específico
        const edicoesDoEvento = todasEdicoes.filter((ed: any) => 
          ed.evento_id === eventId
        );

        this.editions = edicoesDoEvento.map((ed: any) => ({
          id: ed._id,
          eventId: eventId,
          year: ed.ano,
          location: ed.local || 'Local não informado',
          articleCount: ed.total_artigos || 0
        })).sort((a: any, b: any) => b.year - a.year); // Ordenar por ano decrescente

        this.calculateStatistics();
        this.loading = false;
      },
      error: (err: any) => {
        console.error('Erro ao carregar edições:', err);
        this.editions = [];
        this.loading = false;
      }
    });
  }

  calculateStatistics(): void {
    if (this.editions.length === 0) {
      return;
    }

    // Total de artigos
    this.totalArticles = this.editions.reduce((sum, ed) => sum + (ed.articleCount || 0), 0);

    // Anos
    const years = this.editions.map(ed => ed.year).sort((a, b) => a - b);
    this.firstEditionYear = years[0];
    this.lastEditionYear = years[years.length - 1];
    
    // Range de anos
    if (this.firstEditionYear && this.lastEditionYear) {
      const range = this.lastEditionYear - this.firstEditionYear;
      this.editionYearsRange = range === 0 ? 'Novo evento' : `${range + 1} anos`;
    }

    // Localidades únicas
    const locations = new Set(
      this.editions
        .map(ed => ed.location)
        .filter(loc => loc && loc !== 'Local não informado')
    );
    this.uniqueLocations = locations.size;
  }

  navigateToEdition(year: number): void {
    if (this.eventSigla) {
      this.router.navigate(['/eventos', this.eventSigla, year]);
    }
  }

  goBack(): void {
    this.router.navigate(['/events']);
  }
}
