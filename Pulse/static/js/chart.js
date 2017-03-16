
function notify(title, description){
    $.post( "notify", { title: title, description: description }, function(data){
        case_id = data.split(",")[0]
        link = data.split(",")[1]
        console.log(link)
            $.notify({
	// options
	message: 'Gus case created : '+ case_id,
    url : link,
    mouse_over: 'pause'
},{
	// settings
	type: 'info'
});
        }   
     );
}

function anomaly_detection(values, anomalies){
    var j =20;
        Highcharts.chart('chart', {
            chart: {
                type: 'spline',
                marginRight: 10,
                events: {
                    load: function () {
                        $(".highcharts-legend-item path").attr('stroke-width', 12);
                        // set up the updating of the chart each second
                        var series = this.series[0];
                        var series1 = this.series[1];

                        setInterval(function () {
                            console.log(values[j][1], anomalies[j][1])
                            var x = values[j][0], 
                                y = values[j][1];
                                
                            series.addPoint([x, y], true, true);
                            
                                y = anomalies[j][1];
                                if (y < 6){
                                    y = 1; 
                                }else{
                                    if($( "#alert" ).hasClass( "active" )){
                                        notify("Anomaly found in DB CPU Usage" ,"Time stamp : "+values[j][0]+"\nValue : "+values[j][1])
                                    }
                                }
                            series1.addPoint([x, y], true, true);
                        j+=1;
                        }, 1500);
                        
                    },
                    redraw: function () {
                        $(".highcharts-legend-item path").attr('stroke-width', 12);
                    }
                }
            },
            title: {
                text: 'CPU Usage'
            },
            subtitle: {
                text: 'Anomalies aganist time series data'
            },
            xAxis: {
                type: 'datetime',
                dateTimeLabelFormats: { 
                    month: '%e. %b',
                    year: '%b'
                },
                title: {
                    text: 'Time'
                }
            },
            yAxis: {
                gridLineWidth: 0,
                title: {
                    text: 'Percentage of usage'
                },
                min: 0
            },
            tooltip: {
                headerFormat: '<b>{series.name}</b><br>',
                pointFormat: '{point.x:%e. %b}: {point.y:.2f} m'
            },
            plotOptions: {
                spline: {
                    marker: {
                        enabled: false
                    }
                }
            },

            series: [{
                name: 'CPU Usage',
                data: (function () {
                    var data = [];
                       
                    for (i = 0; i <= 19; i += 1) {
                        data.push({
                            x: values[i][0],
                            y: values[i][1]
                        });
                    }
                    return data;
                }()),
                color: '#21a0df'
        },{
                name: 'Anomalies',
                data: (function () {
                    var data = [];
  

                    for (i = 0; i <= 19; i += 1) {
                        data.push({
                            x: anomalies[i][0],
                            y: 1
                        });
                    }
                    return data;
        }()),zones: [{
            value: 1.2,
            color: '#0f0'
        },{
            color: '#f00'
        }],
            color: '#0f0'
        }],
        
        });
}


function prediction(title, subtitle, series1_label, series2_label, series1_values, series2_values, x_axis_label, y_axis_label, x_axis_metric, y_axis_metric){
    var j =20;
        Highcharts.chart('chart', {
            chart: {
                type: 'spline',
                marginRight: 10,
                events: {
                    load: function () {
                        console.log(j)
                        $(".highcharts-legend-item path").attr('stroke-width', 12);
                        // set up the updating of the chart each second
                        var series = this.series[0];
                        var series1 = this.series[1];

                        setInterval(function () {
                            console.log(values[j][0], values[j][1], predictions[j][1])
                            var x = values[j][0],     
                                y = predictions[j][1];
                            series1.addPoint([x, y], true, true);
                                y = values[j][1];
                            series.addPoint([x, y], true, true);
                            //redraw()
                        j+=1;
                        }, 1000);
                        
                    },
                    redraw: function () {
                        $(".highcharts-legend-item path").attr('stroke-width', 12);
                    }
                }
            },
            title: {
                text: title
            },
            subtitle: {
                text: subtitle
            },
            xAxis: {
                type: 'datetime',
                dateTimeLabelFormats: { 
                    month: '%e. %b',
                    year: '%b'
                },
                title: {
                    text: x_axis_label
                }
            },
            yAxis: {
                gridLineWidth: 0,
                title: {
                    text: y_axis_label
                },
                min: 0
            },
            tooltip: {
                headerFormat: '<b>{series.name}</b><br>',
                pointFormat: '{point.x:%e. %b}: {point.y:.2f} '+ y_axis_metric
            },
            plotOptions: {
                spline: {
                    marker: {
                        enabled: false
                    }
                }
            },

            series: [{
                name: series1_label,
                data: (function () {
                    var data = [];
                       
                    for (i = 0; i <= 19; i += 1) {
                        data.push({
                            x: values[i][0],
                            y: values[i][1]
                        });
                    }
                    return data;
                }()),
                color: '#21a0df'
        },{
                name: series2_label,
                data: (function () {
                    var data = [];
  

                    for (i = 0; i <= 19; i += 1) {
                        data.push({
                            x: predictions[i][0],
                            y: 1
                        });
                    }
                    return data;
        }()),
        
        color: '#0f0'
        
    }],
        
        });
}
        
