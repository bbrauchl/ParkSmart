<?php

// allow access from any hosts. This makes development from localhost convienient but should be
// taken out later for security purposes.
header("Access-Control-Allow-Origin: *"); 

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  print_r($_POST);

} 

?>
