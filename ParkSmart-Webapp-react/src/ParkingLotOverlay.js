import React from 'react';
import PropTypes from 'prop-types';

import ParkingSpace from './parkingSpace.js';

import './parksmart.css';

export default class ParkingLotOverlay extends React.Component {
    constructor(props) {
        super(props);

        
    }
    
    render() {
        let elements = [];
        let lotState = this.props.lotState;

        console.log(lotState);
        if (lotState == null) {
            lotState = [];
        }

        this.props.coords.forEach((coord, index) => {
            if (lotState[index] == null) { lotState.push( {Space: index} ); }
            elements.push(<ParkingSpace key={index} coords={coord} status={lotState[index]} />);
        })
        return (
            <div className="overlay" >
                {elements}
            </div>
        );
    }
}

ParkingLotOverlay.defaultProps = {
    lotName: 'Lot_D',
    coords: {},
    lotState: {},
}

ParkingLotOverlay.propTypes = {
    lotName: PropTypes.string,
    coords: PropTypes.array,
    lotState: PropTypes.object,
}