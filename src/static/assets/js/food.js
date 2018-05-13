const ctx1 = document.getElementById("myChart1");
const myChart1 = new Chart(ctx1, {
    type: 'doughnut',
    data: {
        labels: ['Carbohydrate', 'Fat', 'Protein'],
        datasets: [{
            data: [12, 19, 3],
            backgroundColor: [
                'rgba(255, 0, 0, 0.5)',
                'rgba(0, 255, 0, 0.5)',
                'rgba(0, 0, 255, 0.5)',
            ],
        }]
    },
    options: {
        responsive: true,
        legend: {
            position: 'top'
        },
        title: {
            display: true,
            text: 'Today\'s major nutrients'
        },
        animation: {
            animateScale: true,
            animateRotate: true
        }
    }
});