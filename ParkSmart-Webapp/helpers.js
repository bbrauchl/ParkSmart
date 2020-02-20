'use strict';

const ParkSmartURL = 'http://lamp.engin.umd.umich.edu/~bbrauchl/ParkSmart/';
const ParkSmartURL_Local = 'http://localhost/ParkSmart/';

function stripUrlFilename(url) {
    let len = url.lastIndexOf('/');
    len = len == -1 ? url.length : len + 1;
    return url.substring(0, len);
}

function getUrl(debug = false) {
    let url;
    try {
        url = window.location.href;
    } catch(error) {
        console.log("No window defined, choosing default localhost. Are you running in a web browser?");
        url = (debug) ? ParkSmartURL_Local : ParkSmartURL;
    }
    return url;
}

module.exports = {
    stripUrlFilename,
    getUrl
}