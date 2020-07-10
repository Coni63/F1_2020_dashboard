import { Component, OnInit } from '@angular/core';
import { environment } from '../../environments/environment';

import { interval, Subscription } from 'rxjs';

import { TimeFormatPipe } from '../pipes.pipe';

import * as io from 'socket.io-client';

@Component({
  selector: 'app-race-info',
  templateUrl: './race-info.component.html',
  styleUrls: ['./race-info.component.sass']
})
export class RaceInfoComponent implements OnInit {

  socket: SocketIOClient.Socket;
  subscription: Subscription;
  status: any;

  constructor() {
    this.socket = io.connect(environment.call_url);

    const source = interval(environment.refresh_rate_track_ms);
    this.subscription = source.subscribe(val => this.socket.emit("give_track"));
  }

  ngOnInit() {
    this.socket.on('track', (msg: any) => {
      this.status = msg;
      console.log(this.status);
      //this.subscription.unsubscribe();
    });
    
  }

  ngOnDestroy() {
    this.subscription.unsubscribe();
  }

}
