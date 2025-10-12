import { Component, Inject, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialogModule } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatButtonModule } from '@angular/material/button';
import { CommonModule } from '@angular/common';
import { Event, EventEdition } from '../../../models/event.model';

interface EditionDialogData {
  edition?: EventEdition;
  events: Event[];
}

@Component({
  selector: 'app-edition-dialog',
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatDialogModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatButtonModule
  ],
  templateUrl: './edition-dialog.html',
  styleUrl: './edition-dialog.scss'
})
export class EditionDialog implements OnInit {
  editionForm: FormGroup;
  isEditMode: boolean;
  events: Event[];

  constructor(
    private fb: FormBuilder,
    private dialogRef: MatDialogRef<EditionDialog>,
    @Inject(MAT_DIALOG_DATA) public data: EditionDialogData
  ) {
    this.isEditMode = !!data.edition;
    this.events = data.events;

    this.editionForm = this.fb.group({
      eventId: ['', Validators.required],
      year: ['', [Validators.required, Validators.min(1900), Validators.max(2100)]],
      numero: ['', [Validators.required, Validators.min(1)]],
      cidadeSede: ['', Validators.required]
    });
  }

  ngOnInit(): void {
    if (this.data.edition) {
      this.editionForm.patchValue(this.data.edition);
    }
  }

  onSave(): void {
    if (this.editionForm.valid) {
      this.dialogRef.close(this.editionForm.value);
    }
  }

  onCancel(): void {
    this.dialogRef.close();
  }
}
