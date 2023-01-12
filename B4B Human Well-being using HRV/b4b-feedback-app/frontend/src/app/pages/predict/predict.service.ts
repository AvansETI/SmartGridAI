import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { PredictionInput } from './predictionInput.model';

@Injectable({
  providedIn: 'root',
})
export class PredictService {
  private baseUrl = environment.baseUrl;

  constructor(private http: HttpClient) {}

  predict(data: PredictionInput) {
    return this.http.post(`${this.baseUrl}/predict`, data);
  }
}
