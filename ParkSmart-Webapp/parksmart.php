<!DOCTYPE html>
<html>
<head>
<style>
table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

td, th {
  border: 1px solid black;
  text-align: left;
  padding: 8px;
}

tr:nth-child(even) {
  background-color: #dddddd;
}
</style>
</head>
<body>

<form method="get">
<input type="text" id="host" name="host" value=<?= array_key_exists("host", $_GET) ? $_GET["host"] : ""; ?> />
<input type="submit" value="Go"/>
<input type="submit" name="history" value="Show All History"/>
</form>

<script type="text/javascript">
function findGetParameter(parameterName) {
    var result = null,
        tmp = [];
    location.search
        .substr(1)
        .split("&")
        .forEach(function (item) {
          tmp = item.split("=");
          if (tmp[0] === parameterName) result = decodeURIComponent(tmp[1]);
        });
    return result;
}
//document.getElementById('host').value = findGetParameter("host");
</script>

<script src = "http://ajax.aspnetcdn.com/ajax/jQuery/jquery-1.6.2.min.js"></script>
<script>
  function getCurrentWeather() {
    const api_key = "2c9454b4193e9aba28622a2603bc5f71";
    $.getJSON("http://api.openweathermap.org/data/2.5/weather?q=Dearborn&APPID=" + api_key, function(json){
      document.getElementById("weatherjson").innerHTML = JSON.stringify(json);
    });
  }
</script>

<a href="parksmart.php">Reset</a><br>

<?php

if (array_key_exists("host", $_GET) && $_GET["host"] !== "") {
    $servername = $_GET["host"];
    $username = "ParkSmart";
    $password = NULL;
    $dbname = "parksmartdb";
    // create database connection
    $conn = new mysqli($servername, $username, $password, $dbname);

    //check connection
    if ($conn->connect_error) {
        die("Connection failed: ".$conn->connect_error);
    }
    echo "Connection successful";

    echo '<table>';
    echo "<tr><td>Space Index</td><td>IsOccupied?</td><td>Confidence</td><td>Last Update</td></tr>";

    //perform a query on the table
    $sql = "SELECT * FROM Lot_D";
    if (isset($_GET["history"])) {
        $sql .= " FOR SYSTEM_TIME ALL"; 
    }
    $result = $conn->query($sql . " ORDER BY Space");

    //if there are any rows returned, print them on the web page.
    if($result->num_rows > 0) {
        //output each row
        while($row = $result->fetch_assoc()) {
            echo "<tr><td>${row["Space"]}</td><td>${row["IsOccupied"]}</td><td>${row["Confidence"]}</td><td>${row["start_timestamp"]}</td></tr>";
        }
    }
}
echo '</table>'
?>
<p id='weatherjson'>help</p>
<script>getCurrentWeather();</script>
</body>
</html>