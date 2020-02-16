<?php 

if ($_SERVER['REQUEST_METHOD']  === 'POST') {
  //print_r($_POST);
  $servername = array_key_exists("sql_servername", $_POST) ? filter_var($_POST["sql_servername"], FILTER_SANITIZE_URL) : "localhost";
  $username = array_key_exists("sql_username", $_POST) ? filter_var($_POST["sql_username"], FILTER_SANITIZE_STRING) : "ParkSmart";
  $password = array_key_exists("sql_password", $_POST) ? filter_var($_POST["sql_password"], FILTER_SANITIZE_STRING ) : NULL;
  $dbname = array_key_exists("sql_database", $_POST) ? filter_var($_POST["sql_database"], FILTER_SANITIZE_STRING ) : "parksmartdb";
  $sql = array_key_exists("sql_query", $_POST) ? filter_var($_POST["sql_query"]) : NULL;
  if (!$sql) {
    die("Parsing Failed: sql_servername not provided");
  }
  //var_dump($servername);
  //var_dump($username);
  //var_dump($password);
  //var_dump($dbname);
  //var_dump($sql);
  //$history = filter_var(filter_var($_POST["history"], FILTER_SANITIZE_STRING), FILTER_VALIDATE_BOOLEAN);
  if ($servername && $username && $dbname && $sql) {
    $conn = new mysqli($servername, $username, $password, $dbname);
    if ($conn->connect_error) {
      die("Connection Failed: ".$conn->connect_error);
    }
    $result = $conn->query($sql);
    while($row = $result->fetch_assoc()) {
      $myArray[] = $row;
    }     
    echo json_encode($myArray);
    $result->close(); 
    $conn->close();
  }
}

?>
