[![author](https://img.shields.io/badge/author-fabiocceruti-red.svg)](https://www.linkedin.com/in/fabio-corr%C3%AAa-ceruti-32ab704b/) [![](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/release/python-365/) [![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://perso.crans.org/besson/LICENSE.html) [![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/carlosfab/data_science/issues)

<p align="center">
  <img src="https://github.com/fabiocceruti/Portfolio/blob/main/Banner_Principal_Ajustado.png?raw=true" >
  <a href="http://www.freepik.com">Designed by starline / Freepik</a>
</p>

# Recomendador de Vídeo do Youtube

Este projeto foi baseado no curso de [Como criar uma solução completa de Data Science | Mario Filho](http://mariofilho.com/curso/).

O **Recomendador de Vídeo** foi desenvolvido no curso passando por todas etapas desde a coleta dos dados até o deploy no Heroku.

Acesse a aplicação disponível no Heroku: [Recomendador de Vídeo - Fabio Ceruti](http://recomendador-video-fabioceruti.herokuapp.com/)

## Estrutura do Projeto

### Definição do Problema

Antes de iniciar qualquer projeto de Data Science, devemos ter de forma clara qual problema queremos resolver. Para isto, foi preciso realizar as seguintes perguntas:
- **Qual o problema?** R: Gasto tempo demais buscando novos vídeos no youtube a respeito de *Data Science*.
- **Qual a solução ideal?** R: Ter uma lista com apenas vídeos que realmente gosto sobre *Data Science*.
- **Como podemos resolver este problema, utilizando conhecimento de *Data Science*?** R: Criar um sistema de recomendação de vídeos do Youtube com base no meu gosto.
- **Como a solução será usada em produção (deploy)?** R: Utilizar uma abordagem de "ponto de corte", ou seja, apresentar os 30 vídeis mais relavantes de acordo com meu gosto.
- **Como validar a implementação?**
  - Métrica primária: Dos top N vídeos, quantos coloco na lista de *watch later*.
  - Métrica secundária: Quanto tempo passo selecionando vídeos.

### Preparação dos Dados e Análise dos dados

A coleta de dados foi realizada, utilizando uma biblioteca chamada [youtube_dl](https://youtube-dl.org/). O projeto inicial consistia em realizar um scrapy da página do youtube, porém, existia o risco da mudança da estrutura da página e futuramente o projeto "quebrar". Portanto, com o objetivo de conservar o processo de coleta de dados, foi decidido utilizar esta biblioteca.

Os dados foram obtidos com base em três buscas de interesse (query):
- Machine learning;
- Data Scince;
- Kaggle.

Vale destacar que foram coletados 2000 vídeos mais recentes para cada busca de interesse.

```
extract_info = ydl.extract_info("ytsearchdate2000:{query}".format(query = query), download = False)
```
Após a coleta, foi realizada uma etapa de *labeling* manual em que avaliei cada título de vídeo coletado para classificá-lo em 0 (*dislike*) ou 1 (*like*). Além disso, foi necessário realizar tratamento de dado para excluir vídeos duplicados e dados com valores ausentes.

Na fase de feature engineering, foram criadas as seguintes variáveis:
- Visualizações por dia; e 
- Palavras vetorizadas do título a partir do método **TfidfVectorizer** do Scikit-Learn.

Por fim, foram utilizadas as variáveis mencionadas acima e a variável visualizações para a modelagem. É importante ressaltar que a ideia deste projeto é construir um modelo simples e que seja eficiente.

### Modelagem

Nesta fase, utilizamos os seguintes modelos de *machine learning*:
- Regressão logística;
- LighGBM;
- Random forest.

Para sua avaliação, escolhemos as métricas que não utilizam ponto de corte. Portanto, usamos a **average_precision** e **ROC_AUC**, dando maior importância para a primeira métrica.

Na etapa envolvendo *tunning* dos hiperparâmetros, utilizamos o conjunto de argumentos do modelo e do algoritmo de vetorização do título (TfidfVectorizer). 

Verificamos que o modelo que consegue o melhor valor para métrica **average_precision** é um ensemble entre a regressão logística e o lightGBM.

```
Ensemble final = 0.3 * Probabilidade_Regressão_Logistica + 0.7 * Probabilidade_LighGBM
```

### Entrega do Projeto Final (Deploy)


