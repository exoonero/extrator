const selectElement = document.querySelector('#municipio-select');

selectElement.addEventListener('change', updateData);

function updateData() {
    var municipio = selectElement.value;
    console.log(municipio)

    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        const ano = card.id.replace('ano-', '');
        fetch(`./dados/inicial/${municipio}-inicial.json`)
            .then(response => response.json())
            .then(data => {
                const detalhe_ano = data.detalhe[ano]

                const numDiarios = document.querySelector(`#ano-${ano} #num-diarios`);
                numDiarios.textContent = detalhe_ano.num_diarios;

                const numExoneracoes = document.querySelector(`#ano-${ano} #num-exoneracoes`);
                numExoneracoes.textContent = detalhe_ano.num_exoneracoes;

                const numNomeacoes = document.querySelector(`#ano-${ano} #num-nomeacoes`);
                numNomeacoes.textContent = detalhe_ano.num_nomeacoes;
            });
    });
}
updateData()