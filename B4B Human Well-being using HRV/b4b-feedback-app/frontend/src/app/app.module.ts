import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './pages/home/home.component';
import { AboutComponent } from './pages/about/about.component';
import { PredictComponent } from './pages/predict/predict.component';
import { HeaderComponent } from './components/header/header.component';
import { ErrorDisplayComponent } from './components/error-display/error-display.component';
import { TooltipComponent } from './components/tooltip/tooltip.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { FooterComponent } from './components/footer/footer.component';
import { IgxLinearGaugeModule } from "igniteui-angular-gauges";

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    AboutComponent,
    PredictComponent,
    HeaderComponent,
    ErrorDisplayComponent,
    TooltipComponent,
    FooterComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    FontAwesomeModule,
    ReactiveFormsModule,
    HttpClientModule,
    IgxLinearGaugeModule
  ],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule { }
