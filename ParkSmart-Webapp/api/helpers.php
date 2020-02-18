<?php

function get_sql_connection_info() {
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
        throw new Exception("Could not connect to SQL database");
    }
    return $conn;
}

function get_current_url() {
    if(isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] === 'on') 
        $url = "https"; 
    else
        $url = "http"; 
    
    // Here append the common URL characters. 
    $url .= "://"; 
    
    // Append the host(domain name, ip) to the URL. 
    $url .= $_SERVER['HTTP_HOST']; 
    
    // Append the requested resource location to the URL 
    $url .= $_SERVER['REQUEST_URI']; 
        
    // Print the link 
    return $url; 
}

function is_JSON_string($string){
    return is_string($string) && json_decode($string, true) && (json_last_error() == JSON_ERROR_NONE) ? true : false;
 }

function get_sql_all_tables() {
    $conn_params = get_sql_connection_info();
    $conn = get_sql_connection($conn_params);
    $sql = "SHOW TABLES;";  
    $result = $conn->query($sql);
    if(!$result) {
        throw new Exception("SQL Update Failed");
    }
    while($row = $result->fetch_assoc()) {
        foreach($row as $key => $value) {
            $resultArray[] = $value;
        }
    }     
    $result->close(); 
    $conn->close();
    return $resultArray;
}

?>