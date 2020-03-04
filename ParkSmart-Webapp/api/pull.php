<?php

// allow access from any hosts. This makes development from localhost convienient but should be
// taken out later for security purposes.
header("Access-Control-Allow-Origin: *"); 

include "helpers.php";

// if the request was made using the 'POST' method
if ($_SERVER['REQUEST_METHOD']  === 'POST') {

    $sql_server = get_sql_connection_info($_POST);

    //get the names of all tables
    $all_tables = get_sql_all_tables();

    //check if the lot name exists
    if (array_key_exists("Lot", $_POST)) {
        if (is_JSON_string($_POST["Lot"])) {
            $lots = json_decode($_POST["Lot"]);
        } else {
            $lots = array($_POST["Lot"]);
        }
    } else {
        $lots = $all_tables;
    }

    $response = new stdClass();

    $conn_info = get_sql_connection_info();
    $conn = get_sql_connection($conn_info);

    foreach ($lots as $lot) {
        if(gettype($lot) != "string") {
            $conn->close();
            die("Error! Lot name specified in incorrect format. Should be provided as a string.");
        }
        if(!in_array($lot, $all_tables)) {
            $conn->close();
            die("Error! User specified Parking lot name that does not exist in the database!");
        }
        $sql = "SELECT * FROM ".$lot. " WHERE end_timestamp > NOW();";
        $result = $conn->query($sql); 
        if(!$result) {
            $conn->close();
            die("SQL Update Failed");
        }
        while($row = $result->fetch_assoc()) {
          $resultArray[] = $row;
        }     
        $response->{$lot} = $resultArray;
        $result->close();
    }
    
    $conn->close();
    
    //set the correct headers for a json response
    header('Content-type:application/json;charset=utf-8');
    //success!!
    echo json_encode($response);
}
else {
    header("Location: " . str_replace(".php", ".html", get_current_url()));
    die();
}

?>