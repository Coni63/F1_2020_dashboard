import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { PositionsComponent } from './positions/positions.component';
import { RaceInfoComponent } from './race-info/race-info.component';
import { MyInfoComponent } from './my-info/my-info.component';

import { formatClassPipe, LapTimePipe, TimeFormatPipe } from './pipes.pipe';

@NgModule({
  declarations: [
    AppComponent,
    PositionsComponent,
    RaceInfoComponent,
    MyInfoComponent,
    formatClassPipe,
    LapTimePipe,
    TimeFormatPipe
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
