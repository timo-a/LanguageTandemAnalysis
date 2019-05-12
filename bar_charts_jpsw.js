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
        datasets: [{ label: 'japanese offer',
	             data: jitter(doy_data_jp_offer), 
                     pointRadius: 4,
                     backgroundColor: 'rgba(255, 99, 132, 1)',
                     borderColor:     'rgba(0,   0,    0, 1)',
		     },
                   { label: 'japanese demand',
	             data: jitter(doy_data_jp_search),
		     pointRadius: 4,
                     backgroundColor: 'rgba(255, 99, 132, 0.1)',
                     borderColor:     'rgba(  0,  0,   0, 1)',
                     },
                   { label: 'swedish offer',
	             data: jitter(doy_data_sw_offer), 
		     pointRadius: 4,
                     backgroundColor: 'rgba( 54, 162, 235, 1)',
                     borderColor:     'rgba(  0,   0,   0, 1)',
                     },
                   { label: 'swedish demand',
	             data: jitter(doy_data_sw_search),
		     pointRadius: 4,
                     backgroundColor: 'rgba( 54, 162, 235, 0.1)',
                     borderColor:     'rgba(  0,   0,   0, 1)',
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
                       max: 6,
		       display: false
                },
	      //stacked: true
	      gridLines: { display:false },display:false
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
var ctx = document.getElementById("searching_jp").getContext('2d');
var searchChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: search_labels_jp,
        datasets: [{
            label: '# of Entries searching for the language',
            data: search_values_jp,
            backgroundColor: 'rgba( 54, 162, 235, 0.2)',
            borderColor:     'rgba( 54, 162, 235, 1)',
            borderWidth: 1
        }]
    },
    options: so_options
});

var ctx = document.getElementById("searching_sw").getContext('2d');
var searchChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: search_labels_sw,
        datasets: [{
            label: '# of Entries searching this language',
            data: search_values_sw,
            backgroundColor: 'rgba(255, 159,  64, 0.2)',
            borderColor:     'rgba(255, 159,  64, 1)',
            borderWidth: 1
        }]
    },
    options: so_options
});
