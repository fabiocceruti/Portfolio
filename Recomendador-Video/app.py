"""

Arquivo principal:

"""

#Importando bibliotecas
from flask import Flask, request, render_template
from Classes import RecomendadorYoutube


#Instanciando o Flask
app = Flask(__name__)

#Instanciando a classe de recomendação de vídeo
recomendador = RecomendadorYoutube(50,30)

@app.route('/')
def main_page():

    #Trazendo as predições
    preds = recomendador.Get_Predictions()
    
    #Renderizando a tabela com scores em html
    return render_template('index.html', predictions = preds)


#Roda API
if __name__ == '__main__':

    app.run(debug = True, host = '0.0.0.0')