$(document).ready(function () {
    const ctx = document.getElementById("myChart");
    let chart;

    let getColor = function() {
        return "rgba(" + Math.floor(Math.random() * 255) + ","
            + Math.floor(Math.random() * 255) + ","
            + Math.floor(Math.random() * 255) + ",0.3)";
    };
    function drawChart(labelSet,dataSet, getColor){
        let colorSet =[];
        for (let i = 0; i < dataSet.length; i++) {
            colorSet[i] = (getColor())
        }
        const myChart = new Chart(ctx, {
            type: 'horizontalBar',
            data: {
                labels: labelSet,
                datasets: [{
                    label: 'Activities',
                    data: dataSet,
                    backgroundColor: colorSet,
                    borderColor: colorSet,
                    borderWidth: 0.25
                }]
            },
            options: {
                options: {
                    title: {
                        display: true,
                        text: 'Activities'
                    },
                    animation: {
                        animateScale: true
                    }
                }
            }
        });
        return myChart;
    }

    $.ajax({
        method: 'GET',
        url: '/activity/get'
    }).done(
        function (response) {
            chart = drawChart(response.label, response.data, getColor);
        }
    );
    $(".form-inline.pagination.justify-content-center").submit(function (e) {
        e.preventDefault();
        let data = $(e.target).serialize();
        $.ajax({
            method: 'GET',
            url: '/activity/add',
            data: data
        }).done(
            function (response) {
                chart.data.labels = response.label;
                chart.data.datasets[0].data = response.data;
                for (let i = 0; i < response.label.length; i++) {
                    chart.data.datasets[0].backgroundColor[i] = (getColor())
                }
                chart.update();
                const htmlString = `<h2>Today activities: ${response.activities_calories}kcal<h2>`;
                $(".page-header").html(htmlString);
            }
        )
    })
});