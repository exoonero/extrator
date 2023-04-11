const selectElement = document.querySelector('#municipio-select');

selectElement.addEventListener('change', updateData);

function updateData() {
    var municipio = selectElement.value;
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        const ano = card.id;
        fetch(`./dados/inicial/${municipio}-inicial.json`)
            .then(response => response.json())
            .then(data => {
                const numDiariosAnoValueElement = document.querySelector(`#${ano} #num-diarios`);
                const detalhe_ano = data.detalhe[ano]
                const numDiariosAno = detalhe_ano.num_diarios;
                numDiariosAnoValueElement.textContent = numDiariosAno;
            });
    });
}
updateData()