'use strict';

const helpers = require('./helpers.js');
const XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;
const debug = true;

function pullRequest(lot, getIsOccupied = true, getConfidence = false, getType = false, getExtra = false,
                getStartTimestamp = false, getEndTimestamp = false) {
    return new Promise(function (resolve, reject) {
        const endpoint = helpers.getUrl(debug) + 'api/pull.php';
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
                resolve(xhr);
            }
        };
        xhr.onerror = function() {
            console.log(onerror);
            reject({
                status: xhr.status,
                statusText: xhr.statusText
            });
        };
        xhr.send(JSON.stringify(payload));
     })
}

async function pullAndPrint(lot) {
    console.log("pull_and_print");
    let r = await pullRequest(lot, debug=debug);
    console.log(r);
    console.log(r.response);
}

async function pull(lot) {
    console.log(pull);
    const r = await pullRequest(lot, debug);
    return JSON.parse(r.responseText);
}

async function main() {
    const obj = await pull('Lot_D', debug);
    Object.keys(obj).forEach(key => {
        obj[key].forEach(space => {
           console.log("space " + space["Space"] + " is " + (Number(space["IsOccupied"]) ? "occupied" : "vacent")); 
        });
    });
}

main();