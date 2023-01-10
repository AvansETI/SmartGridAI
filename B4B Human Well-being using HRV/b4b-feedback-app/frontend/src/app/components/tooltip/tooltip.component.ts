import { Component, Input, OnInit } from '@angular/core';
import { faCircleInfo } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-tooltip',
  templateUrl: './tooltip.component.html',
  styleUrls: ['./tooltip.component.scss'],
})
export class TooltipComponent implements OnInit {
  faCircleInfo = faCircleInfo;
  tooltip_status = 0;
  @Input() description = '';

  constructor() {}

  ngOnInit(): void {}
}
