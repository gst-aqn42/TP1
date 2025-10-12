import { Component, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { Article, Event, EventEdition } from '../../models/event.model';

@Component({
  selector: 'app-home',
  imports: [RouterLink, CommonModule, MatCardModule, MatButtonModule, MatIconModule],
  templateUrl: './home.html',
  styleUrl: './home.scss'
})
export class Home implements OnInit {
  topArticles: Article[] = [];
  topEvents: Event[] = [];

  ngOnInit(): void {
    this.loadTopArticles();
    this.loadTopEvents();
  }

  private loadTopArticles(): void {
    // Carrega os top 5 artigos mais recentes
    this.topArticles = [
      {
        id: '1',
        title: 'Machine Learning aplicado à Engenharia de Software',
        authors: ['Rafael Santos', 'Ana Costa'],
        abstract: 'Como ML pode auxiliar no desenvolvimento e manutenção de software...',
        year: 2024,
        pages: '300-320',
        pdfUrl: 'http://example.com/ml-software-eng.pdf',
        eventEditionId: '2'
      },
      {
        id: '2',
        title: 'Segurança em Aplicações Mobile',
        authors: ['Patricia Lima', 'Fernando Costa'],
        abstract: 'Principais vulnerabilidades e práticas de segurança em apps móveis...',
        year: 2024,
        pages: '230-250',
        pdfUrl: 'http://example.com/mobile-security.pdf',
        eventEditionId: '3'
      },
      {
        id: '3',
        title: 'DevOps e Integração Contínua',
        authors: ['Lucas Almeida', 'Sandra Silva'],
        abstract: 'Estratégias de DevOps para melhorar a entrega de software...',
        year: 2024,
        pages: '78-95',
        pdfUrl: 'http://example.com/devops-ci.pdf',
        eventEditionId: '2'
      },
      {
        id: '4',
        title: 'Inteligência Artificial no Desenvolvimento de Software',
        authors: ['Ana Costa', 'Carlos Mendes', 'João Silva'],
        abstract: 'Aplicações de IA no ciclo de desenvolvimento de software moderno...',
        year: 2024,
        pages: '100-115',
        pdfUrl: 'http://example.com/ai-development.pdf',
        eventEditionId: '1'
      },
      {
        id: '5',
        title: 'Metodologias Ágeis em Engenharia de Software',
        authors: ['João Silva', 'Maria Santos'],
        abstract: 'Este artigo apresenta uma análise das metodologias ágeis aplicadas ao desenvolvimento de software...',
        year: 2024,
        pages: '10-20',
        pdfUrl: 'http://example.com/agile-methods.pdf',
        eventEditionId: '1'
      }
    ];
  }

  private loadTopEvents(): void {
    // Carrega os top 5 eventos mais recentes
    this.topEvents = [
      {
        id: '1',
        name: 'Simpósio Brasileiro de Engenharia de Software',
        sigla: 'SBES',
        description: 'O principal evento de engenharia de software do Brasil',
        editions: []
      },
      {
        id: '2',
        name: 'Conferência Brasileira de Software',
        sigla: 'CBS',
        description: 'Conferência sobre desenvolvimento e qualidade de software',
        editions: []
      },
      {
        id: '3',
        name: 'Workshop de Testes de Software',
        sigla: 'WTS',
        description: 'Workshop focado em técnicas e ferramentas de teste',
        editions: []
      },
      {
        id: '4',
        name: 'Seminário de Arquitetura de Software',
        sigla: 'SAS',
        description: 'Seminário sobre padrões e práticas arquiteturais',
        editions: []
      },
      {
        id: '5',
        name: 'Congresso de DevOps e Agilidade',
        sigla: 'CDA',
        description: 'Congresso sobre práticas DevOps e metodologias ágeis',
        editions: []
      }
    ];
  }

  openPdf(pdfUrl: string): void {
    if (pdfUrl) {
      window.open(pdfUrl, '_blank');
    }
  }
}
