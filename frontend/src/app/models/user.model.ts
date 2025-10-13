export interface User {
  id?: string;
  name: string;
  email: string;
  createdAt?: Date;
  updatedAt?: Date;
}

export interface NotificationPreference {
  id?: string;
  userId: string;
  email: string;
  isActive: boolean;
  createdAt?: Date;
  updatedAt?: Date;
}
