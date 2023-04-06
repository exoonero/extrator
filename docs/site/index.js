const selectElement = document.querySelector('#municipio-select');

selectElement.addEventListener('change', updateData);

function updateData() {
    const municipio = selectElement.value.toUpperCase();
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        const ano = card.id;
        fetch(`./diarios/${ano.split('-')[1]}/${municipio}.json`)
            .then(response => response.json())
            .then(data => {
                const mediaDiariosMesElement = document.querySelector(`#${ano} #media-diarios-mes`);
                const totalDiariosAnoElement = document.querySelector(`#${ano} #total-diarios-ano`);
                const mediaDiariosMes = data.resumo.media_diarios_mes;
                const totalDiariosAno = data.resumo.total_ano;
                mediaDiariosMesElement.textContent = `Média de diários por mês: ${mediaDiariosMes.toFixed(1)}`;
                totalDiariosAnoElement.textContent = `Total de diários no ano: ${totalDiariosAno}`;
            });
    });
}
updateData()