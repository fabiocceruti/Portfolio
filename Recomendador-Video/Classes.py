"""
Arquivo criado para definir as funções necessárias para coletar os vídeos novos do youtube e fazer as predições

"""

#Importando as bibliotecas
import sqlite3 as sql
import youtube_dl
import joblib as jb
import pandas as pd
from scipy.sparse import hstack, csr_matrix
import numpy as np
import json

#Classe com funções para gerar o recomendador de vídeos de Youtube
class RecomendadorYoutube :

    #Definindo algumas variáveis globais sem modificar pela instância
    queries = ["machine+learning", "data+science", "kaggle"]
    db_name = 'videos_youtube.db'
    lista_videos = []
    mdl_rl = jb.load('Models/logistic_reg.pkl.z')
    mdl_lgbm = jb.load('Models/lgbm.pkl.z')
    title_vec = jb.load('Models/title_vectorizer.pkl.z')

    def __init__(self, qtd_videos, qtd_videos_front_end):

        #Recebe a quantidade de videos para realizar a busca
        self.qtd_videos = qtd_videos
        self.qtd_videos_front_end = qtd_videos_front_end

    #Função para criar o banco de dados
    def Create_Conection(self):

        #Criando a conexão com o banco de dados
        with sql.connect(RecomendadorYoutube.db_name) as conn:
            
            c = conn.cursor()
            c.execute('''CREATE TABLE videos
                         (title text, video_id text, score real)''') #Criando a tabela dentro do banco de dados
            conn.commit()
        
        return True
    
    #Função para pegar as informações
    def Update_Data(self):

        #Instanciando o youtube-dl
        ydl = youtube_dl.YoutubeDL({"ignoreerrors": True})

        #Criando a conexão com o banco de dados
        with sql.connect(RecomendadorYoutube.db_name) as conn:

            #Rodando um loop entre as queries
            for query in RecomendadorYoutube.queries:

                #Extraindo as 20 últimas consultas
                extract_info = ydl.extract_info("ytsearchdate{qtd_videos}:{query}".format( qtd_videos = self.qtd_videos , query = query), download = False)

                #Roda um for para cada entrada de dados -> entries (chave a onde possui as informações que precisamos)
                for entry in extract_info['entries'] :
        
                    #Verifica se não é um vídeo indisponível (para estes casos retorna um valor vazio sem a chave entry)
                    if entry is not None :
                
                        #Armazena o assunto da query
                        entry['query'] = query
        
                #Armazena as informações das buscas
                RecomendadorYoutube.lista_videos += (extract_info['entries'])
            
            #Retira os valores vazios recebidos quando o vídeo está indisponível
            RecomendadorYoutube.lista_videos = [info for info in RecomendadorYoutube.lista_videos if info is not None]

            #Tratamento dos dados
            data_processed = self.Data_Processing(RecomendadorYoutube.lista_videos)

            #Criando as features para as predições
            X = self.Create_Features(data_processed)

            #Realizando as predições
            probabilidade = self.Predict_Proba(X)

            #Criando um dicionário com as informações
            data_front = {'title': data_processed['title'].replace("'",""),
                          'video_id': data_processed['webpage_url'],
                          'score': probabilidade  }
            
            #Criando um loop para inserir os dados no banco
            for line in range(0, len(probabilidade)):

                c = conn.cursor()

                c.execute("INSERT INTO videos VALUES (?, ?, ? )", (data_front['title'][line], data_front['video_id'][line] , round(data_front['score'][line],4)))

                conn.commit()
            
        return True 

    #Função para tratar os dados
    def Data_Processing(self, data):

        #Transformando os dados em um Dataframe
        df = pd.DataFrame(data)

        #Deletando as linhas duplicadas -> Pode aparecer um mesmo vídeo para mais de uma query
        #df.drop_duplicates(subset = ['webpage_url'],inplace = True)

        #Deletando as linhas que estão com valores ausentes
        df.dropna(axis = 0, subset = ['upload_date', 'view_count', 'query'], inplace = True)

        #Convertendo as variável upload_date para datetime
        df['upload_date'] = pd.to_datetime(df['upload_date'])

        #Retorna o DataFrame tratado
        return df

    def Create_Features(self, data, default = 0):

        #Criando um default caso seja para avaliar apenas um vídeo
        if default == 0:
        
            #Criando um dataframe de features
            features = pd.DataFrame(index = data.index)
        
        else :

            #Criando um dataframe de features
            features = pd.DataFrame(index = [0])

            #Transformando em datetime
            data['upload_date'] = pd.to_datetime(data['upload_date'])

        #Criando a feature de diferença diária
        features['tempo_desde_pub'] = (pd.Timestamp.today() - data['upload_date'])/np.timedelta64(1, 'D')

        #Armazenando as views
        features['views'] = data['view_count']

        #Fazendo o cálculo de views por dia
        features['views_por_dia'] = features['views'] / features['tempo_desde_pub']

        #Deletando a variável tempo_desde_pub
        features.drop(['tempo_desde_pub'], axis = 1, inplace = True)

        #Criando a variável de título
        title = data['title']

        #Vetorizando o título
        title_bow = RecomendadorYoutube.title_vec.transform(title)

        #Juntando as matrizes
        features_final = hstack([features, title_bow])

        #Retorna as features tratadas
        return features_final

    def Predict_Proba(self, X):

        #Fazendo as predições da regressão logística + LGBM
        p_lr = RecomendadorYoutube.mdl_rl.predict_proba(X)[:, 1]
        p_lgbm = RecomendadorYoutube.mdl_lgbm.predict_proba(X)[: , 1]

        #Calculando a ensemble das duas com base em uma média ponderada
        p_final = 0.3 * p_lr + 0.7 * p_lgbm 

        #Retornando a probabilidade
        return p_final
    
    def Get_Predictions(self):

        #Cria uma lista para armazenar os dados
        videos = []

        #Faz uma conexão com o banco de dados
        with sql.connect(RecomendadorYoutube.db_name) as conn:

            c = conn.cursor()

            #loop entre as linhas
            for line in c.execute("SELECT * FROM videos"):

                #Cria um dicionário
                line_dict = {'title': line[0],
                             'video_id': line[1],
                             'score': line[2]}
                
                #Armazena em uma lista
                videos.append(line_dict)
            
        #Cria uma lista para as predições
        predictions = []

        #Cria um loop em relação a lista de videos
        for video in videos:

            #Armazena os valores
            predictions.append((video['video_id'], video['title'], float(video['score'])))

        #Ordena entre os maiores scores de acordo com o que foi passado
        predictions = sorted(predictions, key = lambda x: x[2], reverse = True)[: self.qtd_videos_front_end]

        #Cria uma lista para formatar as previsões em forma de html
        #predictions_formatted = []

        #Cria um loop
        #for e in predictions:

            #Armazenando as predições em forma de html
            #predictions_formatted.append("<tr><th><a href=\"{link}\">{title}</a></th><th>{score}</th></tr>".format(title=e[1], link=e[0], score=e[2]))

        #return '\n'.join(predictions_formatted)
        return predictions