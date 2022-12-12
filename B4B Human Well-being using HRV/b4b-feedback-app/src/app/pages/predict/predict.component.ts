import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-predict',
  templateUrl: './predict.component.html',
  styleUrls: ['./predict.component.scss'],
})
export class PredictComponent implements OnInit {
  prediction?: any;
  loading: Boolean = false;
  explanation: Boolean = false;

  predictionForm: FormGroup = new FormGroup({
    decile1: new FormControl(null, [
      Validators.required,
      Validators.min(1),
      Validators.max(10),
    ]),
    decile3: new FormControl(null, [
      Validators.required,
      Validators.min(1),
      Validators.max(10),
    ]),
    lsat: new FormControl(null, [
      Validators.required,
      Validators.min(120),
      Validators.max(180),
    ]),
    ugpa: new FormControl(null, [
      Validators.required,
      Validators.min(0),
      Validators.max(4),
    ]),
    fulltime: new FormControl(false),
    grad: new FormControl(false),
  });

  ngOnInit(): void {}

  makePrediction(): void {}
}
