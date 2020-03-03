import React from 'react';
import PropTypes from 'prop-types';

import ParkingSpace from './ParkingSpace.js';

import './parksmart.css';

export default class ParkingLotOverlay extends React.Component {
    
    render() {
        let elements = [];
        let lotState = this.props.lotState;

        console.log(lotState);
        if (lotState == null) {
            lotState = [];
        }
        lotState = lotState.sort((s1, s2) => {
            return s1.Space - s2.Space;
        })

        this.props.coords.forEach((coord, index) => {
            if (lotState[index] == null) { lotState.push( {Space: index} ); }
            if (lotState[index].Space != index) {lotState.splice(index, 0, {Space: index} )}
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