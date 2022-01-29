from ast import keyword
from re import search
from shutil import ExecError
from time import time
from flask import Flask, make_response,redirect, render_template, request, url_for, session,jsonify
import secrets
import googlemaps
import pandas as pd
import openpyxl
import json
import time

app = Flask(__name__)


API_KEY = 'AIzaSyDviKMu_KGmMJqsMKrioJUZ3jIjpVr9Q5M'
map_client = googlemaps.Client(API_KEY)

secret_key = secrets.token_hex(16)
# example output, secret_key = 000d88cd9d90036ebdd237eb6b0db000
app.config['SECRET_KEY'] = secret_key

global search_string


@app.route("/")
def index():
    return render_template('index.html')

@app.route('/teste', methods=["GET","POST"])
def teste():
    dado_um = request.form['um']
    dado_2 = request.form['dois']
    dado_3 = request.form['tres']
    dado_4 = request.form['quatro']
    dado_5 = request.form['cinco']
    dado_6 = request.form['lat']
    dado_7 = request.form['lng']
    
    
    if dado_6 == "" or dado_7=="":
        return redirect(url_for('index'))
    # session['escolha_um'] = dado_um
    # session['escolha_2'] = dado_2
    # session['escolha_3'] = dado_3
    # session['escolha_4'] = dado_4
    # session['escolha_5'] = dado_5
    # session['escolha_LAT'] = dado_6
    # session['escolha_LNG'] = dado_7
    dicionario_escolha = {
        'dado_um':dado_um,
        'dado_2':dado_2,
        'dado_3':dado_3,
        'dado_4':dado_4,
        'dado_5':dado_5,
        'dado_6_LAT':dado_6,
        'dado_7_LNG':dado_7,
    }
    print(dicionario_escolha)
    session['escolha'] = dicionario_escolha

    
    return redirect(url_for('pagina_dados'))


def primeira_opcaao_dados():
    escolha = session['escolha']
    lat = escolha['dado_6_LAT']
    lng = escolha['dado_7_LNG']
    location = (lat, lng)        
    search_string = escolha['dado_um']
    print("SEARCH STRING>>>_____----, "+search_string)        
    distance = 500 #Aqui tem que dar algum jeito do usuario escolher a distância
    response_ = map_client.places_nearby(
        location=location,
        keyword=search_string,
        name=escolha['dado_um'],
        radius=distance,
    )
    df = pd.DataFrame(response_['results'])
    df['photos'].fillna('...', inplace=True)
    #df.to_excel('lista.xlsx')
    ##--------------
    ### NOME
    lista_geral = []
    lista_geral.append(df['name'].values)
    lista_nova = lista_geral[0]
    lista_final_nomes = {
        'lista':list(lista_nova)
    }
    ##--------------
    ### location
    lista_primeiraopcao_location = df['geometry'].values
    lista_primeiraopcao_location=json.dumps(list(lista_primeiraopcao_location))
    teste = json.loads(lista_primeiraopcao_location)
    lista_final_primeiraopcao_locaiton = []
    dicio_primeiraopcao_location = []
    for item in teste:
        dicio_primeiraopcao_location.append(item['location'])       
    lista_final_primeiraopcao_locaiton= {
        'lista':list(dicio_primeiraopcao_location)
    }
    #print(session['lista_final_primeiraopcao_locaiton'])
    ##--------------
    ### endereco
    lista_primeiraopcao_endereco = df['vicinity'].values
    dicio_lista_primeiraopcao_endereco = {
        'lista': list(lista_primeiraopcao_endereco)
    }
    #print(session['lista_primeiraopcao_endereco'])
    ##--------------
    ### fotos
    #print(session['lista_primeiraopcao_fotos'])
    ##--------------
    ### rating
    lista_primeiraopcao_rating = df['rating'].values
    dicio_lista_primeiraopcao_rating = {
        'lista': list(lista_primeiraopcao_rating)
    }    
    #print(session['lista_primeiraopcao_rating'])

    #session['lista_final_nomes'] = lista_final_nomes
    #session['lista_final_primeiraopcao_locaiton'] = lista_final_primeiraopcao_locaiton
    #session['lista_primeiraopcao_endereco'] = dicio_lista_primeiraopcao_endereco
    #session['lista_primeiraopcao_fotos'] = dic_primeiraopcao_fotos
    #session['lista_primeiraopcao_rating'] = dicio_lista_primeiraopcao_rating
    try:
        lista_primeiraopcao_fotos = df['photos'].values
        lista_primeiraopcao_fotos_json_dumps=json.dumps(list(lista_primeiraopcao_fotos))
        lista_primeiraopcao_fotos_json_loads = json.loads(lista_primeiraopcao_fotos_json_dumps)
        lista_primeiraopcao_fotos= []
        for item in lista_primeiraopcao_fotos_json_loads:
            lista_primeiraopcao_fotos.append(item)
        dic_primeiraopcao_fotos= {
            'lista':list(lista_primeiraopcao_fotos)
        }
        final_primeiraopcao_fotos_dois = []
        # print(dic_primeiraopcao_fotos['lista'])
        # print('-------')
        for item in dic_primeiraopcao_fotos['lista']:
            if item == '...':
                src = 'https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/restaurant-71.png'
            else:
                src = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference='+item[0]['photo_reference']+'&key='+API_KEY
            final_primeiraopcao_fotos_dois.append(src)
    except Exception as e:
        final_primeiraopcao_fotos_dois = []
        src = 'https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/restaurant-71.png'
        final_primeiraopcao_fotos_dois.append(src)

    lista_total = {
    'lista_primeiraopcao_nome':lista_final_nomes,
    'lista_final_primeiraopcao_locaiton':lista_final_primeiraopcao_locaiton,
    'lista_primeiraopcao_endereco':dicio_lista_primeiraopcao_endereco,
    'lista_total_primeiraopcao_fotos':final_primeiraopcao_fotos_dois,
    'lista_primeiraopcao_rating':dicio_lista_primeiraopcao_rating

    }
    return lista_total

def segunda_opcao_dados():
    escolha = session['escolha']
    lat = escolha['dado_6_LAT']
    lng = escolha['dado_7_LNG']
    location = (lat, lng)        
    search_string = escolha['dado_2']  
    print("SEARCH STRING>>>_____----, "+search_string)      
    distance = 500 #Aqui tem que dar algum jeito do usuario escolher a distância
    response_ = map_client.places_nearby(
        location=location,
        keyword=search_string,
        name=escolha['dado_2'],
        radius=distance,
    )
    df = pd.DataFrame(response_['results'])
    df['photos'].fillna('...', inplace=True)
    #df.to_excel('lista.xlsx')
    ##--------------
    ### NOME
    lista_geral = []
    lista_geral.append(df['name'].values)
    lista_nova = lista_geral[0]
    lista_final_nomes = {
        'lista':list(lista_nova)
    }
    ##--------------
    ### location
    lista_primeiraopcao_location = df['geometry'].values
    lista_primeiraopcao_location=json.dumps(list(lista_primeiraopcao_location))
    teste = json.loads(lista_primeiraopcao_location)
    lista_final_primeiraopcao_locaiton = []
    dicio_primeiraopcao_location = []
    for item in teste:
        dicio_primeiraopcao_location.append(item['location'])       
    lista_final_primeiraopcao_locaiton= {
        'lista':list(dicio_primeiraopcao_location)
    }
    #print(session['lista_final_primeiraopcao_locaiton'])
    ##--------------
    ### endereco
    lista_primeiraopcao_endereco = df['vicinity'].values
    dicio_lista_primeiraopcao_endereco = {
        'lista': list(lista_primeiraopcao_endereco)
    }
    #print(session['lista_primeiraopcao_endereco'])
    #print(session['lista_primeiraopcao_fotos'])
    ##--------------
    ### rating
    lista_primeiraopcao_rating = df['rating'].values
    dicio_lista_primeiraopcao_rating = {
        'lista': list(lista_primeiraopcao_rating)
    }    
    #print(session['lista_primeiraopcao_rating'])

    #session['lista_final_nomes'] = lista_final_nomes
    #session['lista_final_primeiraopcao_locaiton'] = lista_final_primeiraopcao_locaiton
    #session['lista_primeiraopcao_endereco'] = dicio_lista_primeiraopcao_endereco
    #session['lista_primeiraopcao_fotos'] = dic_primeiraopcao_fotos
    #session['lista_primeiraopcao_rating'] = dicio_lista_primeiraopcao_rating
    ##--------------
    ### fotos
    try:
        lista_primeiraopcao_fotos = df['photos'].values
        lista_primeiraopcao_fotos_json_dumps=json.dumps(list(lista_primeiraopcao_fotos))
        lista_primeiraopcao_fotos_json_loads = json.loads(lista_primeiraopcao_fotos_json_dumps)
        lista_primeiraopcao_fotos= []
        for item in lista_primeiraopcao_fotos_json_loads:
            lista_primeiraopcao_fotos.append(item)
        dic_primeiraopcao_fotos= {
            'lista':list(lista_primeiraopcao_fotos)
        }
        final_primeiraopcao_fotos_dois = []
        # print(dic_primeiraopcao_fotos['lista'])
        # print('-------')
        for item in dic_primeiraopcao_fotos['lista']:
            if item == '...':
                src = 'https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/restaurant-71.png'
            else:
                src = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference='+item[0]['photo_reference']+'&key='+API_KEY
            final_primeiraopcao_fotos_dois.append(src) 
   
    except Exception as e:
        final_primeiraopcao_fotos_dois = []
        src = 'https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/restaurant-71.png'
        final_primeiraopcao_fotos_dois.append(src)

    lista_total = {
    'lista_primeiraopcao_nome':lista_final_nomes,
    'lista_final_primeiraopcao_locaiton':lista_final_primeiraopcao_locaiton,
    'lista_primeiraopcao_endereco':dicio_lista_primeiraopcao_endereco,
    'lista_total_primeiraopcao_fotos':final_primeiraopcao_fotos_dois,
    'lista_primeiraopcao_rating':dicio_lista_primeiraopcao_rating

    }
    return lista_total

def terceira_opcao_dados():
    escolha = session['escolha']
    lat = escolha['dado_6_LAT']
    lng = escolha['dado_7_LNG']
    location = (lat, lng)        
    search_string = escolha['dado_3']     
    print("SEARCH STRING>>>_____----, "+search_string)   
    distance = 500 #Aqui tem que dar algum jeito do usuario escolher a distância
    response_ = map_client.places_nearby(
        location=location,
        keyword=search_string,
        name=escolha['dado_3'],
        radius=distance,
    )
    df = pd.DataFrame(response_['results'])
    df['photos'].fillna('...', inplace=True)
    #df.to_excel('lista.xlsx')
    ##--------------
    ### NOME
    lista_geral = []
    lista_geral.append(df['name'].values)
    lista_nova = lista_geral[0]
    lista_final_nomes = {
        'lista':list(lista_nova)
    }
    ##--------------
    ### location
    lista_primeiraopcao_location = df['geometry'].values
    lista_primeiraopcao_location=json.dumps(list(lista_primeiraopcao_location))
    teste = json.loads(lista_primeiraopcao_location)
    lista_final_primeiraopcao_locaiton = []
    dicio_primeiraopcao_location = []
    for item in teste:
        dicio_primeiraopcao_location.append(item['location'])       
    lista_final_primeiraopcao_locaiton= {
        'lista':list(dicio_primeiraopcao_location)
    }
    #print(session['lista_final_primeiraopcao_locaiton'])
    ##--------------
    ### endereco
    lista_primeiraopcao_endereco = df['vicinity'].values
    dicio_lista_primeiraopcao_endereco = {
        'lista': list(lista_primeiraopcao_endereco)
    }
    #print(session['lista_primeiraopcao_endereco'])
    #print(session['lista_primeiraopcao_fotos'])
    ##--------------
    ### rating
    lista_primeiraopcao_rating = df['rating'].values
    dicio_lista_primeiraopcao_rating = {
        'lista': list(lista_primeiraopcao_rating)
    }    
    #print(session['lista_primeiraopcao_rating'])

    #session['lista_final_nomes'] = lista_final_nomes
    #session['lista_final_primeiraopcao_locaiton'] = lista_final_primeiraopcao_locaiton
    #session['lista_primeiraopcao_endereco'] = dicio_lista_primeiraopcao_endereco
    #session['lista_primeiraopcao_fotos'] = dic_primeiraopcao_fotos
    #session['lista_primeiraopcao_rating'] = dicio_lista_primeiraopcao_rating
    ##--------------
    ### fotos
    try:
        lista_primeiraopcao_fotos = df['photos'].values
        lista_primeiraopcao_fotos_json_dumps=json.dumps(list(lista_primeiraopcao_fotos))
        lista_primeiraopcao_fotos_json_loads = json.loads(lista_primeiraopcao_fotos_json_dumps)
        lista_primeiraopcao_fotos= []
        for item in lista_primeiraopcao_fotos_json_loads:
            lista_primeiraopcao_fotos.append(item)
        dic_primeiraopcao_fotos= {
            'lista':list(lista_primeiraopcao_fotos)
        }
        final_primeiraopcao_fotos_dois = []
        # print(dic_primeiraopcao_fotos['lista'])
        # print('-------')
        for item in dic_primeiraopcao_fotos['lista']:
            if item == '...':
                src = 'https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/restaurant-71.png'
            else:
                src = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference='+item[0]['photo_reference']+'&key='+API_KEY
            final_primeiraopcao_fotos_dois.append(src) 
    except Exception as e:
        final_primeiraopcao_fotos_dois = []
        src = 'https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/restaurant-71.png'
        final_primeiraopcao_fotos_dois.append(src)
    lista_total = {
    'lista_primeiraopcao_nome':lista_final_nomes,
    'lista_final_primeiraopcao_locaiton':lista_final_primeiraopcao_locaiton,
    'lista_primeiraopcao_endereco':dicio_lista_primeiraopcao_endereco,
    'lista_total_primeiraopcao_fotos':final_primeiraopcao_fotos_dois,
    'lista_primeiraopcao_rating':dicio_lista_primeiraopcao_rating

    }
    return lista_total

def quarta_opcao_dados():
    escolha = session['escolha']
    lat = escolha['dado_6_LAT']
    lng = escolha['dado_7_LNG']
    location = (lat, lng)        
    search_string = escolha['dado_4']    
    print("SEARCH STRING>>>_____----, "+search_string)    
    distance = 500 #Aqui tem que dar algum jeito do usuario escolher a distância
    response_ = map_client.places_nearby(
        location=location,
        keyword=search_string,
        name=escolha['dado_4'],
        radius=distance,
    )
    df = pd.DataFrame(response_['results'])
    df['photos'].fillna('...', inplace=True)
    #df.to_excel('lista.xlsx')
    ##--------------
    ### NOME
    lista_geral = []
    lista_geral.append(df['name'].values)
    lista_nova = lista_geral[0]
    lista_final_nomes = {
        'lista':list(lista_nova)
    }
    ##--------------
    ### location
    lista_primeiraopcao_location = df['geometry'].values
    lista_primeiraopcao_location=json.dumps(list(lista_primeiraopcao_location))
    teste = json.loads(lista_primeiraopcao_location)
    lista_final_primeiraopcao_locaiton = []
    dicio_primeiraopcao_location = []
    for item in teste:
        dicio_primeiraopcao_location.append(item['location'])       
    lista_final_primeiraopcao_locaiton= {
        'lista':list(dicio_primeiraopcao_location)
    }
    #print(session['lista_final_primeiraopcao_locaiton'])
    ##--------------
    ### endereco
    lista_primeiraopcao_endereco = df['vicinity'].values
    dicio_lista_primeiraopcao_endereco = {
        'lista': list(lista_primeiraopcao_endereco)
    }
    #print(session['lista_primeiraopcao_endereco'])
    #print(session['lista_primeiraopcao_fotos'])
    ##--------------
    ### rating
    lista_primeiraopcao_rating = df['rating'].values
    dicio_lista_primeiraopcao_rating = {
        'lista': list(lista_primeiraopcao_rating)
    }    
    #print(session['lista_primeiraopcao_rating'])

    #session['lista_final_nomes'] = lista_final_nomes
    #session['lista_final_primeiraopcao_locaiton'] = lista_final_primeiraopcao_locaiton
    #session['lista_primeiraopcao_endereco'] = dicio_lista_primeiraopcao_endereco
    #session['lista_primeiraopcao_fotos'] = dic_primeiraopcao_fotos
    #session['lista_primeiraopcao_rating'] = dicio_lista_primeiraopcao_rating
    ##--------------
    ### fotos
    try:
        lista_primeiraopcao_fotos = df['photos'].values
        lista_primeiraopcao_fotos_json_dumps=json.dumps(list(lista_primeiraopcao_fotos))
        lista_primeiraopcao_fotos_json_loads = json.loads(lista_primeiraopcao_fotos_json_dumps)
        lista_primeiraopcao_fotos= []
        for item in lista_primeiraopcao_fotos_json_loads:
            lista_primeiraopcao_fotos.append(item)
        dic_primeiraopcao_fotos= {
            'lista':list(lista_primeiraopcao_fotos)
        }
        final_primeiraopcao_fotos_dois = []
        # print(dic_primeiraopcao_fotos['lista'])
        # print('-------')
        for item in dic_primeiraopcao_fotos['lista']:
            if item == '...':
                src = 'https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/restaurant-71.png'
            else:
                src = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference='+item[0]['photo_reference']+'&key='+API_KEY
            final_primeiraopcao_fotos_dois.append(src) 
    except Exception as e:
        final_primeiraopcao_fotos_dois = []
        src = 'https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/restaurant-71.png'
        final_primeiraopcao_fotos_dois.append(src)

    lista_total = {
    'lista_primeiraopcao_nome':lista_final_nomes,
    'lista_final_primeiraopcao_locaiton':lista_final_primeiraopcao_locaiton,
    'lista_primeiraopcao_endereco':dicio_lista_primeiraopcao_endereco,
    'lista_total_primeiraopcao_fotos':final_primeiraopcao_fotos_dois,
    'lista_primeiraopcao_rating':dicio_lista_primeiraopcao_rating

    }
    return lista_total

def quinta_opcao_dados():
    escolha = session['escolha']
    lat = escolha['dado_6_LAT']
    lng = escolha['dado_7_LNG']
    location = (lat, lng)        
    search_string = escolha['dado_5']    
    print("SEARCH STRING>>>_____----, "+search_string)    
    distance = 500 #Aqui tem que dar algum jeito do usuario escolher a distância
    response_ = map_client.places_nearby(
        location=location,
        keyword=search_string,
        name=escolha['dado_5'],
        radius=distance,
    )
    df = pd.DataFrame(response_['results'])
    df['photos'].fillna('...', inplace=True)
    #df.to_excel('lista.xlsx')
    ##--------------
    ### NOME
    lista_geral = []
    lista_geral.append(df['name'].values)
    lista_nova = lista_geral[0]
    lista_final_nomes = {
        'lista':list(lista_nova)
    }
    ##--------------
    ### location
    lista_primeiraopcao_location = df['geometry'].values
    lista_primeiraopcao_location=json.dumps(list(lista_primeiraopcao_location))
    teste = json.loads(lista_primeiraopcao_location)
    lista_final_primeiraopcao_locaiton = []
    dicio_primeiraopcao_location = []
    for item in teste:
        dicio_primeiraopcao_location.append(item['location'])       
    lista_final_primeiraopcao_locaiton= {
        'lista':list(dicio_primeiraopcao_location)
    }
    #print(session['lista_final_primeiraopcao_locaiton'])
    ##--------------
    ### endereco
    lista_primeiraopcao_endereco = df['vicinity'].values
    dicio_lista_primeiraopcao_endereco = {
        'lista': list(lista_primeiraopcao_endereco)
    }
    #print(session['lista_primeiraopcao_endereco'])
    ##--------------
    ### fotos
    lista_primeiraopcao_fotos = df['photos'].values
    lista_primeiraopcao_fotos_json_dumps=json.dumps(list(lista_primeiraopcao_fotos))
    lista_primeiraopcao_fotos_json_loads = json.loads(lista_primeiraopcao_fotos_json_dumps)
    lista_primeiraopcao_fotos= []
    for item in lista_primeiraopcao_fotos_json_loads:
        lista_primeiraopcao_fotos.append(item)
    dic_primeiraopcao_fotos= {
        'lista':list(lista_primeiraopcao_fotos)
    }
    #print(session['lista_primeiraopcao_fotos'])
    ##--------------
    ### rating
    lista_primeiraopcao_rating = df['rating'].values
    dicio_lista_primeiraopcao_rating = {
        'lista': list(lista_primeiraopcao_rating)
    }    
    #print(session['lista_primeiraopcao_rating'])

    #session['lista_final_nomes'] = lista_final_nomes
    #session['lista_final_primeiraopcao_locaiton'] = lista_final_primeiraopcao_locaiton
    #session['lista_primeiraopcao_endereco'] = dicio_lista_primeiraopcao_endereco
    #session['lista_primeiraopcao_fotos'] = dic_primeiraopcao_fotos
    #session['lista_primeiraopcao_rating'] = dicio_lista_primeiraopcao_rating
    final_primeiraopcao_fotos_dois = []
    # print(dic_primeiraopcao_fotos['lista'])
    # print('-------')
    for item in dic_primeiraopcao_fotos['lista']:
        if item == '...':
            src = 'https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/restaurant-71.png'
        else:
            src = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference='+item[0]['photo_reference']+'&key='+API_KEY
        final_primeiraopcao_fotos_dois.append(src) 
    lista_total = {
    'lista_primeiraopcao_nome':lista_final_nomes,
    'lista_final_primeiraopcao_locaiton':lista_final_primeiraopcao_locaiton,
    'lista_primeiraopcao_endereco':dicio_lista_primeiraopcao_endereco,
    'lista_total_primeiraopcao_fotos':final_primeiraopcao_fotos_dois,
    'lista_primeiraopcao_rating':dicio_lista_primeiraopcao_rating

    }
    return lista_total





@app.route('/pagina_dados')
def pagina_dados():
    primeira = session['escolha']['dado_um']
    segunda = session['escolha']['dado_2']
    terceira = session['escolha']['dado_3']
    quarta = session['escolha']['dado_4']
    quinta = session['escolha']['dado_5']
    lista_escolhas = []
    lista_escolhas.append(primeira)
    lista_escolhas.append(segunda)
    lista_escolhas.append(terceira)
    lista_escolhas.append(quarta)
    lista_escolhas.append(quinta)
    lista_primeira_opcao = primeira_opcaao_dados()
    time.sleep(0.1)
    lista_segunda_opcao = segunda_opcao_dados()  
    lista_terceira_opcao = terceira_opcao_dados()  
    lista_quarta_opcao = quarta_opcao_dados()  
    time.sleep(0.1)
    lista_quinta_opcao = quinta_opcao_dados()  


     
    return render_template('pagina_dados.html',lista_escolhas=lista_escolhas,lista_primeira_opcao=lista_primeira_opcao,lista_segunda_opcao=lista_segunda_opcao,lista_terceira_opcao=lista_terceira_opcao,lista_quarta_opcao=lista_quarta_opcao,lista_quinta_opcao=lista_quinta_opcao, len=len)

    


if __name__=="__main__":
    app.run(debug=True)