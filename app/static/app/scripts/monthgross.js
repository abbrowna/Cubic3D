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
                    }]
                },
                options: {
                    /*responsive: true,*/
                    /*title: {
                        display: true,
                        text: 'Lifetime Monthly Gross Income',
                        fontColor: '#b3b3b3',
                        fontFamily: "'DIN Neuzeit Grotesk'",
                        fontSize: 19,
                        fontStyle: 'normal' 
                    },*/
                    /*legend: {
                        display: false,
                    },*/
                }
            });
        }
    });
});