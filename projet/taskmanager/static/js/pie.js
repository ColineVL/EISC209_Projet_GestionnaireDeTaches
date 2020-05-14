// On récupère les données utiles
const dico = JSON.parse(document.getElementById('dico').textContent);

// On prépare les données pour le chart
let data = [];
for (var key in dico) {
    data.push({
        name: key,
        y: dico[key]
    });
}
;

// On construit le chart
Highcharts.chart('graph', {
    chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: 'pie'
    },
    title: {
        text: 'Vos tâches classées par statut'
    },
    tooltip: {
        pointFormat: '{series.name}: <b>{point.y}</b>'
    },
    plotOptions: {
        pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
                enabled: false
            },
            showInLegend: true
        }
    },
    series: [{
        name: 'Tâches',
        colorByPoint: true,
        data: data
    }]
});