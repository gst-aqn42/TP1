import { Component, Inject, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialogModule } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { Event } from '../../../models/event.model';

@Component({
  selector: 'app-event-dialog',
  imports: [
    ReactiveFormsModule,
    MatDialogModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule
  ],
  templateUrl: './event-dialog.html',
  styleUrl: './event-dialog.scss'
})
export class EventDialog implements OnInit {
  eventForm: FormGroup;
  isEditMode: boolean;

  constructor(
    private fb: FormBuilder,
    private dialogRef: MatDialogRef<EventDialog>,
    @Inject(MAT_DIALOG_DATA) public data: Event | null
  ) {
    this.isEditMode = !!data;
    this.eventForm = this.fb.group({
      name: ['', Validators.required],
      sigla: ['', Validators.required],
      description: ['']
    });
  }

  ngOnInit(): void {
    if (this.data) {
      this.eventForm.patchValue(this.data);
    }
  }

  onSave(): void {
    if (this.eventForm.valid) {
      this.dialogRef.close(this.eventForm.value);
    }
  }

  onCancel(): void {
    this.dialogRef.close();
  }
}
