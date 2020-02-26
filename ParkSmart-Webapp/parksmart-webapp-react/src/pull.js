'use strict';

const debug = false;
const apiUrl = 'http://lamp.engin.umd.umich.edu/~bbrauchl/';

function strip_url_filename(url) {
    let len = url.lastIndexOf('/');
    len = len == -1 ? url.length : len + 1;
    return url.substring(0, len);
}

function get_url() {
    return apiUrl;
    return "./";
}

function pull_request(lot, getIsOccupied = true, getConfidence = false, getType = false, getExtra = false,
                getStartTimestamp = false, getEndTimestamp = false) {
    return new Promise(function (resolve, reject) {
        const endpoint = get_url() + 'api/pull.php';
        console.log(endpoint);
        const payload = {"lot":lot,
            "getIsOccupied":getIsOccupied,
            "getConfidence":getConfidence,
            "getType":getType,
            "getExtra":getExtra,
            "getStartTimestamp":getStartTimestamp,
            "getEndTimestamp":getEndTimestamp,
                    };
        const xhr = new XMLHttpRequest();
        xhr.open("POST", endpoint, true);
        xhr.responseType = 'json';

        xhr.onload = function() {
            console.log("onload")
            if (xhr.status >= 200 && xhr.status <= 300) {
                console.log("load status is good")
                resolve(xhr.response);
            }
        };
        xhr.onerror = function() {
            console.log("onerror");
            reject({
                status: xhr.status,
                statusText: xhr.statusText
            });
        };
        xhr.send(JSON.stringify(payload));
     })
}

async function pull_and_print(lot) {
    console.log("pull_and_print");
    const xhr = await pull_request(lot, debug=debug);
    console.log(xhr);
    console.log(JSON.stringify(xhr.response));
}

export async function pull(lot) {
    console.log("pull");
    const xhr = await pull_request(lot, debug);
    return xhr;
}

async function demo() {
    const obj = await pull('Lot_D');
    Object.keys(obj).forEach(key => {
        obj[key].forEach(space => {
           console.log("space " + space["Space"] + " is " + (Number(space["IsOccupied"]) ? "occupied" : "vacent")); 
        });
    });
}