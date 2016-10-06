<?php require_once 'db.php'; ?>
<!DOCTYPE html>
<html lang="en">
  <head>
    <title>
  </title>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="../../favicon.ico">
    <link href="assets/css/bootstrap.min.css" rel="stylesheet">
    <link href="assets/css/ie10-viewport-bug-workaround.css" rel="stylesheet">
    <link href="assets/jumbotron-narrow.css" rel="stylesheet">
    <!--[if lt IE 9]><script src="assets/js/ie8-responsive-file-warning.js"></script><![endif]-->
    <script src="assets/js/ie-emulation-modes-warning.js"></script>
    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
    <style type="text/css">
      body {
        padding-top: 70px;
        padding-bottom: 40px;
      }
    </style>
  </head>

 <body>
    <nav class="navbar navbar-default navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="#">Spidy</a>
        </div>
        <div id="navbar" class="navbar-collapse collapse">
          <ul class="nav navbar-nav pull-right">
            <li><a href="index.php"><span class="glyphicon glyphicon-list-alt" aria-hidden=""></span> Статистика</a></li>
            <li><a href="index.php?p=search"><span class="glyphicon glyphicon-search" aria-hidden=""></span> Поиск результатов</a></li>
          </ul>
        </div>
      </div>
    </nav>
<?php
$page_detect = $_SERVER[REQUEST_URI];
$page_search = $_SERVER["PHP_SELF"]."?p=search";
if($page_detect == $page_search) { $page = "Поиск по базе"; } 
else { $page = "Статистика"; }
?>

<div class="container">
<div class="row">
<div class="col-lg-10 col-lg-offset-1">

<h3 style="color: #3399f3;">Spidy - простой сканер интернетов<small> [ <?php echo $page; ?> ]</small></h3>
<hr />
</div>
<?php 
if($page_detect != $page_search) {
$total_query = mysql_query("SELECT COUNT(host) FROM test_scan");
$total_result = mysql_fetch_row($total_query);

$hosts_query = mysql_query("SELECT COUNT(DISTINCT(host)) FROM test_scan");
$uniq_hosts = mysql_fetch_row($hosts_query);
$ports_query = mysql_query("SELECT COUNT(DISTINCT(port)) FROM test_scan");
$uniq_ports = mysql_fetch_row($ports_query);
$banners_query = mysql_query("SELECT COUNT(banner) FROM test_scan WHERE banner = 'success'");
$uniq_banners = mysql_fetch_row($banners_query);
$last_update = mysql_query("SELECT date FROM test_scan ORDER BY date desc LIMIT 1");
$last_date = mysql_fetch_row($last_update);

?>
<div class="col-lg-8 col-lg-offset-1">
  <h2>Статистика сканирования <small>[ Всего результатов: <?php echo $total_result[0]; ?> ]</small></h2>
  <table class="table table-bordered">
    <thead><tr><th>Уник. хостов</th><th>Уник. портов</th><th>Успешных доступов</th><th>Последнее обновление</th></tr></thead>
    <tbody>
      <tr><td><?echo $uniq_hosts[0];?></td><td><?echo $uniq_ports[0];?></td><td><?echo $uniq_banners[0];?></td><td><?echo $last_date[0];?></td></tr>
  </tbody></table>
</div>
<?php } else {?>
<div class="col-lg-8 col-lg-offset-1">
  <h2>Поиск по базе данных</h2>
  <form action="<?echo $page_search;?>" method="post" role="form">
    <input type="text" name="port"  value="" placeholder="Порт" />
    <input type="text" name="host"  value="" placeholder="Хост" />
      Показывать только успешные попытки <input type="checkbox" name="success" value="success" /> 
    <input type="submit" value="Найти" class="form-control" />
  </form>
<hr />
<?php
$host = mysql_real_escape_string($_POST['host']);
$port = mysql_real_escape_string($_POST['port']);
$success = mysql_real_escape_string($_POST['success']);


if(!empty($port) || !empty($host)) {

  echo "<table class='table table-bordered'>";
  echo "<thead><tr><th>Хосты</th><th>Порты</th><th>Статус</th><th>Дата</th></tr></thead>";
  echo "<tbody>";

$search_query = mysql_query("SELECT * FROM test_scan WHERE host LIKE '$host' and banner LIKE '%{$success}%' OR port = '$port' AND banner LIKE '%{$success}%'");
while($row_search = mysql_fetch_array($search_query)) {
  $show_hosts = $row_search['host']; $show_ports = $row_search['port']; $show_banner = $row_search['banner']; $show_date = $row_search['date'];

    echo "<tr><td>".$show_hosts."</td><td>".$show_ports."</td><td>".$show_banner."</td><td>".$show_date."</td></tr>";

    }

  echo "</tbody>";
  echo "</table>";
    
  }
}
?>

</div>
</div>


<div class="container-fluid">
  <div class="footer">
    <div class="col-md-6 col-md-offset-4">
            <div class="inner">
              &copy; <a href="http://sm0k3.net" target=_blank title="Spidy">Spidy by sm0k3</a>, 2016&nbsp;
            </div>
    </div>
  </div>
</div>
  </body>
</html>
