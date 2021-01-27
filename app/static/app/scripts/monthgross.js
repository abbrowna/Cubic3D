$(function () {
    var $thismonthchart = $("#this_month_chart");
    $.ajax({
        url: $thismonthchart.data("url"),
        success: function (data) {
            var ctx = $thismonthchart[0].getContext("2d")
            new Chart(ctx, {
                type: 'horizontalBar',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Gross Income',
                        data: data.data,
                        backgroundColor: 'rgba(0, 0, 0, 1.0)',
                        borderColor: 'rgba(247, 213, 127, 0.7)',
                        borderWidth: 1,
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    title: {
                        display: true,
                        text: 'Gross Income this month',
                        fontColor: '#b3b3b3',
                        fontFamily: "'DIN Neuzeit Grotesk'",
                        fontSize: 19,
                        fontStyle: 'normal' 
                    },
                    legend: {
                        display: false,
                    },
                    scales: {
                        yAxes: [{
                            ticks: {
                                fontColor: '#b3b3b3',
                            },
                            gridLines: {
                                color: 'rgba(0, 0, 0, 0.3)',
                                zeroLineColor: 'rgba(0, 0, 0, 0.8)',
                            },
                        }],
                        xAxes: [{
                            gridLines: {
                                color: 'rgba(0, 0, 0, 0.3)',
                                zeroLineColor: 'rgba(0, 0, 0, 0.8)',
                            },
                            
                        }]
                    },
                }
            });
        }
    });
});