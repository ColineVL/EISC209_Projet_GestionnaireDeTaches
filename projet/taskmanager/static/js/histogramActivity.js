// On récupère les données utiles
let list_dates = JSON.parse(document.getElementById('list_dates').textContent);
let list_dates_timestamp = JSON.parse(document.getElementById('list_dates_timestamp').textContent);
let data = [];
let data_timestamp = [];

for (let date of list_dates) {
    data.push([Date.UTC(date[0], date[1], date[2], date[3], date[4])]);
}

for (let date of list_dates_timestamp) {
        data_timestamp.push(new Date(date*1000));
}

// // Données test
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
        // tickInterval: 24 * 3600 * 1000, // one day
        // dateTimeLabelFormats: {
        //     day: '%d %b %Y'    //ex- 01 Jan 2016
        // },
        // labels: {
        //     formatter: function () {
        //         return new Date(this.value);
        //         // return Highcharts.dateFormat('%a %d %b', this.value);
        //     },
        //     format: "{value}%"
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
        data: data_timestamp,
        id: 's1',
        visible: false,
    }]
});
