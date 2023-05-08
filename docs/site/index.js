const selectElement = document.querySelector("#municipio-select");

selectElement.addEventListener("change", updateData);

function updateData() {
  var municipio = selectElement.value;
  console.log(municipio);

  const cards = document.querySelectorAll(".card");
  cards.forEach((card) => {
    const ano = card.id.replace("ano-", "");
    fetch(`./dados/inicial/${municipio}-inicial.json`)
      .then((response) => response.json())
      .then((data) => {
        const detalhe_ano = data.detalhe[ano];
        const numDiarios = document.querySelector(`#ano-${ano} #num-diarios`);
        numDiarios.textContent = detalhe_ano ? detalhe_ano.num_diarios : "0";
        const numExoneracoes = document.querySelector(
          `#ano-${ano} #num-exoneracoes`
        );
        numExoneracoes.textContent = detalhe_ano ? detalhe_ano.num_exoneracoes : "0";
        const numNomeacoes = document.querySelector(
          `#ano-${ano} #num-nomeacoes`
        );
        numNomeacoes.textContent = detalhe_ano ? detalhe_ano.num_nomeacoes : "0";
      });
  });
}
updateData();

var options = {
  series: [
    {
      name: "Nomeações",
      data: [30, 40, 45, 50, 49, 60, 70, 91, 24, 56]
    },
    {
      name: "Exonerações",
      data: [23, 31, 33, 42, 48, 32, 51, 36, 30, 56]
    }
  ],
  chart: {
    type: 'bar',
    height: 230
  },
  legend: {
    position: 'top',
    horizontalAlign: 'center',
    containerMargin: {
      right: 20
    },
    markers: {
      width: 12,
      height: 12,
      padding: 12,
      radius: 12,
      offsetX: 12,
    },
    itemMargin: {
      horizontal: 150
    },
    fontSize: 16,
    fontFamily: "Source Sans Pro, sans-serif"
  },
  plotOptions: {
    bar: {
      horizontal: false,
      borderRadius: 5,
      columnWidth: '40%',
      endingShape: 'rounded'
    }
  },
  dataLabels: {
    enabled: false
  },
  stroke: {
    show: true,
    width: 1.5,
    colors: ['transparent']
  },
  xaxis: {
    categories: ['2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023'],
    labels: {
      style: {
          fontFamily: 'Source Sans Pro, sans-serif',
          fontSize: 15,
          fontWeight: 700,
      }}
  },
  grid: {
    show: false
  },
  fill: {
    opacity: 1
  },
  tooltip: {
    y: {
      formatter: function (val) {
        return val + " pessoas"
      }
    }
  },
  colors: ['#57C5ED', '#EC6666']
};

var chart = new ApexCharts(document.querySelector("#chart"), options);
chart.render();