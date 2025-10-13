export interface Event {
  id?: string;
  name: string;
  sigla?: string;
  description?: string;
  createdAt?: Date;
  updatedAt?: Date;
  editions?: EventEdition[];
}

export interface EventEdition {
  id?: string;
  eventId: string;
  year: number;
  numero?: number;
  cidadeSede?: string;
  location?: string;
  startDate?: Date;
  endDate?: Date;
  description?: string;
  articles?: Article[];
  articleCount?: number;
  createdAt?: Date;
  updatedAt?: Date;
}

export interface Article {
  id?: string;
  title: string;
  authors: string[];
  abstract?: string;
  keywords?: string[];
  eventEditionId?: string;
  pdfUrl?: string;
  bibtexEntry?: string;
  year?: number;
  pages?: string;
  doi?: string;
  createdAt?: Date;
  updatedAt?: Date;
}
