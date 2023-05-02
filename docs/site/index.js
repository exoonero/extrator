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
        numDiarios.textContent = detalhe_ano ? detalhe_ano.num_diarios: "0";
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
  chart: {
    type: 'bar'
  },
  series: [{
    name: 'sales',
    data: [30,40,35,50,49,60,70,91,125]
  }],
  xaxis: {
    categories: [2014,2015,2016,2017,2018,2019,2020,2021,2022,2023]
  }
}

var chart = new ApexCharts(document.querySelector("#chart"), options);

chart.render();