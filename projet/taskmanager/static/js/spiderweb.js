// On récupère les données utiles
const list_dicts = JSON.parse(document.getElementById('list_dicts').textContent);

// On initialise les options du chart
const options = {
    chart: {
        polar: true,
        type: 'line'
    },

    title: {
        align: "center",
        text: 'Nombre de tâches par personne',
    },
    xAxis: {
        categories: [],
        tickmarkPlacement: 'on',
        lineWidth: 0
    },

    yAxis: {
        gridLineInterpolation: 'polygon',
        lineWidth: 0,
        min: 0
    },

    tooltip: {
        shared: true,
        pointFormat: '<span>{series.name}: <b>{point.y}</b><br/>'
    },

    legend: {
        enabled: false,
    },

    series: [{
        name: 'Nombre de tâches',
        data: [],
        pointPlacement: 'on'
    }],
};

// On remplit les options
for (var dict of list_dicts) {
    options.xAxis.categories.push(dict["name"]);
    options.series[0].data.push(dict["nb"]);
}

// On affiche le chart
Highcharts.chart('spiderweb', options);

// TODO le rendre responsive ?

