document.addEventListener('DOMContentLoaded', function() {
    
    const months = JSON.parse(document.getElementById('data-months').textContent);
    const revisions = JSON.parse(document.getElementById('data-revisions').textContent);
    const events = JSON.parse(document.getElementById('data-events').textContent);

    let data = []

    for (let revision in revisions){
        let trace = {
            x: revisions[revision].x,
            y: revisions[revision].y,
            mode: 'line',
            type: 'scatter',
            name: revision,
        }
        data.push(trace)
    }
    let layout = {
        title: "Time Series Chart of Wikipedia Revisions by Month",
        xaxis: {title: "Date"},
        yaxis: {title: "Number of Revisions"},
        hovermode: 'closest'
    }

    function updateChart() {
        let selectedTag = document.getElementById('tagFilter').value;
        layout.shapes = [];

        events.forEach((event) => {
            if (selectedTag === "" || event.tags.includes(selectedTag)){
                layout.shapes.push({
                    type: 'line',
                    x0: event.month,
                    x1: event.month,
                    y0: 0.05,
                    y1: 1,
                    yref: 'paper',
                    line: {
                        color: 'red',
                        width: 2
                    }
                })
            }
        })
        Plotly.newPlot('timeseriesChart', data, layout)
    }

    updateChart()
})