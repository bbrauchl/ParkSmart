
const debug = true;
const apiUrl = 'http://lamp.engin.umd.umich.edu/~bbrauchl/';

function get_url() {
    if (debug) {
        return apiUrl;
    }
    return "./";
}

function pull_request(lot, getIsOccupied = true, getConfidence = false, getType = false, getExtra = false,
                getStartTimestamp = false, getEndTimestamp = false) {
    return new Promise(function (resolve, reject) {
        const endpoint = get_url() + 'api/pull.php';
        console.log(endpoint);
        const payload = {"lot":lot};
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

export async function pull_and_print(lot) {
    console.log("pull_and_print");
    const xhr = await pull_request(lot);
    console.log(xhr);
    console.log(JSON.stringify(xhr.response));
}

export default async function pull(lot) {
    console.log("pull");
    const xhr = await pull_request(lot);
    return xhr;
}

export async function demo() {
    const obj = await pull('Lot_D');
    Object.keys(obj).forEach(key => {
        obj[key].forEach(space => {
           console.log("space " + space["Space"] + " is " + (Number(space["IsOccupied"]) ? "occupied" : "vacent")); 
        });
    });
}