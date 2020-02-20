'use strict';

const helpers = require('./helpers.js');
const XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;
const $ = require('jquery');

const url = "http://api.openweathermap.org/data/2.5/weather"
const api_query_location = "q=";
const api_api_key = "APPID=", api_key = "2c9454b4193e9aba28622a2603bc5f71";


function get_weather(query) {
    return new Promise(function(resolve, reject) {
        const endpoint = url + "?" + api_query_location + query + "&" + api_api_key + api_key;
        console.log("Request made to " + endpoint);
        const xhr = new XMLHttpRequest();
        xhr.open("GET", endpoint, true);
        xhr.responseType = 'json';

        xhr.onload = function() {
            if (xhr.status >= 200 && xhr.status <= 300) {
                console.log("OpenWeatherMap Response Loaded Successfully!");
                resolve(JSON.parse(xhr.responseText));
            }
        };
        xhr.onerror = function() {
            console.log(onerror);
            reject({
                status: xhr.status,
                statusText: xhr.statusText
            });
        } 
        xhr.send();
    })
}

async function get_Dearborn_weather() {
    const query_location = "Dearborn,Michigan,USA";
    const weather = await get_weather(query_location);
    return weather;
}

async function print_weather(query_location) {
    const weather = await get_weather(query_location);
    console.log(JSON.stringify(weather));
}

async function print_Dearborn_weather() {
    const weather = await get_Dearborn_weather();
    console.log(JSON.stringify(weather));
}

exports = {get_weather, get_Dearborn_weather, print_weather, print_Dearborn_weather};