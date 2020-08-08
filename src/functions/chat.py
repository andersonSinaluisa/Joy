
# https://chatterbot.readthedocs.io/en/stable/tutorial.html
# install pip chatterbot7


from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.comparisons import JaccardSimilarity, SentimentComparison
from chatterbot.comparisons import LevenshteinDistance
from chatterbot.conversation import Statement

# Descomentar estas lineas sólo la primera vez que se ejecute el algoritmo para instalar los componentes que falten.
# Luego se pueden volver a comentar

# import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')

# Creo una instancia de la clase ChatBot
from textblob import TextBlob, Word

chatbot = ChatBot(
    'JOY',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database='./database.sqlite5',  # fichero de la base de datos (si no existe se creará automáticamente)



    # Un Logic_adapter es una clase que devuelve una respuesta ante una pregunta dada.
    # Se pueden usar tantos logic_adapters como se quiera
    logic_adapters=[
        # 'chatterbot.logic.MathematicalEvaluation', #Este es un logic_adapter que responde preguntas sobre matemáticas en inglés
        # 'chatterbot.logic.TimeLogicAdapter', #Este es un logic_adapter que responde preguntas sobre la hora actual en inglés

        {
            "import_path": "chatterbot.logic.BestMatch",
            "statement_comparison_function": "chatterbot.comparisons.levenshtein_distance",

        },
         {
            'import_path': 'chatterbot.logic.MathematicalEvaluation',
             'threshold': 0.51,
            'default_response': 'Disculpa, no te he entendido bien. ¿Puedes ser más específico?.'
         },
        # {
        #    'import_path': 'chatterbot.logic.SpecificResponseAdapter',
        #    'input_text': 'Eso es todo',
        #    'output_text': 'Perfecto. Hasta la próxima'
        # },
    ],

    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace'
    ],

    # read_only=True,
)

import pyttsx3 as voz
from os import path,stat
import src as _

def hablar(texto):
    lupita = voz.init()
    velocidad = lupita.getProperty('rate')
    lupita.setProperty('rate', velocidad-45)
    lupita.setProperty('voice', 'TTS_MS_ES-MX_SABINA_11.0') # voz con acento mexicano
    lupita.say(texto)
    lupita.runAndWait()

trainer = ChatterBotCorpusTrainer(chatbot)

ruta = path.join(_.DIRNAME, 'files/QA.yml')
rutaf = ruta.replace('\\', '/')

# Train based on the english corpus

trainer.train(rutaf)





# chatbot.train([
#    '¿Cómo estás?',
#    'Bien.',
#    'Me alegro.',
#    'Gracias.',
#    'De nada.',
#    '¿Y tú?'
# ])
import speech_recognition as re
import src.functions.asistente as asis
def saveWord():

    r = re.Recognizer()
    with re.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        asis.sonido()

        comando = r.recognize_google(audio, language='es-EC')

        print("Creo que dijiste: " + comando)


        return comando# lo que se debe hacer con el comando de audio

    except re.UnknownValueError:
        # si no se entendió
        #hablar('no has dicho nada')
        print("No te pude entender")
        saveWord()



    except LookupError as e:
        print('el error es {0}'.format(e))
        #hablar('error temporal')
        saveWord()


from datetime import date
from datetime import datetime
now = datetime.now()
def conversation(var):
    entradaDelUsuario = Statement(var)
    # Elegir la forma de medir la similitud entre dos frases
    levenshtein_distance = LevenshteinDistance()
    # synset_distance = SynsetDistance()
    sentiment_comparison = SentimentComparison()
    # jaccard_similarity = JaccardSimilarity()
   # hablar("el tipo de entrada es {0}".format(type(entradaDelUsuario)))

    disparate = Statement('te equivocaste')  # convertimos una frase en un tipo statement

    if levenshtein_distance.compare(entradaDelUsuario, disparate) > 0.51:
        hablar('¿Qué debería haber dicho?')
        entradaDelUsuarioCorreccion= saveWord()
        trainer.train([entradaDelUsuario,entradaDelUsuarioCorreccion])
        hablar("He aprendiendo que cuando digas {} debo responder {}".format(entradaDelUsuario.text,entradaDelUsuarioCorreccion.text))
    # leemos la entrada del usuario
    elif levenshtein_distance.compare(entradaDelUsuario, Statement('¿que hora es?')) > 0.51:
        hora = str(now.hour)
        minutos = str(now.minute)
        hablar('son las {0} y {1}'.format(hora,minutos))

    elif levenshtein_distance.compare(entradaDelUsuario, Statement('¿cual es la definicion de ?')) > 0.51:
        zen = TextBlob(var)
        palabra = zen.words[-1]

        for i in Word(palabra).definitions:
            tras = TextBlob(i).translate('es')
            hablar(tras)

    elif  levenshtein_distance.compare(entradaDelUsuario, Statement('chao')) > 0.51:
        hablar('hasta luego')

    response = chatbot.generate_response(entradaDelUsuario)




        # print(statement) #statement contiene el mismo valor que entradaDelUsuario
    hablar(response.text)