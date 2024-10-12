// const renderChart = (data, labels) => {
//     var ctx = document.querySelector('#myChart').getContext('2d');
//     new Chart(ctx, {
//         type: 'doughnut',
//         data: {
//             labels: labels,
//             datasets: [{
//                 label: 'Gastos de los últimos 6 meses',
//                 data: data,
//                 backgroundColor: [
//                     'rgba(255, 99, 132, 0.2)',
//                     'rgba(54, 162, 235, 0.2)',
//                     'rgba(255, 206, 86, 0.2)',
//                     'rgba(75, 192, 192, 0.2)',
//                     'rgba(153, 102, 255, 0.2)',
//                     'rgba(255, 152, 64, 0.2)',
//                 ],
//                 borderColor: [
//                     'rgba(255, 99, 132, 1)',
//                     'rgba(54, 162, 235, 1)',
//                     'rgba(255, 206, 86, 1)',
//                     'rgba(75, 192, 192, 1)',
//                     'rgba(153, 102, 255, 1)',
//                     'rgba(255, 159, 64, 1)',
//                 ],
//                 borderWidth: 1
//             }]
//         },
//         options: {
//             title: {
//                 display: true,
//                 text: "Gastos por categorías",
//             },
//         },
//     });
// }


const renderChart = (data, labels) => {
    let n, d, s, c, p;
    c = (isDarkStyle ? ((n = config.colors_dark.cardColor),
        (d = config.colors_dark.headingColor),
        (s = config.colors_dark.textMuted),
        (p = config.colors_dark.bodyColor),
        config.colors_dark) : ((n = config.colors.cardColor),
        (d = config.colors.headingColor),
        (s = config.colors.textMuted),
        (p = config.colors.bodyColor),
        config.colors)
    ).borderColor;

    var b = document.getElementById("myChart"),
    b = (b && new Chart(b, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [
                {
                    data: data,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.8)',
                        'rgba(54, 162, 235, 0.8)',
                        'rgba(255, 206, 86, 0.8)',
                        'rgba(75, 192, 192, 0.8)',
                        'rgba(153, 102, 255, 0.8)',
                        'rgba(255, 152, 64, 0.8)',
                    ],
                    borderColor: "transparent",
                    maxBarThickness: 100,
                    borderRadius: { topRight: 15, topLeft: 15 },
                },
            ],
        },
        options: {
            responsive: !0,
            maintainAspectRatio: !1,
            animation: { duration: 500 },
            plugins: {
                tooltip: {
                    rtl: isRtl,
                    backgroundColor: n,
                    titleColor: d,
                    bodyColor: p,
                    borderWidth: 1,
                    borderColor: c,
                },
                legend: { display: !1 },
            },
            scales: {
                x: {
                    grid: { color: c, drawBorder: !1, borderColor: c },
                    ticks: { color: s },
                },
                y: {
                    min: 0,
                    max: 300,
                    grid: { color: c, drawBorder: !1, borderColor: c },
                    ticks: { stepSize: 100, color: s },
                },
            },
        },
    }));
}

const getChartData = () => {
    // console.log("fetching");
    fetch("/expenses/expense-category-summary/")
        .then((res) => res.json())
        .then((results) => {
            // console.log(results);
            const category_data = JSON.parse(results.expense_category_data);

            const labels = Object.keys(category_data);
            const data = Object.values(category_data);

            renderChart(data, labels);
        });
}

document.onload = getChartData();