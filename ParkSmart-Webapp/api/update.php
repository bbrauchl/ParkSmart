<?php

include "helpers.php";

// if the request was made using the 'POST' method
if ($_SERVER['REQUEST_METHOD']  === 'POST') {

    $sql_server = get_sql_connection_info($_POST);

    //check if the payload exists
    if (!array_key_exists("payload", $_POST)) {
        die("No JSON Payload delivered with POST request! use the key \"payload\"");
    }

    //extract the payload with update information
    $payload = json_decode(filter_var($_POST["payload"]));

    //convert all elements to arrays if they are not already
    if (gettype($payload) != "array") {
        $payload = array($payload);
    }

    foreach ($payload as $element) { 

        //check to make sure that all required components of the update request are present
        if (!array_key_exists('Lot', $element) 
                || !array_key_exists('Space', $element)
                || !array_key_exists('IsOccupied', $element)
                || !array_key_exists('Confidence', $element)
                || !array_key_exists('Type', $element)) {
            die("JSON Payload element is missing a required key! see " . str_replace(".php", ".html", get_current_url()));
        }
        
        //Check existance of optional elements
        if (!array_key_exists('Extra', $element)) {
            $element->Extra = '';
        }
        //fix for python
        if (!array_key_exists('IsOccupied', $element) || $element->IsOccupied == NULL) {
            $element->IsOccupied = 0;
        }

        //create SQL update string
        try {
            //expire previous entry
            $sql_query = "UPDATE " . $element->Lot . " SET end_timestamp = NOW() WHERE Space = $element->Space AND end_timestamp > NOW();";
            $conn = get_sql_connection($sql_server);  
            $result = $conn->query($sql_query);
            //set new entry
            $sql_query = "INSERT INTO ".$element->Lot."(Space, IsOccupied, Confidence, Type, Extra) ";
            $sql_query .= "VALUES ($element->Space, $element->IsOccupied, $element->Confidence, '$element->Type', '$element->Extra');";
            $result = $conn->query($sql_query);
            if(!$result) {
                throw new Exception("SQL Update Failed");
            }
        } catch (Exception $error) {
            die($error);
        }
    }

    echo "Success!";
}
else {
    header("Location: " . str_replace(".php", ".html", get_current_url()));
    die();
}

?>