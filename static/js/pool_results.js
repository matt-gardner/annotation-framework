google.load("visualization", "1", {packages:["corechart"]});
google.setOnLoadCallback(drawChart);

function drawChart() {
  var data = google.visualization.arrayToDataTable($.results.precision_recall);

  var options = {
    title: 'Precision/Recall',
    hAxis: {maxValue: 1.0, minValue: 0.0},
    vAxis: {maxValue: 1.0, minValue: 0.0}
  };

  var chart = new google.visualization.LineChart(document.getElementById('precision-recall'));

  chart.draw(data, options);
}
