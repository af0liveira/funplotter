const ctx = document.getElementById('plotCanvas').getContext('2d');
const lineChart = new Chart(ctx, {
  type: 'line',
  data: {
    datasets: dataSets, // NOTE: `dataSets` should be defined in `document`
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    elements: {
      point: {
        pointStyle: false
      }
    },
    scales: {
      x: {
        type: 'linear',
        position: 'bottom',
        title: {
          display: true,
          text: 'x'
        }
      },
      y: {
        type: 'linear',
        position: 'left',
        title: {
          display: true,
          text: 'f(x)'
        }
      }
    }
  }
});
