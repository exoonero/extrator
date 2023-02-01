# Monitoramento de atos do executivo municipal de Alagoas a partir dos diários oficiais

Este projeto é financiado pelo [Instituto Federal de Alagoas (IFAL)](https://www2.ifal.edu.br/) através do projeto de pesquisa PVA328-2022. Além do financiamento, o projeto conta com apoio da [Open Knowledge Brasil (OKBR)](https://ok.org.br/), no âmbito de uma [parceria com foco no projeto Querido Diário](https://ok.org.br/noticia/querido-diario-nas-universidades-okbr-lanca-chamada-para-parcerias-em-projetos-de-ciencia-de-dados/). O projeto teve início em agosto 2022 e terá até 12 meses de duração.

O projeto conta com os seguintes integrantes:
- [Alex Custódio](https://github.com/alex-custodio): discente do curso técnico de Informática do IFAL campus Arapiraca
- [Emanuel Lucas da Silva](https://github.com/emanuelucas04): discente do curso técnico de Informática do IFAL campus Arapiraca
- [Daniel Fireman](https://github.com/danielfireman): professor do IFAL campus Arapiraca
- [Felipe Alencar](https://github.com/felipealencar): professor do IFAL campus Arapiraca
- [Luisa Coelho](https://github.com/luisa-coelho): bolsista PCDaS

O projeto tem como principal objetivo coletar, transformar em texto e separar em municípios os diários oficiais municipais da [Associação dos Municípios Alagoanos (AMA)](https://www.diariomunicipal.com.br/ama/). Além da separação do conteúdo por município, o texto do diário de cada ente estadual é separado em atos normativos. Também iremos utilizar algoritmos computacionais para classificar e extrair informações dos atos normativos dos diários de cada município. Mais especificamente, o nosso foco será em nomeações e exonerações.

Também buscamos alguns requisitos não-funcionais:
- **Simplicidade**: ela se traduziu em uma análise de diversos casos, onde chegamos a conclusão que poderíamos utilizar expressões regulares (ao invés de inteligência computacional, por exemplo);
- **Facilidade de utilização do código pelo QD**: com a ajuda da busca pela simplicidade, o objetivo é depender o mínimo possível de bibliotecas de terceiros e focar numa API de clara e com boa documentação;
- **Replicabilidade do código para outros estados/associações de municípios**: prevemos que a solução possa ser utilizada em outros contextos apenas modificando as expressões regulares.

Além destes, todo o código produzido é aberto e distribuído de forma livre no repositório [danielfireman/ifal-qd](https://github.com/danielfireman/ifal-qd).

Para tornar mais fácil o acompanhamento, o projeto foi dividido em duas fases. A primeira fase tem como principal objetivo propor e avaliar um algoritmo que permita a separação do conteúdo do diário oficial da [Associação dos Municípios Alagoanos (AMA)](https://www.diariomunicipal.com.br/ama/) por município. A segunda fase diz respeito a extração e monitoramento de informações relevantes, por exemplo, nomeações e exonerações.

## Fase 1: Separação do conteúdo diários oficiais da AMA em municípios

Essa fase foi executada com sucesso entre agosto e dezembro de 2022. Seu objetivo foi coletar, transformar em texto e separar em municípios os diários oficiais municipais da [Associação dos Municípios Alagoanos (AMA)](https://www.diariomunicipal.com.br/ama/). Além da separação do conteúdo por município, o texto do diário de cada ente estadual é separado em atos normativos.

Esse foi objetivo foi atingido com a execução das seguintes etapas:

1. Através do software Apache Tika é possível transformar o diário que está em formato PDF em texto ASCII e então é possível ter o primeiro conjunto de dados;
1. A partir do texto completo do diário, utilizamos um algoritmo baseado em expressão regular para separar o conteúdo por municípios. A partir daí temos o texto dos diários oficiais de cada município;
1. O texto de cada diário é então processado e separado em atos normativos. Essa etapa também é realizada utilizando um algoritmo baseado em expressões regulares.

Para aumentar a confiança na solução proposta, testamos com sucesso 25 diários, com amostra todos os anos entre 2014 e 2022. Os testes realizam as seguintes checagens:
- Data de publicação do diário;
- Municípios incluídos em cada diário;
- Atos dos diários de cada município.

A OKBR planeja integrar esses algoritmos ao projeto Querido Diário a partir de janeiro de 2023. Dessa forma será possível coletar continuamente os diários dos 102 municípios alagoanos e disponibilizá-los na plataforma, permitindo consultas e habilitando análises mais ricas.

O sucesso na execução da primeira etapa da deste projeto reforça que o potencial da inclusão de instituições de nível técnico na parceria IFAL-OKBR. 

## Fase 2: Classificação dos atos normativos -- nomeações e exonerações

A segunda etapa do projeto foi iniciada em dezembro 2022. O principal objetivo dessa etapa é utilizar algoritmos computacionais para classificar e extrair informações dos atos normativos dos diários de cada município. Mais especificamente, o nosso foco será em nomeações e exonerações.

Publicaremos mais informações sobre essa etapa a medida que ela transcorra. Fiquem atentos/as!
