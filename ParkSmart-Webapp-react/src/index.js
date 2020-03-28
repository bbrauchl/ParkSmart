import React from 'react';
import ReactDOM from 'react-dom';

import ParkingLot from './ParkingLot.js';
import get_Dearborn_weather from './weather.js'



ReactDOM.render(
  ( <div>
      <h1>ParkSmart</h1>
      <h2>Lot D</h2>
      <ParkingLot lotName="Lot_D" />
    </div>
  ),
  document.getElementById('root')
);

async function check_weather() {
  var cur_weather = await get_Dearborn_weather();
  console.log(cur_weather);
  if (cur_weather["visibility"] < 15000) {
    alert("Visibility is poor. Results may be inaccuate");
  } 
  else if (Number(cur_weather.weather[0].id) < 800) {
    alert("Weather Conditions are poor. Results may be inaccuate");
  }
}

check_weather();