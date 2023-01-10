import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-error-display',
  templateUrl: './error-display.component.html',
  styleUrls: ['./error-display.component.scss'],
})
export class ErrorDisplayComponent implements OnInit {
  @Input('control')
  control: any;

  ngOnInit(): void {}
}
