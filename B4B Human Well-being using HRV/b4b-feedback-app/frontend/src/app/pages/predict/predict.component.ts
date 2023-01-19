import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { PredictService } from './predict.service';
import { PredictionInput } from './predictionInput.model';
import { PredictionOutput } from './predictionOutput.model';

@Component({
  selector: 'app-predict',
  templateUrl: './predict.component.html',
  styleUrls: ['./predict.component.scss'],
})
export class PredictComponent implements OnInit {
  prediction?: any;
  loading: Boolean = false;
  explanation: Boolean = false;
  error?: any;

  predictionForm: FormGroup = new FormGroup({
    thermalPreference: new FormControl(2, [Validators.required]),
    temperature: new FormControl(null, [
      Validators.required,
      Validators.min(0),
      Validators.max(100),
    ]),
    humidity: new FormControl(null, [
      Validators.required,
      Validators.min(0),
      Validators.max(100),
    ]),
    mood: new FormControl(3, [Validators.required]),
    modeOfTransport: new FormControl(1, [Validators.required]),
    light: new FormControl(null, [
      Validators.required,
      Validators.min(0),
      Validators.max(10000),
    ]),
    TVOC: new FormControl(null, [
      Validators.required,
      Validators.min(0),
      Validators.max(10000),
    ]),
    cloth2: new FormControl(false, [Validators.required]),
    eatRecentTwoHoursAgo: new FormControl(false, [Validators.required]),
    RMSSD: new FormControl(60, [Validators.required]),
  });

  constructor(private predictService: PredictService) { }

  ngOnInit(): void { }

  makePrediction(): void {
    this.loading = true;
    console.log('test1')
    this.predictService
      .predict(this.predictionForm.value as PredictionInput)
      .subscribe(
        (result) => {
          console.log("test")
          this.prediction = result as PredictionOutput

        },
        error => {
          this.loading = false;
          this.error = error
          console.log(error)
        }
      )
  };


  resetOutput(): void {
    this.prediction = undefined;
    this.loading = false;
  }

  showExplanation() {
    this.explanation = true;
  }

  hideExplanation() {
    this.explanation = false;
  }
}
