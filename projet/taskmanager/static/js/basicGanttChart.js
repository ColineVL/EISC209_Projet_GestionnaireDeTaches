var options = {
    series: [{
        name: "name",
        data: [{
            name: test,
            start: Date.UTC(2014, 10, 18),
            end: Date.UTC(2014, 10, 20)
        }]
    }]
};
//
// for (var i = 0; i<3; i++) {
//     options.series[0].data.push({
//         name: names[i],
//         start: Date.UTC(starts[i][0], starts[i][1], starts[i][2]),
//         end: Date.UTC(ends[i][0], ends[i][1], ends[i][2]),
//     })
// }

options.series[0].data.push({
    name: 'End prototype',
    start: Date.UTC(2014, 10, 28),
    end: Date.UTC(2014, 10, 30)
})

var chart = new Highcharts.ganttChart('container', options);