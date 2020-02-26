import React from 'react';
import ReactDOM from 'react-dom';

import LotD from './images/Lot_D.png';
import { pull } from './pull.js';


class ParkingLotD extends React.Component {

  constructor() {
    super();
    this.state = {};
    this.lotName = 'Lot_D';
  }

  async componentDidMount() {
    const resp = await pull(this.lotName);
    console.log(resp);
    this.setState(resp);
  }

  render() {
    console.log(LotD);
    return (
      <div>
        <img src={LotD} alt="Parking Lot D" />
        <p>{this.state[this.lotName]}</p>
      </div>
    );
  }
}

ReactDOM.render(
  <ParkingLotD />,
  document.getElementById('root')
);
  