// THE CHART
var myChart = Highcharts.ganttChart('container', {
    title: {
        text: 'Gantt Chart with Progress Indicators'
    },
    xAxis: {
        min: Date.UTC(2014, 10, 17),
        max: Date.UTC(2014, 10, 30)
    },

    series: [{
        name: 'Project 1',
        data: [{
            name: 'Start prototype',
            start: Date.UTC(2014, 10, 18),
            end: Date.UTC(2014, 10, 25),
            completed: 0.25
        }]
    }]

});


