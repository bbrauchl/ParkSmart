<?php

// allow access from any hosts. This makes development from localhost convienient but should be
// taken out later for security purposes.
header("Access-Control-Allow-Origin: *"); 

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

    $conn = get_sql_connection($sql_server);
    $conn->query("START TRANSACTION");

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
        if (!array_key_exists('Space', $element) || $element->Space == NULL) {
            $element->Space = 0;
        }
        if (!array_key_exists('IsOccupied', $element) || $element->IsOccupied == NULL) {
            $element->IsOccupied = 0;
        }
        if (!array_key_exists('Confidence', $element) || $element->Confidence == NULL) {
            $element->Confidence = 0.0;
        }
        if (!array_key_exists('Type', $element) || $element->Confidence == NULL) {
            $element->Confidence = "student";
        }

        //Grab the current entries for the historic table
        $sql_query = "SELECT * FROM $element->Lot WHERE Space = $element->Space;";
        $result = $conn->query($sql_query);
        if(!$result) {
            echo json_encode($conn->error_list);
            $conn->query("ROLLBACK");
            $conn->close();
            throw new Exception("SQL Select Failed");
        }
        $expired_datas = [];
        while($row = $result->fetch_assoc()) {
            $expired_datas[] = $row;
        }

        if(sizeof($expired_datas) != 1) {        
            //something went wrong, more there is not the right amount of entries in the main table.
            //delete all in the main table
            $sql_query = "DELETE FROM $element->Lot WHERE Space = $element->Space;";
            $result = $conn->query($sql_query);
            if(!$result) {
                echo json_encode($conn->error_list);
                $conn->query("ROLLBACK");
                $conn->close();
                throw new Exception("SQL Select Failed");
            }
            //insert new into main table
            $sql_query = "INSERT INTO $element->Lot (Space, IsOccupied, Confidence, Type, Extra) ";
            $sql_query .= "VALUES ($element->Space, $element->IsOccupied, $element->Confidence, '$element->Type', '$element->Extra');";
            $result = $conn->query($sql_query);
            if(!$result) {
                echo json_encode($conn->error_list);
                $conn->query("ROLLBACK");
                $conn->close();
                throw new Exception("SQL Insert Failed");
            }
        }
        else {
            //expected behavior
            $sql_query = "UPDATE $element->Lot SET";
            $sql_query .= " IsOccupied = $element->IsOccupied, Confidence = $element->Confidence, Type = '$element->Type', Extra = '$element->Extra'";
            $sql_query .= " WHERE Space = $element->Space;";
            $result = $conn->query($sql_query);
            //echo $sql_query;
            if(!$result) {
                echo json_encode($conn->error_list);
                $conn->query("ROLLBACK");
                $conn->close();
                throw new Exception("SQL Update Failed");
            }
        }

        if(sizeof($expired_datas) > 0) {
            //update the historic table
            foreach($expired_datas as $expired_data) {
                //set historic entry
                if (!array_key_exists('Space', $expired_data) || $expired_data['Space'] == NULL) {
                    $expired_data['Space'] = 0;
                }
                if (!array_key_exists('IsOccupied', $expired_data) || $expired_data['IsOccupied'] == NULL) {
                    $expired_data['IsOccupied'] = 0;
                }
                if (!array_key_exists('Confidence', $expired_data) || $expired_data['Confidence'] == NULL) {
                    $expired_data['Confidence'] = 0.0;
                }
                if (!array_key_exists('Type', $expired_data) || $expired_data['Type'] == NULL) {
                    $expired_data['Type'] = "student";
                }
                if (!array_key_exists('start_timestamp', $expired_data) || $expired_data['start_timestamp'] == NULL) {
                    $expired_data['start_timestamp'] = '';//date($expired_data['start_timestamp']);
                }
                if (!array_key_exists('end_timestamp', $expired_data) || $expired_data['end_timestamp'] == NULL) {
                    $expired_data['end_timestamp'] = '';//date($expired_data['end_timestamp']'');
                }

                $sql_query = "INSERT INTO {$element->Lot}_hist (Space, IsOccupied, Confidence, Type, Extra, start_timestamp, end_timestamp) ";
                $sql_query .= "VALUES ($expired_data[Space], $expired_data[IsOccupied], $expired_data[Confidence], '$expired_data[Type]',";
                $sql_query .= "'$expired_data[Extra]', '$expired_data[start_timestamp]', '$expired_data[end_timestamp]');";
                $result = $conn->query($sql_query);
                if(!$result) {
                    echo $sql_query;
                    echo json_encode($conn->error_list);
                    $conn->query("ROLLBACK");
                    $conn->close();
                    throw new Exception("SQL Insert Failed");
                }
            }
        }
    }

    $conn->query("COMMIT");
    $conn->close();

    echo "Success!";
}
else {
    header("Location: " . str_replace(".php", ".html", get_current_url()));
    die();
}

?>