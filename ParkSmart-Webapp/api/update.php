<?php

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  print_r($_POST);
  echo '\n\n';
  $recieved = json_decode($_POST['json']);
  print_r($recieved->ParkingSpaces);

} 

?>
