$(document).ready(function () {
    const ctx = document.getElementById("myChart");
    let chart;

    function getRandomColor() {
        return "rgba(" + Math.floor(Math.random() * 255) + ","
            + Math.floor(Math.random() * 255) + ","
            + Math.floor(Math.random() * 255) + ",0.5)";

    }

    $.ajax({
        method: 'GET',
        url: '/activity/get'
    }).done(
        function (response) {
            labelSet = response.label;
            dataSet = response.data;
            colorSet = [];
            for (let i = 0; i < dataSet.length; i++) {
                colorSet[i] = (getRandomColor())
            }
            const myChart = new Chart(ctx, {
                type: 'horizontalBar',
                data: {
                    labels: labelSet,
                    datasets: [{
                        label: 'activities',
                        data: dataSet,
                        backgroundColor: colorSet,
                        borderColor: colorSet,
                        borderWidth: 0.25
                    }]
                },
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: true
                            }
                        }]
                    },
                    title: {
                        display: true,
                        text: 'Activities'
                    }
                }
            });
            chart = myChart

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
                chart.data.labele = response.label;
                chart.data.datasets[0].data = response.data;
                chart.update();
                htmlString = `<h2>Today activities: ${response.activities_calories}kcal<h2>`;
                $(".page-header").html(htmlString)
            }
        )
    })
});