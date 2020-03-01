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
            style.backgroundColor = "yellow";
        } else if (this.props.status.IsOccupied) {
            style.backgroundColor = "red";
        } else {
            style.backgroundColor = "green";
        }
        console.log(style);
        return (
            <div className="space" style={style}>
                {this.props.status.Space}
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