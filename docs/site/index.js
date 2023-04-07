const selectElement = document.querySelector('#municipio-select');

selectElement.addEventListener('change', updateData);

function createId(nome) {
    var id = nome.trim().toLowerCase().replace(" ", "").normalize('NFD').replace(/[\u0300-\u036f]/g, "");
    return id
}

function updateData() {
    var municipio = selectElement.value;
    municipio = createId(municipio)
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        const ano = card.id;
        fetch(`./diarios/${ano.split('-')[1]}/${municipio}-inicial.json`)
            .then(response => response.json())
            .then(data => {
                const mediaDiariosMesValueElement = document.querySelector(`#${ano} #media-diarios-mes`);
                const totalDiariosAnoValueElement = document.querySelector(`#${ano} #total-diarios-ano`);
                const mediaDiariosMes = data.resumo.media_diarios_mes;
                const totalDiariosAno = data.resumo.total_diarios_ano;
                mediaDiariosMesValueElement.textContent = mediaDiariosMes.toFixed(1);
                totalDiariosAnoValueElement.textContent = totalDiariosAno;
            });
    });
}
updateData()