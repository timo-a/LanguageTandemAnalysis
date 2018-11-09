var ctx = document.getElementById("entries_by_day_of_week").getContext('2d');
var dowChart = new Chart(ctx, {
    type: 'bar',
    data: { //window.chartColors.blue: 'rgb(54, 162, 235)'
        labels: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        datasets: [{
            label: '% entries by men',
            data: weekday_distribution_m,
            backgroundColor: 'rgba(54, 162, 235, 0.5)', //color(window.chartColors.blue).alpha(0.5).rgbString(),
            borderColor: 'rgb(54, 162, 235)', //window.chartColors.red,
            borderWidth: 1
        }, {
            label: '% entries by women',
            data: weekday_distribution_f,
            backgroundColor: 'rgba(255, 99, 132, 0.5)', //color(window.chartColors.red).alpha(0.5).rgbString(),
            borderColor: 'rgb(255, 99, 132)',  //window.chartColors.blue,
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        }
    }
});

var so_options =  {
  scales: {
  xAxes: [{type: 'category',
           gridLines: { display:false },
           ticks: {autoSkip: false }}],
  yAxes: [{
           ticks: {
               beginAtZero:true
           }
          }]
  }
}
