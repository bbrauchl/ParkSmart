import React from 'react';
import ReactDOM from 'react-dom';
import PropTypes from 'prop-types';

import './parksmart.css';
import pull from './pull.js';
import ParkingLotOverlay from './ParkingLotOverlay.js'

class ParkingLot extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
    this.lotName = props.lotName;
    this.lotPath = `./images/${this.lotName}.png`;
    this.lotImage = require(`${this.lotPath}`);
    this.coordsPath = `./coords/${this.lotName}.json`;
    this.coords = require(`${this.coordsPath}`);
  }

  async componentDidMount() {
    const resp = await pull(this.lotName);
    console.log(resp);
    this.setState(resp);
  }

  render() {
    console.log(this.lotName);
    return (
      <div className="lot">
        <img src={this.lotImage} alt={this.lotName} />
        <ParkingLotOverlay lotName={this.lotName} coords={this.coords} lotState={this.state['Lot_D']} />
      </div>
    );
  }
}

ParkingLot.defaultProps = {
  lotName: 'Lot_D',
}

ParkingLot.propTypes = {
  lotName: PropTypes.string,
}

ReactDOM.render(
  ( <div>
      <h1>HelpMe</h1>
      <ParkingLot lotName="Lot_D" />
    </div>
  ),
  document.getElementById('root')
);