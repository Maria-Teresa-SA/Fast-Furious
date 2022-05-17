# importa l'API de Telegram
from telegram.ext import Updater, CommandHandler
import city
import metro
import restaurants

street_graph = city.load_osmnx_graph("barcelona.grf")
metro_graph = metro.get_metro_graph()
graph_city = city.build_city_graph(street_graph, metro_graph)
list_restaurants = restaurants.read()


diccionari_ajuda = {
    "start" : "Inicia la conversa. :)",
    "help" : "Ofereix ajuda sobre les comandes disponibles. :)",
    "author" : "Mostra el nom de les autores del projecte. :)",
    "find" : "Cerca quins restaurants satisfan la cerca i n'escriu una llista numerada (12 elements com a molt). Per exemple: /find pizza. :)",
    "info" : "mostra la informació sobre el restaurant especificat pel seu número (triat de la darrera llista numerada obtinguda amb /find). :)",
    "guide" : "mostra un mapa amb el camí més curt per anar del punt actual on es troba l'usuari al restaurant especificat pel seu número (triat de la darrera llista numerada obtinguda amb /find). :)"
}

# defineix una funció que saluda i que s'executarà quan el bot rebi el missatge /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hola! Benvingut al SúperBot.")
    username = update.effective_chat.username
    fullname =  update.effective_chat.first_name + ' ' + update.effective_chat.last_name


def help(update, context):
    if len(context.args) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text = 
        """Hola, soc l'Emma i soc aquí per ajudar! Aquest bot implementa les següents comandes:
                1. start
                2. find
                3. info
                4. guide
                5. help
                6. author
        Si necessites informació addicional d'alguna d'aquestes comandes pots fer-ho fent help <comand>.
        Molta sort navegant-me.
        """)
    elif context.args[0] in diccionari_ajuda:
        context.bot.send_message(chat_id=update.effective_chat.id, text = diccionari_ajuda[context.args[0]])
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text = "No reconec aquesta comanda.")
    # especificacions de cada comanda

def author(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hola! Aquest bot l'han creat les millors programadores del món (pista: Sílvia Fàbregas i Laura Solà)")


def find(update, context):
    requirements = ''
    for entry in context.args: 
        requirements += str(entry) + " "
    possibilities = restaurants.find(requirements, list_restaurants)
    context.user_data['found'] = possibilities
   
    num_outputs  = min(len(possibilities), 12)
    _text = ''
    for i in range(num_outputs):
        _text += str(i + 1) + " - " + possibilities[i].name + '\n'
    context.bot.send_message(chat_id=update.effective_chat.id, text= _text)


# altres errors a considerar: primer argument d'entrada no és un enter
def info(update, context):
    if 'found' in context.user_data:
        # context.bot.send_message(chat_id=update_effective_chat.id, text="haha")
        possibilities = context.user_data['found']
        entrada = int(context.args[0])
        if entrada <= len(possibilities):
            restaurant = possibilities[entrada - 1]
            _text = '' 
            for el in [restaurant.name, restaurant.category, restaurant.address.district, restaurant.address.neighbourhood, restaurant.address.address_name, restaurant.position]:
                _text += str(el) + '\n'
            context.bot.send_message(chat_id=update.effective_chat.id, text= _text)

        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text= 'prova amb un número dins el rang de possibilitats.')
    else:
        # print(e)
        context.bot.send_message(chat_id=update.effective_chat.id, text = 'ups. Prova a fer find primer.')


def where(update, context):
    lat, lon = update.message.location.latitude, update.message.location.longitude

# recordar checkejar que l'entrada és un enter
def guide(update, context):
    if 'found' in contex.user_data:
        possibilities = context.user_data['found']
        entrada = int(context.args[0])
        if entrada <= len(possibilities):
            filename = "hola_et_guio.png"
            coordinate_restaurant = possibilities.position
            current_location = 
            # falta afegir les coordenades del retaurant, agafar les coordenades de la persona amb qui ens comuniquem, fer les funcions plot(city i path) i show a city.py
            path = city.find_path(street_graph, city_graph, coordinate_restaurant, current_location)
            city.plot_path(g, path, filename)
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(filename, "rb"))

        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text='prova amb un número dins el rang de possibilitats.')

    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='ups. Prova a fer find primer.')

# declara una constant amb el access token que llegeix de token.txt
TOKEN = open('token.txt').read().strip()

# crea objectes per treballar amb Telegram
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# indica que quan el bot rebi la comanda /start s'executi la funció start
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CommandHandler('find', find))
dispatcher.add_handler(CommandHandler('info', info))
dispatcher.add_handler(CommandHandler('guide', guide))
dispatcher.add_handler(CommandHandler('author', author))
dispatcher.add_handler(MessageHandler(Filters.location, where))


# engega el bot
updater.start_polling()
updater.idle()