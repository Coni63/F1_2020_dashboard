import { Component, OnInit } from '@angular/core';
import { environment } from '../../environments/environment';

import { interval, Subscription } from 'rxjs';

import { formatClassPipe, LapTimePipe } from '../pipes.pipe';

import * as io from 'socket.io-client';


@Component({
  selector: 'app-positions',
  templateUrl: './positions.component.html',
  styleUrls: ['./positions.component.sass'],
  // providers: [formatClassPipe]
})
export class PositionsComponent implements OnInit {

  socket: SocketIOClient.Socket;
  subscription: Subscription;
  status: any;

  constructor() {
    this.socket = io.connect(environment.call_url);

    const source = interval(environment.refresh_rate_pilots_ms);
    this.subscription = source.subscribe(val => this.socket.emit("give_status"));
  }

  ngOnInit() {
    this.socket.on('status', (msg: any) => {
      this.status = msg.length == 0 ? null : msg;
      console.log(this.status);
      //this.subscription.unsubscribe();
    });
    
  }

  ngOnDestroy() {
    this.subscription.unsubscribe();
  }

}
