var jitter = function(data) {
  return data.map(function(e) {
           var yJitter = Math.random()*0.6 -0.3;
           return { t: e.t,   y: e.y + yJitter,    }
  });
};


var ctx = document.getElementById("entries_by_doy").getContext('2d');

var doyChart = new Chart(ctx, {
    type: 'scatter',
    data: {
        labels: doy_labels,
        datasets: [{ label: 'natives',
	             data: jitter(doy_data_natives), 
                     pointRadius: 4,
                     backgroundColor: 'rgba(54, 162, 235, 0.5)',
                     borderColor:     'rgb(54, 162, 235)',
		     },
                   { label: 'internationals',
	             data: jitter(doy_data_interns),
		     pointRadius: 4,
                     backgroundColor: 'rgba(255, 99, 132, 0.5)',
                     borderColor:     'rgb(255, 99, 132)',
                     }
                    ]
    },
    options: {
       scales: {
          xAxes: [{
	          type: 'time', 
                  ticks: { /*source: 'labels',*/  min: '2016-01-01', max: '2016-10-31' },
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
                       max: 3,
		       display: false
                },
	      //stacked: true
	      gridLines: { display:false },display:false
          }]
        }
    }
});

