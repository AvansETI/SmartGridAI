import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss'],
})
export class HeaderComponent implements OnInit {
  menuItems = [
    {
      link: '/home',
      title: 'Home',
    },
    {
      link: '/about',
      title: 'About',
    },
    {
      link: '/predict',
      title: 'Predict',
    },
  ];

  constructor() {}

  ngOnInit(): void {}
}
