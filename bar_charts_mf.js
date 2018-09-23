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
var ctx = document.getElementById("entries_by_doy").getContext('2d');

var doyChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: doy_labels,
        datasets: [{ label: '# of Entries by day of year',
	             data: doy_data, //deb_data,
                     pointRadius: 4,
		     //stack: 'Stack 0'
		     },
                   { type: 'line',
		     label: 'smoothed by 1 week',
	             data: doy_data_s7, //deb_data,
                     //stack: 'Stack 0',
		     pointRadius: 4,
                     backgroundColor: 'rgba(255, 159,  64, 0.2)',
                     borderColor:     'rgba(255, 206,  86, 1)',
                     },
                   { type: 'line',
		     label: '#smoothed by 2 weeks',
	             data: doy_data_s14, //deb_data,
                     //stack: 'Stack 0',
		     pointRadius: 4,
                     backgroundColor: 'rgba( 54, 162, 235, 0.2)',
                     borderColor:     'rgba( 54, 162, 235, 1)',
                     }
                    ]
    },
    options: {
       scales: {
          xAxes: [{
	          type: 'time', 
                  ticks: { source: 'labels' },
		  gridLines: { display:false },
		  time: {format: 'YYYY-MM-DD',
			 tooltipFormat:  'MMM DD',
			 displayFormats: {day: 'MMM D' },
                  stacked: true
                  }
          }],
          yAxes: [{
                ticks: {
                       beginAtZero:true,
                       max: 10
                },
		//stacked: true
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
var ctx = document.getElementById("searching").getContext('2d');
var searchChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: search_labels,
        datasets: [{
            label: '# of Entries searching for the language',
            data: search_values,
            backgroundColor: 'rgba( 54, 162, 235, 0.2)',
            borderColor:     'rgba( 54, 162, 235, 1)',
            borderWidth: 1
        }]
    },
    options: so_options
});

var ctx = document.getElementById("offering").getContext('2d');
var searchChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: offer_labels,
        datasets: [{
            label: '# of Entries offering this language',
            data: offer_values,
            backgroundColor: 'rgba(255, 159,  64, 0.2)',
            borderColor:     'rgba(255, 159,  64, 1)',
            borderWidth: 1
        }]
    },
    options: so_options
});
