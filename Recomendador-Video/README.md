[![author](https://img.shields.io/badge/author-fabiocceruti-red.svg)](https://www.linkedin.com/in/fabio-corr%C3%AAa-ceruti-32ab704b/) [![](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/release/python-365/) [![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://perso.crans.org/besson/LICENSE.html) [![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/carlosfab/data_science/issues)

<p align="center">
  <img src="https://github.com/fabiocceruti/Portfolio/blob/main/Banner_Principal_Ajustado.png?raw=true" >
  <a href="http://www.freepik.com">Designed by starline / Freepik</a>
</p>

# Recomendador de Vídeo do Youtube

Este projeto foi baseado no curso de [Como criar uma solução completa de Data Science | Mario Filho](http://mariofilho.com/curso/).

O **Recomendador de Vídeo** foi desenvolvido no curso passando por todas etapas desde a coleta dos dados até o deploy no Heroku.

Acesse a aplicação disponível no Heroku: [Recomendador de Vídeo - Fabio Ceruti](http://recomendador-video-fabioceruti.herokuapp.com/)

<p align="center" style="margin-bottom: -10px">
    <img src="gif/gif.gif" alt="Gif Demonstrativo">
    <p align="center" style="font-size: 12px">Gif Demonstrativo</p>
</p>

## Ferramentas utilizadas

Foram utilizadas as seguintes ferramentas na criação e execução do projeto:

- Linguagem de programação: Python
- IDE de desenvolvimento: Jupyter Lab e Visual Studio Code
- Pacotes e Frameworks: 
    - Flask==2.0.1
    - gunicorn==20.1.0
    - joblib==1.0.1
    - lightgbm==3.2.1
    - numpy==1.20.3
    - pandas==1.2.4
    - requests==2.25.1
    - scikit-learn==0.23.2
    - scipy==1.6.3
    - youtube-dl==2021.6.6
- Linguagens e Frameworks usados no front-end:
    - HTML e CSS
    - Bootstrap
- Ferramenta de conteinerização: Docker
- Plataforma de hospedagem em nuvem: Heroku
- Ferramentas auxiliares:
    - Anaconda e Microsoft Excel

## Estrutura do Projeto

### 1.Definição do Problema

Antes de iniciar qualquer projeto de Data Science, devemos ter de forma clara qual problema queremos resolver. Para isto, foi preciso realizar as seguintes perguntas:
- **Qual o problema?** R: Gasto tempo demais buscando novos vídeos no youtube a respeito de *Data Science*.
- **Qual a solução ideal?** R: Ter uma lista com apenas vídeos que realmente gosto sobre *Data Science*.
- **Como podemos resolver este problema, utilizando conhecimento de *Data Science*?** R: Criar um sistema de recomendação de vídeos do Youtube com base no meu gosto.
- **Como a solução será usada em produção (deploy)?** R: Utilizar uma abordagem de "ponto de corte", ou seja, apresentar os 30 vídeis mais relavantes de acordo com meu gosto.
- **Como validar a implementação?**
  - Métrica primária: Dos top N vídeos, quantos coloco na lista de *watch later*.
  - Métrica secundária: Quanto tempo passo selecionando vídeos.

### 2.Preparação dos Dados e Análise dos dados

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

### 3.Modelagem

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

### 4.Entrega do Projeto Final (Deploy)

O *deploy* do processo de *Data Science* foi realizado através do **Flask** e hospedado no [Heroku](http://recomendador-video-fabioceruti.herokuapp.com/). Todo o processo realizado desde a fase de coletagem até a predição foi feita em python e colocada em produção. É importante ressaltar que criamos uma classe em python para programar todas as funções/etapas necessárias para realizar a predição. Além disso, conforme mencionado anteriormente, foi construída uma listagem do 30 vídeos mais relevantes com base no meu gosto. 
Esta listagem foi renderizada em uma página HTML.

-------------------------------------------------------

### 📡 Onde me encontrar?

[<img align="left"  width="22px" src="https://cdn.jsdelivr.net/npm/simple-icons@3.4.0/icons/linkedin.svg" />](https://www.linkedin.com/in/fabio-ceruti/)
[<img align="left"  width="22px" src="https://cdn3.iconfinder.com/data/icons/colorful-guache-social-media-logos-1/159/social-media_web-512.png" />](https://fabioceruti.tech/)
[<img align="left" alt="fabiocceruti | medium" width="22px" src="https://cdn.jsdelivr.net/npm/simple-icons@3.4.0/icons/medium.svg" />](https://fabiocceruti.medium.com/)
[<img align="left" alt="fabio_cceruti | Instagram" width="22px" src="https://cdn4.iconfinder.com/data/icons/picons-social/57/38-instagram-2-512.png" />](https://www.instagram.com/fabio_cceruti/)
<br/>

Convido a você para se conectar comigo se inscrevendo em meu [site](https://fabioceruti.tech/) e nas demais redes para acompanhar as minhas publicações sobre a área de dados. 

<img align="left" alt="ceruti.tech | gmail" width="22px" src="https://cdn1.iconfinder.com/data/icons/logos-and-brands-3/512/147_Gmail_logo_logos-512.png" />*ceruti.tech@gmail.com*


