document.getElementById('stockForm').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent form from submitting the traditional way

    // Get form inputs
    const ticker = document.getElementById('ticker').value;
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;

    // Update API URL with full address (change the port if necessary)
    const apiUrl = `http://localhost:8080/api/?tk=${ticker}&stdate=${startDate}&eddate=${endDate}`;

    // Fetch data from your Flask API
    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            const dates = data.map(item => item.record_date);
            const closeValues = data.map(item => item.close_value);

            // Use Plotly to create the graph
            const trace = {
                x: dates,
                y: closeValues,
                type: 'scatter',
                mode: 'lines',
                name: `${ticker} Stock`
            };

            const layout = {
                title: `${ticker} Stock Prices from ${startDate} to ${endDate}`,
                xaxis: { title: 'Date' },
                yaxis: { title: 'Price' }
            };

            Plotly.newPlot('graph', [trace], layout);
        })
        .catch(error => console.error('Error fetching data:', error));
});
