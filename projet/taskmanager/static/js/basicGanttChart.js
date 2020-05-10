// On récupère les données utiles
const name_project = JSON.parse(document.getElementById('name_project').textContent);
const list_dicts = JSON.parse(document.getElementById('list_dicts').textContent);

// On initialise les options du chart
const options = {
    series: [{
        name: name_project,
        data: []
    }]
};

// On remplit les options
for (var dict of list_dicts) {
    let start = dict["start"];
    let end = dict["end"];
    options.series[0].data.push({
        name: dict["name"],
        start: Date.UTC(start[0], start[1], start[2]),
        end: Date.UTC(end[0], end[1], end[2])
    })
}

// On affiche le chart
Highcharts.ganttChart('gantt', options);