<?php

// if the request was made using the 'POST' method
if ($_SERVER['REQUEST_METHOD']  === 'POST') {

    include "helpers.php";
    $sql_server = get_sql_connection_info($_POST);

    //check if the payload exists
    if (!array_key_exists("payload", $_POST)) {
        die("Payload must conform to the API specification");
    }

    //extract the payload with update information
    $payload = json_decode(filter_var($_POST["payload"]));
    //print_r($payload);
    //check if the lot to update is specified
    if (!array_key_exists('Lot', $payload) 
            || !array_key_exists('Space', $payload)
            || !array_key_exists('IsOccupied', $payload)
            || !array_key_exists('Confidence', $payload)
            || !array_key_exists('Type', $payload)
            || !array_key_exists('Extra', $payload)) {
        die("Payload must conform to the API specification");
    }

    //create SQL update string
    try {
    $sql_query = "UPDATE $payload->Lot SET ";
    $sql_query .= "IsOccupied=$payload->IsOccupied, Confidence=$payload->Confidence, Type='$payload->Type', Extra='$payload->Extra' WHERE Space=$payload->Space";
    // $sql_query = "INSERT INTO $payload->Lot (Space, IsOccupied, Confidence, Type, Extra) ";
    // $sql_query .= "VALUES ($payload->Space, $payload->IsOccupied, $payload->Confidence, '$payload->Type', '$payload->Extra')";
    $conn = get_sql_connection($sql_server);  
    //print($sql_query);
    $result = $conn->query($sql_query);

    } catch (Exception $error) {
        die($error);
    }

    //do sql call
    if($result) {
        //print_r($result);
        echo "Success!";
    }
}

?>