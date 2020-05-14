// On récupère les données utiles
let list_dates = JSON.parse(document.getElementById('list_dates').textContent);
let data = [];
// On les met dans une liste propre
for (let date of list_dates) {
    data.push([Date.UTC(date[0], date[1], date[2], date[3], date[4])]);
}

// On crée un chart
Highcharts.chart('graph', {
    title: {
        text: 'Histogramme des entrées au cours du temps'
    },

    xAxis: [{
        type: 'datetime',
        alignTicks: false,
        opposite: true,
    }, {
        alignTicks: false,
    }],

    yAxis: [{
        title: {
            text: '',
            opposite: true
        }
    }, {
        title: {
            text: ''
        },
    }],

    series: [{
        name: 'Entrées',
        type: 'histogram',
        xAxis: 1,
        yAxis: 1,
        baseSeries: 's1',
    }, {
        name: 'Data',
        type: 'scatter',
        data: data,
        id: 's1',
        visible: false,
    }]
});
