<?php

function get_sql_connection_info($var) {
    $result = [];
    $result['sql_servername'] = array_key_exists("sql_servername", $_POST) ? filter_var($_POST["sql_servername"], FILTER_SANITIZE_URL) : "localhost";
    $result['sql_username'] = array_key_exists("sql_username", $_POST) ? filter_var($_POST["sql_username"], FILTER_SANITIZE_STRING) : "ParkSmart";
    $result['sql_password'] = array_key_exists("sql_password", $_POST) ? filter_var($_POST["sql_password"], FILTER_SANITIZE_STRING ) : NULL;
    $result['sql_database'] = array_key_exists("sql_database", $_POST) ? filter_var($_POST["sql_database"], FILTER_SANITIZE_STRING ) : "parksmartdb";
    $result['sql_query'] = array_key_exists("sql_query", $_POST) ? filter_var($_POST["sql_query"], FILTER_SANITIZE_STRING) : NULL;
    return $result;
}

function get_sql_connection($var) {
    $conn = new mysqli($var['sql_servername'], 
                        $var['sql_username'],
                        $var['sql_password'],
                        $var['sql_database']);
    
    if ($conn->connect_error) {
        die("Connection Failed: ".$conn->connect_error);
    }
    return $conn;
}
?>