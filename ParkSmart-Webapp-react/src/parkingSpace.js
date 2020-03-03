import React from 'react';
import PropTypes from 'prop-types';

import './parksmart.css';

export default class ParkingSpace extends React.Component {
    constructor(props) {
        super(props);

    }
    
    render() {
        const style = {
            top: this.props.coords.y,
            left: this.props.coords.x,
            height: this.props.coords.height,
            width: this.props.coords.width,
        }
        console.log(this.props.status.IsOccupied)
        if (this.props.status.IsOccupied == null) {
            //colored yellow if there is no data. This should also produce a warning.
            style.backgroundColor = `rgb(255,255,0,0.3)`;
        } else if (this.props.status.IsOccupied == 1) {
            //colored red if the spaces are occupied
            //use background alpha channel to indicate perdiction Confidence
            style.backgroundColor = `rgb(255,0,0,${0.3 + this.props.status.Confidence*.7})`;
        } else {
            //colored green if the spaces are vacent
            //use background alpha channel to indicate perdiction Confidence
            style.backgroundColor = `rgb(0,255,0,${0.3 + this.props.status.Confidence*.7})`;
        }
        console.log(this.props.status.Space);
        return (
            <div className="space" style={style}>
                <p>{this.props.status.Space}</p>
            </div>
        );
    }
}

ParkingSpace.defaultProps = {
    coords: {
        x: 0,
        y: 0,
        height: 0,
        width: 0,
    },
    status: {},
}

ParkingSpace.propTypes = {
    coords: PropTypes.object,
    status: PropTypes.object,
}