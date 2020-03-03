import React from 'react';
import ReactDOM from 'react-dom';

import ParkingLot from './ParkingLot.js';

ReactDOM.render(
  ( <div>
      <h1>HelpMe</h1>
      <ParkingLot lotName="Lot_D" />
    </div>
  ),
  document.getElementById('root')
);