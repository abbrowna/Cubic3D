$(function () {
    var $lifegrosschart = $("#life_gross_chart");
    $.ajax({
        url: $lifegrosschart.data("url"),
        success: function (data) {
            var ctx = $lifegrosschart[0].getContext("2d")
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Gross Income',
                        data: data.data,
                        borderColor: 'rgb(179, 179, 179, 0.5)',
                        pointBackgroundColor: 'rgb(247, 213, 127, 0.5)'
                    }]
                },
                options: {
                    responsive: true,
                    title: {
                        display: true,
                        text: 'Lifetime Monthly Gross Income',
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
                            }
                        }],
                        xAxes: [{
                            gridLines: {
                                color: 'rgba(0, 0, 0, 0.3)',
                                zeroLineColor: 'rgba(0, 0, 0, 0.8)',
                            }
                        }]

                    },
                }
            });
        }
    });
});