import React from 'react';
import PropTypes from 'prop-types';

import './parksmart.css';
import pull from './pull.js';
import ParkingLotOverlay from './ParkingLotOverlay.js'

export default class ParkingLot extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
    this.state[props.lotName] = null;
    this.lotName = props.lotName;
    this.lotPath = `./images/${this.lotName}.png`;
    this.lotImage = require(`${this.lotPath}`);
    this.coordsPath = `./coords/${this.lotName}.json`;
    this.coords = require(`${this.coordsPath}`);

    this.pollState = this.pollState.bind(this);
    this.onFocus = this.onFocus.bind(this);
    this.onBlur = this.onBlur.bind(this);
  }

  async onFocus() {
    this.pollState();
    clearInterval(this.interval);
    this.interval = setInterval(this.pollState, 1000);
  }

  async onBlur() {
    clearInterval(this.interval);
    this.interval = setInterval(this.pollState, 10000);
  }

  async pollState() {
    let resp;
    try {
      resp = await pull(this.lotName);
    } catch (error) {
      resp = {};
      resp[this.lotName] = null;
    }
    console.log(resp);
    this.setState(resp);
  }

  async componentDidMount() {
    this.pollState();
    this.interval = setInterval(this.pollState, 1000);
    window.addEventListener("focus", this.onFocus);
    window.addEventListener("blur", this.onBlur);
  }

  componentWillUnmount(){
    clearInterval(this.interval);
    window.removeEventListener("focus", this.onFocus);
    window.addEventListener("blur", this.onBlur);
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
