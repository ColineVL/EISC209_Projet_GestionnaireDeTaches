// var data = [3.5, 3, 3.2, 3.1, 3.6, 3.9, 3.4, 3.4, 2.9, 3.1, 3.7, 3.4, 3, 3, 4, 4.4, 3.9, 3.5, 3.8, 3.8, 3.4, 3.7, 3.6, 3.3, 3.4, 3, 3.4, 3.5, 3.4, 3.2, 3.1, 3.4, 4.1, 4.2, 3.1, 3.2, 3.5, 3.6, 3, 3.4, 3.5, 2.3, 3.2, 3.5, 3.8, 3, 3.8, 3.2, 3.7, 3.3, 3.2, 3.2, 3.1, 2.3, 2.8, 2.8, 3.3, 2.4, 2.9, 2.7, 2, 3, 2.2, 2.9, 2.9, 3.1, 3, 2.7, 2.2, 2.5, 3.2, 2.8, 2.5, 2.8, 2.9, 3, 2.8, 3, 2.9, 2.6, 2.4, 2.4, 2.7, 2.7, 3, 3.4, 3.1, 2.3, 3, 2.5, 2.6, 3, 2.6, 2.3, 2.7, 3, 2.9, 2.9, 2.5, 2.8, 3.3, 2.7, 3, 2.9, 3, 3, 2.5, 2.9, 2.5, 3.6, 3.2, 2.7, 3, 2.5, 2.8, 3.2, 3, 3.8, 2.6, 2.2, 3.2, 2.8, 2.8, 2.7, 3.3, 3.2, 2.8, 3, 2.8, 3, 2.8, 3.8, 2.8, 2.8, 2.6, 3, 3.4, 3.1, 3, 3.1, 3.1, 3.1, 2.7, 3.2, 3.3, 3, 2.5, 3, 3.4, 3];

// On récupère les données utiles
let data = JSON.parse(document.getElementById('list_dates').textContent);
// data = [
//     [Date.UTC(1970, 10, 25)],
//     [Date.UTC(1970, 11, 6)],
//     [Date.UTC(1970, 11, 20)],
//     [Date.UTC(1970, 11, 25)],
//     [Date.UTC(1971, 0, 4)],
//     [Date.UTC(1971, 0, 17)],
//     [Date.UTC(1971, 0, 24)],
//     [Date.UTC(1971, 1, 4)],
//     [Date.UTC(1971, 1, 14)],
//     [Date.UTC(1971, 2, 6)],
//     [Date.UTC(1971, 2, 14)],
//     [Date.UTC(1971, 2, 24)],
//     [Date.UTC(1971, 3, 1)],
//     [Date.UTC(1971, 3, 11)],
//     [Date.UTC(1971, 3, 27)],
//     [Date.UTC(1971, 4, 4)],
//     [Date.UTC(1971, 4, 9)],
// ];

Highcharts.chart('graph', {
    title: {
        text: 'Histogramme des entrées au cours du temps'
    },

    xAxis: [{
        type: 'datetime',
        tickInterval: 24 * 3600 * 1000, // one day
        // dateTimeLabelFormats: { // don't display the dummy year
        //     month: '%e. %b',
        //     year: '%b'
        // },
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
