<?php 

if ($_SERVER['REQUEST_METHOD']  === 'POST') {
  $servername = filter_var($_POST["host"]);
  $username = filter_var($_POST["user"]);
  $password = filter_var($_POST["pass"]);
  $dbname = filter_var($_POST["dbname"]);
  $sql = filter_var($_POST["sql"]);
  if (! $password) {
    $password = NULL;
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
