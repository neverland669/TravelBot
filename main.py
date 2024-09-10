import telebot
from telebot import types
import urllib.parse
import requests

import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

YANDEX_MAPS_API_KEY = '6618c8f7-1e96-4990-935b-ea913a9f81f8'
BOT_TOKEN = '7459376341:AAECUgnT7q-OdoJJKRTDEWTut1x5Y5Qcu0I'

bot = telebot.TeleBot(BOT_TOKEN)

def create_city_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=1)
    btnMSK = types.KeyboardButton('Москва')
    btnSPB = types.KeyboardButton('Санкт-Петербург')
    btnNSK = types.KeyboardButton('Новосибирск')
    btnSVO = types.KeyboardButton('Свое место')
    btnBLIZ = types.KeyboardButton('Ближайшие места')
    markup.add(btnMSK, btnSPB, btnNSK, btnSVO, btnBLIZ)
    return markup

def create_type_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=1)
    btnArch = types.KeyboardButton('Архитектура')
    btnMus = types.KeyboardButton('Музеи и Искусство')
    btnAnim = types.KeyboardButton('Животные и Природа')
    btnBACK = types.KeyboardButton('Назад')
    markup.add(btnArch, btnMus, btnAnim, btnBACK)
    return markup

def handle_location(message) -> None:
    user_location = message.location
    latitude = user_location.latitude
    longitude = user_location.longitude

    # Запрос к Google Places API
    url = f'https://search-maps.yandex.ru/v1/?apikey={YANDEX_MAPS_API_KEY}&text=достопримечательности&lang=ru_RU&ll={longitude},{latitude}&spn=0.1,0.1&type=biz'
    response = requests.get(url)
    data = response.json()

    if 'features' in data:
        attractions = data['features']
        if attractions:
            message_t = "Ближайшие достопримечательности:\n"
            for attraction in attractions[:5]:  # Ограничимся первыми 5 достопримечательностями
                name = attraction['properties']['name']
                address = attraction['properties'].get('description', 'Адрес не указан')
                message_t += f"- {name} ({address})\n"
        else:
            message_t = "К сожалению, рядом с вами не найдено достопримечательностей."
    else:
        message_t = "Произошла ошибка при поиске достопримечательностей."
        logger.error(f"Yandex Maps API error: {data.get('message', 'Unknown error')}")

    bot.send_message(message.chat.id, message_t)
    message.text = 'Список городов'
    on_click(message)


@bot.message_handler(commands=['start', 'main', 'hello'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Список городов')
    markup.add(btn1)
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! Это самый обычный ботик, который расскажет и проведет вас по самым лучшим местам разных городов России😉')
    startfile = open('./Start.jpg', 'rb')
    bot.send_photo(message.chat.id, startfile, 'Про какой город вы бы хотели узнать?', reply_markup=markup)
    bot.register_next_step_handler(message, on_click)

def on_click(message):
    if message.text == 'Список городов':
        bot.send_message(message.chat.id, 'В нашем боте доступны такие города как: Москва, Санкт-Петербург и Новосибирск, а так же поиск своего места. Что вы выберете?', reply_markup=create_city_keyboard())
        bot.register_next_step_handler(message, citychoose)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, нажмите на кнопку "Список городов".')
        bot.register_next_step_handler(message, on_click)

def citychoose(message):
    if message.text == 'Москва':
        MSKfile = open('./start_photo.jpg', 'rb')
        bot.send_photo(message.chat.id, MSKfile)
        bot.send_message(message.chat.id, 'Какой тип достопримечательностей вас интересует?', reply_markup=create_type_keyboard())
        bot.register_next_step_handler(message, MSK)
    elif message.text == 'Санкт-Петербург':
        MSKfile = open('./spb.jpg', 'rb')
        bot.send_photo(message.chat.id, MSKfile)
        bot.send_message(message.chat.id, 'В стадии разработки')
        message.text = 'Список городов'
        on_click(message)
    elif message.text == 'Новосибирск':
        MSKfile = open('./nsk.jpeg', 'rb')
        bot.send_photo(message.chat.id, MSKfile)
        bot.send_message(message.chat.id, 'В стадии разработки')
        message.text = 'Список городов'
        on_click(message)
    elif message.text == 'Свое место':
        bot.send_message(message.chat.id, 'Введите место, которое вас интересует')
        bot.register_next_step_handler(message, get_custom_place)
    elif message.text == 'Ближайшие места':
        bot.send_message(message.chat.id, 'Пришли мне геопозицию', reply_markup=create_city_keyboard())
        bot.register_next_step_handler(message, handle_location_message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки")
        message.text = 'Список городов'
        on_click(message)

def handle_location_message(message):
    if message.location:
        handle_location(message)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, отправьте свою геопозицию.')
        message.text = 'Ближайшие места'
        citychoose(message)

def get_custom_place(message):
    place_name = message.text
    encoded_place_name = urllib.parse.quote(place_name)  # Кодируем строку для URL
    location_url = f'https://yandex.ru/maps/?text={encoded_place_name}'
    bot.send_message(message.chat.id, f'Вот ссылка на место: {location_url}')
    message.text = 'Список городов'
    on_click(message)

def MSK(message):
    markuptypeMSK = types.ReplyKeyboardMarkup(row_width=1)

    btnKras = types.KeyboardButton('Красная площадь и Мавзолей')
    btnKreml = types.KeyboardButton('Московский Кремль')
    btnVasil = types.KeyboardButton('Храм Василия Блаженного')
    btnSpasit = types.KeyboardButton('Храм Христа Спасителя')
    btnOst = types.KeyboardButton('Останкинская телебашня')
    btnVDNH = types.KeyboardButton('ВДНХ')
    btnArbat = types.KeyboardButton('Старый Арбат')

    btnBACK = types.KeyboardButton('Назад')

    btnIstor = types.KeyboardButton('Государственный исторический музей')
    btnAlmaz = types.KeyboardButton('Алмазный фонд и Оружейная палата')
    btnTretyak = types.KeyboardButton('Третьяковская галерея')
    btnPushk = types.KeyboardButton('Пушкинский музей')
    btnMuzeon = types.KeyboardButton('Парк искусств «Музеон»')
    btnBolshoy = types.KeyboardButton('Большой театр')

    btnVorob = types.KeyboardButton('Воробьёвы горы')
    btnMoskvarium = types.KeyboardButton('«Москвариум»')
    btnBotan = types.KeyboardButton('Ботанический сад МГУ им. М. В. Ломоносова «Аптекарский огород»')
    btnPobeda = types.KeyboardButton('Парк Победы на Поклонной горе')
    btnZoo = types.KeyboardButton('Московский зоопарк')

    if message.text == 'Архитектура':
        markuptypeMSK.add(btnKras, btnKreml, btnVasil, btnSpasit, btnOst, btnVDNH, btnArbat, btnBACK)
        bot.send_message(message.chat.id, 'Какая достопримечательность вас интересует?', reply_markup=markuptypeMSK)
        bot.register_next_step_handler(message, MSK_ARCH)
    elif message.text == 'Музеи и Искусство':
        markuptypeMSK.add(btnIstor, btnAlmaz, btnTretyak, btnPushk, btnMuzeon, btnBolshoy, btnBACK)
        bot.send_message(message.chat.id, 'Какая достопримечательность вас интересует?', reply_markup=markuptypeMSK)
        bot.register_next_step_handler(message, MSK_MUS)
    elif message.text == 'Животные и Природа':
        markuptypeMSK.add(btnVorob, btnMoskvarium, btnBotan, btnPobeda, btnZoo, btnBACK)
        bot.send_message(message.chat.id, 'Какая достопримечательность вас интересует?', reply_markup=markuptypeMSK)
        bot.register_next_step_handler(message, MSK_NAT)
    elif message.text == 'Назад':
        message.text = 'Список городов'
        on_click(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки")
        message.text = 'Москва'
        citychoose(message)

def MSK_ARCH(message):
    markuptypeMSK = types.ReplyKeyboardMarkup(row_width=1)
    btnRoute = types.KeyboardButton('Построить маршрут')
    btnBACK = types.KeyboardButton('Назад')

    if message.text == 'Красная площадь и Мавзолей':
        markuptypeMSK.add(btnRoute, btnBACK)
        MSKfile = open('./krasn.jpg', 'rb')
        bot.send_photo(message.chat.id, MSKfile, '*Красная площадь и Мавзолей* \n Главные достопримечательности Москвы '
                                                 'и must-see для каждого путешественника, оказавшегося в столице. Это — главная московская площадь, '
                                                 'где находится Лобное место, Исторический музей и храм Василия Блаженного. Рядом с ними, у Кремлёвской стены, есть некрополь, '
                                                 'где похоронены государственные деятели и известные политики. Например, И. В. Сталин, Ф. Э. Дзержинский и Л. И. Брежнев. Одна '
                                                 'из наиболее посещаемых достопримечательностей Красной площади — Мавзолей В. И. Ленина. Первоначально он был деревянный. '
                                                 'В 1930 году было построено каменное здание, которое сохранилось до сегодняшнего дня. Напротив него располагается '
                                                 'Главный универсальный магазин. Прогулка по модным бутикам — также обязательная часть программы. \n \n \n Построить маршрут?', reply_markup=markuptypeMSK)
        bot.register_next_step_handler(message, descrKrasn)

    elif message.text == 'Московский Кремль':
        markuptypeMSK.add(btnRoute, btnBACK)
        MSKfile = open('./kreml.jpg', 'rb')
        bot.send_photo(message.chat.id, MSKfile, '*Московский Кремль* \n В Кремле работает семь музеев, старейший из которых — '
                                                 'Оружейная палата — был основан в 1806 году по указу Александра I. Часть выставок размещается в '
                                                 'Благовещенском, Архангельском и Успенском соборах. Ряд экспозиций также находится в Патриарших '
                                                 'палатах, церкви Ризоположения и внутри колокольни Ивана Великого. В коллекции музеев Московского '
                                                 'Кремля — предметы быта, оружие, украшения и одежда. В некоторых залах проводятся временные выставки '
                                                 'изобразительного и декоративно-прикладного искусства.\n \n \n Построить маршрут?', reply_markup=markuptypeMSK)
        bot.register_next_step_handler(message, descrKreml)


    elif message.text == 'Храм Василия Блаженного':
        markuptypeMSK.add(btnRoute, btnBACK)
        MSKfile = open('./vasil.jpg', 'rb')
        bot.send_photo(message.chat.id, MSKfile, '*Храм Василия Блаженного* \n Один самых важных памятников русской архитектуры XVI века, '
                                                 'возведённый по указу Ивана Грозного в честь покорения Казанского царства. По легенде, после завершения '
                                                 'строительства зодчие были ослеплены, чтобы они никогда не смогли построить другой храм такой же красоты.'
                                                 ' Не все знают, но здание собора на самом деле объединяет 11 церквей (пределов), каждая из которых обладает '
                                                 'уникальным внутренним убранством и иконостасом. С 1923 года службы здесь прекратились, а само здание '
                                                 'музеефицировали. Благодаря этому внутри главных достопримечательностей Москвы сохранились исторические '
                                                 'интерьеры, коллекция памятников древнерусской иконописи, настенные росписи и фрески XVI века.\n \n \n Построить маршрут?', reply_markup=markuptypeMSK)
        bot.register_next_step_handler(message, descrVasil)

    elif message.text == 'Храм Христа Спасителя':
        markuptypeMSK.add(btnRoute, btnBACK)
        MSKfile = open('./xram-xrista-spasitelya.jpg', 'rb')
        bot.send_photo(message.chat.id, MSKfile, '*Храм Христа Спасителя*\n Первый собор на набережной Москвы-реки, недалеко от Кремля освятили в 1883 году. '
                                                 'Здание построили по проекту К. А. Тона — архитектора, ставшего родоначальником русско-византийского стиля в '
                                                 'России. В 1931 году храм Христа Спасителя взорвали: советское правительство планировало построить на его месте '
                                                 'гигантский Дворец Советов. Из-за начала Великой Отечественной от проекта отказались, а на месте строительного '
                                                 'котлована открыли бассейн «Москва». В конце 1990-х историческую достопримечательность решили восстановить на '
                                                 'том же месте. Это не точная копия разрушенного здания, но в общих чертах оно повторяет формы своего предшественника.\n \n \n Построить маршрут?', reply_markup=markuptypeMSK)
        bot.register_next_step_handler(message, descrSpas)

    elif message.text == 'Останкинская телебашня':
        markuptypeMSK.add(btnRoute, btnBACK)
        MSKfile = open('./ostankinskaya-telebasnya.jpg', 'rb')
        bot.send_photo(message.chat.id, MSKfile, '*Останкинская телебашня* \n Москва знаменита не только древними постройками, но и современными достопримечательностями. Останкинская телебашня — такая же визитная карточка города, как и Кремль. Это одно из самых высоких сооружений в мире, высота которого достигает 540 метров. Она возводилась по спецпроекту на уникальном фундаменте, способном выдержать землетрясение в 8 баллов по шкале Рихтера. Сегодня телебашня продолжает выполнять свою основную функцию. А ещё здесь находится вращающийся ресторан и три смотровые площадки на высоте 337 метров, на полу одной из которых установлены стеклянные вставки.  Актуальную информацию о возможности визита можно найти на сайте https://www.tvtower.ru/\n \n \n Построить маршрут?', reply_markup=markuptypeMSK)
        bot.register_next_step_handler(message, descrOstan)

    elif message.text == 'ВДНХ':
        markuptypeMSK.add(btnRoute, btnBACK)
        MSKfile = open('./vdnh.jpg', 'rb')
        bot.send_photo(message.chat.id, MSKfile, '*ВДНХ* \n Огромный выставочный комплекс площадью более 350 гектаров, где можно увидеть архитектурные памятники времён СССР. Среди них скульптурная композиция «Рабочий и колхозница», оригинальные фонтаны «Дружба народов» и «Каменный цветок», павильоны «Земледелие» с Центром славянской письменности, «Космос» с макетом ракеты и другие. На ВДНХ постоянно работает «Парк ремёсел», проводятся разнообразные культурные мероприятия, а зимой открывается гигантский каток.://www.tvtower.ru/\n \n \n Построить маршрут?', reply_markup=markuptypeMSK)
        bot.register_next_step_handler(message, descrVDNH)

    elif message.text == 'Старый Арбат':
        markuptypeMSK.add(btnRoute, btnBACK)
        MSKfile = open('./staryi-arbat.jpg', 'rb')
        bot.send_photo(message.chat.id, MSKfile, '*Старый Арбат* \n Вся улица – это сплошная историческая достопримечательность в центре Москвы. В XVII веке Арбат был ремесленным центром, в XVIII столетии здесь стали появляться дворянские дома. Сегодня это большое творческое пространство под открытым небом. Во время прогулок получится посетить уютные кафе и рестораны с летними верандами, оценить выступления уличных музыкантов и костюмированных артистов, увидеть стену Виктора Цоя, посетить спектакль в Театре Вахтангова. Среди других интересных мест Арбата можно выделить музеи с необычными экспозициями – например, НЛО или парфюмерии. А ещё именно на этой улице расположена мемориальная квартира А. С. Пушкина – великий русский поэт снимал её в 1830-х и провёл здесь первые месяцы жизни с Натальей Гончаровой после свадьбы.://www.tvtower.ru/\n \n \n Построить маршрут?', reply_markup=markuptypeMSK)
        bot.register_next_step_handler(message, descrArbat)

    elif message.text == 'Назад':
        message.text = 'Москва'
        citychoose(message)

    else:
        message.text = 'Архитектура'
        MSK(message)

def MSK_MUS(message):
    markuptypeMSK = types.ReplyKeyboardMarkup(row_width=1)
    btnRoute = types.KeyboardButton('Построить маршрут')
    btnBACK = types.KeyboardButton('Назад')

    if message.text == 'Государственный исторический музей':
        markuptypeMSK.row(btnRoute, btnBACK)
        MSKfile = open('./istor.jpg', 'rb')
        bot.send_photo(message.chat.id, MSKfile, '*Государственный исторический музей* \n Построен в Москве в 1875-1883 годах по приказу Александра II, лично заложившего первый камень при начале работ. Сегодня в музее 39 залов, а его фонды насчитывают свыше 5 миллионов экспонатов. Каждая экспозиция посвящена определённому историческому периоду. Например, в зале «Неолит» демонстрируются копии наскальных рисунков с берегов Ангары и Онеги, а в «Древнерусском городе» представлены копии фресок церкви Спаса на Нередице, построенной в 1199 году. Почти все помещения здания проектировались под определённые экспозиции, что позволило музейщикам гармонично воссоздать атмосферу каждого исторического периода.://www.tvtower.ru/\n \n \n Построить маршрут?', reply_markup=markuptypeMSK)
        bot.register_next_step_handler(message, descrIstor)

    elif message.text == 'Алмазный фонд и Оружейная палата':
        markuptypeMSK.add(btnRoute, btnBACK)
        MSKfile = open('./almaz.jpg', 'rb')
        bot.send_photo(message.chat.id, MSKfile, '*Алмазный фонд и Оружейная палата* \n Музей Москвы, который нередко называют сокровищницей России. Здесь хранится скипетр Екатерины II с бриллиантом «Орлов» весом более 150 карат, большая императорская корона и собрание царских драгоценностей. Отдельная экспозиция посвящена самоцветам необычной формы. Алмазный фонд расположен в здании Оружейной палаты, где выставлены древние государственные регалии, парадная одежда русских императоров (в их числе — легендарная шапка Мономаха), двойной трон, созданный специально для одновременной коронации братьев Ивана Алексеевича и Петра Алексеевича (будущего Петра I), и другие интересные экспонаты.://www.tvtower.ru/\n \n \n Построить маршрут?', reply_markup=markuptypeMSK)
        bot.register_next_step_handler(message, descrAlmaz)

    elif message.text == 'Третьяковская галерея':
        markuptypeMSK.add(btnRoute, btnBACK)
        MSKfile = open('./tretyakovskaya-galereya.jpg', 'rb')
        bot.send_photo(message.chat.id, MSKfile, '*Третьяковская галерея* \n Один из крупнейших художественных музеев мира, коллекция которого насчитывает свыше 180 тысяч предметов: от византийских икон до произведений советских художников. Именно здесь находятся хорошо знакомые всем «Богатыри» Васнецова, медвежата с картины Шишкина «Утро в сосновом лесу» и другие шедевры русской живописи. Сегодня Третьяковская галерея — это яркая достопримечательность и музейный комплекс по всему центру Москвы: основное расположено в Лаврушинском переулке, на Крымском валу находится Новая Третьяковка с огромной экспозицией искусства XX века, а также ещё несколько небольших тематических музеев. Понадобится дня 3, если не больше, чтобы побывать в каждом из них.://www.tvtower.ru/\n \n \n Построить маршрут?', reply_markup=markuptypeMSK)
        bot.register_next_step_handler(message, descrTretyak)

    elif message.text == 'Пушкинский музей':
        markuptypeMSK.add(btnRoute, btnBACK)
        MSKfile = open('./puskinskii-muzei.jpg', 'rb')
        bot.send_photo(message.chat.id, MSKfile, '*Пушкинский музей* \n Основан в 1912 году профессором И. В. Цветаевым при финансовой поддержке Николая II, выделившего крупную сумму на строительство. Сегодня коллекции музея насчитывают более 670 тысяч предметов: от копий античных статуй и древнегреческих амфор до полотен Ван Гога и Пикассо. Оформление некоторых залов стилизовано под определённые исторические периоды, которым посвящены экспозиции. Например, «Итальянский дворик» оформлен в традициях флорентийского палаццо Барджелло. В Пушкинском музее постоянно проходят выставки крупнейших европейских художников прошлого и современных авторов. В 1970-е здесь, например, в течение двух месяцев выставлялась знаменитая «Джоконда».://www.tvtower.ru/\n \n \n Построить маршрут?', reply_markup=markuptypeMSK)
        bot.register_next_step_handler(message, descrPushk)

    elif message.text == 'Парк искусств «Музеон»':
        markuptypeMSK.add(btnRoute, btnBACK)
        MSKfile = open('./park-iskusstv-muzeon.jpg', 'rb')
        bot.send_photo(message.chat.id, MSKfile, '*Парк искусств «Музеон»* \n Это необычный музей под открытым небом, где собрано свыше тысячи скульптур советской эпохи, а также работ современных художников. Коллекцию здешних достопримечательностей начали собирать в 1992 году. Тогда в парк у Новой Третьяковки свозили, кроме всего прочего, ещё и демонтированные памятники. Экспозиция поделена на несколько тематических зон, есть даже отдельный «детский уголок» с фигурами сказочных героев.://www.tvtower.ru/\n \n \n Построить маршрут?', reply_markup=markuptypeMSK)
        bot.register_next_step_handler(message, descrMuzeon)

    elif message.text == 'Большой театр':
        markuptypeMSK.add(btnRoute, btnBACK)
        MSKfile = open('./bolsoi-teatr.jpg', 'rb')
        bot.send_photo(message.chat.id, MSKfile, '*Большой театр* \n История достопримечательности начинается с 1776 года, когда прокурор П. В. Урусов по указу Екатерины II начал строительство здания на Петровке. Театр несколько раз горел, во времена СССР подвергался значительным перестройкам, а в 2005-2011 годах Историческая сцена была закрыта на реконструкцию, в ходе которой были восстановлены интерьеры XIX века. Сегодня основу репертуара Большого составляют классические произведения оперы и балета XIX-XX веков. Тем, кому не посчастливится попасть на представление, доступна экскурсия по театру. Это в разы дешевле билетов на показы спектаклей.://www.tvtower.ru/\n \n \n Построить маршрут?', reply_markup=markuptypeMSK)
        bot.register_next_step_handler(message, descrBolshoy)

    elif message.text == 'Назад':
        message.text = 'Москва'
        citychoose(message)
    else:
        message.text = 'Музеи и Искусство'
        MSK(message)

def MSK_NAT(message):
    markuptypeMSK = types.ReplyKeyboardMarkup(row_width=1)
    btnRoute = types.KeyboardButton('Построить маршрут')
    btnBACK = types.KeyboardButton('Назад')

    if message.text == 'Воробьёвы горы':
        markuptypeMSK.add(btnRoute, btnBACK)
        MSKfile = open('./vorobyovy-gory.jpg', 'rb')
        bot.send_photo(message.chat.id, MSKfile, '*Воробьёвы горы* \n Холмистый район на высоком берегу Москвы-реки расположен напротив стадиона «Лужники». В этом месте находится одна из топовых смотровых площадок города, Андреевский монастырь, спортивный комплекс с горнолыжными склонами, ботанический сад МГУ и другие достопримечательности Москвы. От «Лужников» до Воробьёвых гор можно добраться по открытой недавно канатной дороге.://www.tvtower.ru/\n \n \n Построить маршрут?', reply_markup=markuptypeMSK)
        bot.register_next_step_handler(message, descrVorob)

    elif message.text == '«Москвариум»':
        markuptypeMSK.add(btnRoute, btnBACK)
        MSKfile = open('./moskvarium.jpg', 'rb')
        bot.send_photo(message.chat.id, MSKfile, '*«Москвариум»* \n Центр океанографии и морской биологии на ВДНХ. В 80 аквариумах «Москвариума» содержится свыше 12 тысяч обитателей морей и рек: косатки, скаты, мечехвосты, веслоносы, арованы и другие удивительные создания. Здесь регулярно проводятся открытые тренировки морских животных, желающие могут поплавать в бассейне с дельфинами, посетить научно-познавательные квесты для детей и взрослых, лекции ведущих специалистов-биологов, дайверов и путешественников.://www.tvtower.ru/\n \n \n Построить маршрут?', reply_markup=markuptypeMSK)
        bot.register_next_step_handler(message, descrMoskvar)

    elif message.text == 'Ботанический сад МГУ им. М. В. Ломоносова «Аптекарский огород»':
        markuptypeMSK.add(btnRoute, btnBACK)
        MSKfile = open('./botaniceskii-sad-mgu-im-m-v-lomonosova-aptekarskii-ogorod.jpg', 'rb')
        bot.send_photo(message.chat.id, MSKfile, '*Ботанический сад МГУ им. М. В. Ломоносова «Аптекарский огород»* \n Был создан в Москве в 1706 году по указу Петра I для обучения студентов-медиков, выращивания и заготовки лекарственных растений. На территории сада сохранилось здание лаборатории 1883 года с воссозданными интерьерами и подлинной меблировкой того периода, а также несколько оранжерей со старинной коллекцией экзотических растений. В зимнее время здесь, кстати, зацветают десятки орхидей.://www.tvtower.ru/\n \n \n Построить маршрут?', reply_markup=markuptypeMSK)
        bot.register_next_step_handler(message, descrBotan)

    elif message.text == 'Парк Победы на Поклонной горе':
        markuptypeMSK.add(btnRoute, btnBACK)
        MSKfile = open('./park-pobedy-na-poklonnoi-gore.jpg', 'rb')
        bot.send_photo(message.chat.id, MSKfile, '*Парк Победы на Поклонной горе* \n Крупный мемориальный комплекс на западе столицы был создан в 1995 году в честь 50-летия Победы в Великой Отечественной войне. В парке расположен центральный музей ВОВ, открыта мемориальная синагога, посвящённая жертвам Холокоста, и храм Георгия Победоносца. Над территорией мемориального комплекса возвышается обелиск — монумент Победы. Также здесь работает партизанский городок под открытым небом, выставлены многочисленные образцы военной техники и находится необычный памятник фронтовой собаке. Для детей есть тематические аттракционы, например «Небесный тихоход» — карусель, на которой можно полетать на моделях знаменитых самолётов-кукурузников.://www.tvtower.ru/\n \n \n Построить маршрут?', reply_markup=markuptypeMSK)
        bot.register_next_step_handler(message, descrPobeda)

    elif message.text == 'Московский зоопарк':
        markuptypeMSK.add(btnRoute, btnBACK)
        MSKfile = open('./moskovskii-zoopark.jpg', 'rb')
        bot.send_photo(message.chat.id, MSKfile, '*Московский зоопарк* \n Огромная территория площадью 21 гектар, на которой обитает более 8000 видов животных со всего мира, в том числе редких. Здесь можно встретить, например, китайских панд, дальневосточных леопардов или африканских зебр. Обитают в зоопарке Москвы также многочисленные насекомые, рыбы, птицы – на прогулку и знакомство со всей фауной стоит выделять целый день. Зоопарк разделён на Старый и Новый. Обе части соединены красивым пешеходным мостом над Большой Грузинской улицей.Помимо вольеров и инсектариев на территории также есть аттракционы, музей, пони-клуб – благодаря этому зоопарк можно назвать одним из лучших мест Москвы для детей.://www.tvtower.ru/\n \n \n Построить маршрут?', reply_markup=markuptypeMSK)
        bot.register_next_step_handler(message, descrZoo)

    elif message.text == 'Назад':
        message.text = 'Москва'
        citychoose(message)
    else:
        message.text = 'Животные и Природа'
        MSK(message)


def descrKrasn(message):
    if message.text == 'Построить маршрут':
        bot.send_message(message.chat.id, 'Вот ссылка по которой вы сможете построить маршрут: \n https://yandex.ru/maps/-/CDBpjEmO')
        message.text = "Архитектура"
        MSK(message)
    elif message.text == 'Назад':
        message.text = "Архитектура"
        MSK(message)
    else:
        message.text = 'Красная площадь и Мавзолей'
        MSK_ARCH(message)
def descrKreml(message):
    if message.text == 'Построить маршрут':
        bot.send_message(message.chat.id, 'Вот ссылка по которой вы сможете построить маршрут:\n https://yandex.ru/maps/-/CDBpjOZV \n\nЭКСКУРСИОННОЕ БЮРО, КАССЫ \n+7 (495) 695-41-46 \n+7 (495) 697-03-49 \n\nСайт: www.kreml.ru')
        message.text = "Архитектура"
        MSK(message)
    elif message.text == 'Назад':
        message.text = "Архитектура"
        MSK(message)
    else:
        message.text = 'Московский Кремль'
        MSK_ARCH(message)

def descrVasil(message):
    if message.text == 'Построить маршрут':
        bot.send_message(message.chat.id, 'Вот ссылка по которой вы сможете построить маршрут:\n'
        'https://yandex.ru/maps/-/CDBpjWY8 \n'
        '\n'
        'Адрес \n'
        'Красная площадь, 7, Москва\n\n'

        'Контакты\n'
        '+7 (495) 698-33-04\n\n'

        'Сайт\n'
        'https://shm.ru/')
        message.text = "Архитектура"
        MSK(message)
    elif message.text == 'Назад':
        message.text = "Архитектура"
        MSK(message)
    else:
        message.text = 'Храм Василия Блаженного'
        MSK_ARCH(message)


def descrSpas(message):
    if message.text == 'Построить маршрут':
        bot.send_message(message.chat.id, 'Вот ссылка по которой вы сможете построить маршрут:\n https://yandex.ru/maps/-/CDBpjW7X \n\nАдрес \nул. Волхонка, 15, Москвa \n\nКонтакты \n+7 (495) 637-12-76 \n\nСайт \nhttp://fxxc.ru/')
        message.text = "Архитектура"
        MSK(message)
    elif message.text == 'Назад':
        message.text = "Архитектура"
        MSK(message)
    else:
        message.text = 'Храм Христа Спасителя'
        MSK_ARCH(message)

def descrOstan(message):
    if message.text == 'Построить маршрут':
        bot.send_message(message.chat.id, 'Вот ссылка по которой вы сможете построить маршрут: \n https://yandex.ru/maps/-/CCUgy2bDlA\n\n Адрес \nул. Академика Королёва, 15, корп. 1, Москва \n\nКонтакты \nИНФОРМИРОВАНИЕ ОБ УСЛУГАХ \n+7 (495) 926-61-11 \n\n Сайт \n tvtower.ru')
        message.text = "Архитектура"
        MSK(message)
    elif message.text == 'Назад':
        message.text = "Архитектура"
        MSK(message)
    else:
        message.text = 'Останкинская телебашня'
        MSK_ARCH(message)

def descrVDNH(message):
    if message.text == 'Построить маршрут':
        bot.send_message(message.chat.id, 'Вот ссылка по которой вы сможете построить маршрут: \n https://yandex.ru/maps/-/CDBpj88Q \n\n Адрес \n просп. Мира, 119В, Москва \n\n Контакты \n СПРАВОЧНАЯ \n +7 (495) 544-34-00 \n\n Сайт \n https://vdnh.ru/')
        message.text = "Архитектура"
        MSK(message)
    elif message.text == 'Назад':
        message.text = "Архитектура"
        MSK(message)
    else:
        message.text = 'ВДНХ'
        MSK_ARCH(message)

def descrArbat(message):
    if message.text == 'Построить маршрут':
        bot.send_message(message.chat.id, 'Вот ссылка по которой вы сможете построить маршрут: \n https://yandex.ru/maps/-/CDBpjDzY')
        message.text = "Архитектура"
        MSK(message)
    elif message.text == 'Назад':
        message.text = "Архитектура"
        MSK(message)
    else:
        message.text = 'Старый Арбат'
        MSK_ARCH(message)

def descrIstor(message):
    if message.text == 'Построить маршрут':
        bot.send_message(message.chat.id, 'Вот ссылка по которой вы сможете построить маршрут: \n https://yandex.ru/maps/-/CDBpnYJb \n\n Адрес \n Красная площадь, 1, Москва \n \n Контакты \n СПРАВОЧНАЯ \n +7 (495) 692-40-19 \n\n Сайт \n https://shm.ru/')
        message.text = "Музеи и Искусство"
        MSK(message)
    elif message.text == 'Назад':
        message.text = "Музеи и Искусство"
        MSK(message)
    else:
        message.text = 'Государственный исторический музей'
        MSK_MUS(message)

def descrAlmaz(message):
    if message.text == 'Построить маршрут':
        bot.send_message(message.chat.id, 'Вот ссылка по которой вы сможете построить маршрут: \n https://yandex.ru/maps/-/CDBpnBz~ \n\n Адрес \n Кремлёвская наб., 1, стр. 3, Москва \n\n Контакты \n АДМИНИСТРАЦИЯ \n +7 (495) 629-20-36 \n\n Сайт \n https://www.gokhran.ru/ \n tickets.gokhran.ru/')
        message.text = "Музеи и Искусство"
        MSK(message)
    elif message.text == 'Назад':
        message.text = "Музеи и Искусство"
        MSK(message)
    else:
        message.text = 'Алмазный фонд и Оружейная палата'
        MSK_MUS(message)


def descrTretyak(message):
    if message.text == 'Построить маршрут':
        bot.send_message(message.chat.id, 'Вот ссылка по которой вы сможете построить маршрут: \n https://yandex.ru/maps/-/CDBpnJYF \n\n Адрес \n  Лаврушинский пер., 10, стр. 4, Москва \n\n Контакты \n +7 (495) 957-07-27  \n\n Сайт \n www.tretyakovgallery.ru')
        message.text = "Музеи и Искусство"
        MSK(message)
    elif message.text == 'Назад':
        message.text = "Музеи и Искусство"
        MSK(message)
    else:
        message.text = 'Третьяковская галерея'
        MSK_MUS(message)


def descrPushk(message):
    if message.text == 'Построить маршрут':
        bot.send_message(message.chat.id, 'Вот ссылка по которой вы сможете построить маршрут: \n https://yandex.ru/maps/-/CDBpnR-q \n\n Адрес \n ул. Волхонка, 12, Москва \n\n  Контакты \n АДМИНИСТРАЦИЯ \n+7 (495) 697-95-78 \n\n Сайт \n pushkinmuseum.art')
        message.text = "Музеи и Искусство"
        MSK(message)
    elif message.text == 'Назад':
        message.text = "Музеи и Искусство"
        MSK(message)
    else:
        message.text = 'Пушкинский музей'
        MSK_MUS(message)

def descrMuzeon(message):
    if message.text == 'Построить маршрут':
        bot.send_message(message.chat.id, 'Вот ссылка по которой вы сможете построить маршрут: \n https://yandex.ru/maps/-/CDBpnV~A \n\n Адрес \n Москва, парк искусств Музеон \n\n Контакты \n +7 (495) 995-00-20 \n\n Время работы \n Круглосуточно')
        message.text = "Музеи и Искусство"
        MSK(message)
    elif message.text == 'Назад':
        message.text = "Музеи и Искусство"
        MSK(message)
    else:
        message.text = 'Парк искусств «Музеон»'
        MSK_MUS(message)

def descrBolshoy(message):
    if message.text == 'Построить маршрут':
        bot.send_message(message.chat.id, 'Вот ссылка по которой вы сможете построить маршрут: \n https://yandex.ru/maps/-/CDw3uDpn \n\n Адрес \nТеатральная площадь, 1, Москва\n\n Контакты \n +7 (495) 455-55-55 \n \n Сайт \n www.bolshoi.ru')
        message.text = "Музеи и Искусство"
        MSK(message)
    elif message.text == 'Назад':
        message.text = "Музеи и Искусство"
        MSK(message)
    else:
        message.text = 'Большой театр'
        MSK_MUS(message)

def descrVorob(message):
    if message.text == 'Построить маршрут':
        bot.send_message(message.chat.id, 'Вот ссылка по которой вы сможете построить маршрут: \n https://yandex.ru/maps/-/CDBpnCZV \n\n Адрес \n Москва, улица Косыгина \n\n Сайт \n vorobgori.mytown.site')
        message.text = "Животные и Природа"
        MSK(message)
    elif message.text == 'Назад':
        message.text = "Животные и Природа"
        MSK(message)
    else:
        message.text = 'Воробьёвы горы'
        MSK_NAT(message)

def descrMoskvar(message):
    if message.text == 'Построить маршрут':
        bot.send_message(message.chat.id, 'Вот ссылка по которой вы сможете построить маршрут: \n https://yandex.ru/maps/-/CDBpnKYP \n\n Адрес \n просп. Мира, 119, стр. 23, Москва \n\n Контакты \n МНОГОКАНАЛЬНЫЙ \n +7 (499) 677-77-77 \n ЗАКАЗ VIP-ЛОЖ \n +7 (499) 677-99-99 \n\n Сайт n www.moskvarium.ru \n tickets.moskvarium.ru/')
        message.text = "Животные и Природа"
        MSK(message)
    elif message.text == 'Назад':
        message.text = "Животные и Природа"
        MSK(message)
    else:
        message.text = '«Москвариум»'
        MSK_NAT(message)

def descrBotan(message):
    if message.text == 'Построить маршрут':
        bot.send_message(message.chat.id, 'Вот ссылка по которой вы сможете построить маршрут: \n https://yandex.ru/maps/-/CDBpnOjd \n\n Адрес \n  просп. Мира, 26, стр. 1, Москва \n\n Контакты \n +7 (495) 680-72-22 \n +7 (495) 680-67-65 \n\n Сайт \n hortus.msu.ru')
        message.text = "Животные и Природа"
        MSK(message)
    elif message.text == 'Назад':
        message.text = "Животные и Природа"
        MSK(message)
    else:
        message.text = 'Ботанический сад МГУ им. М. В. Ломоносова «Аптекарский огород»'
        MSK_NAT(message)

def descrPobeda(message):
    if message.text == 'Построить маршрут':
        bot.send_message(message.chat.id, 'Вот ссылка по которой вы сможете построить маршрут: \n https://yandex.ru/maps/-/CDBpnS9Z \n \n Адрес\n Москва, парк Победы \n\n Контакты \n +7 (499) 148-83-00 \n\n Время работы \n  Круглосуточно')
        message.text = "Животные и Природа"
        MSK(message)
    elif message.text == 'Назад':
        message.text = "Животные и Природа"
        MSK(message)
    else:
        message.text = 'Парк Победы на Поклонной горе'
        MSK_NAT(message)
def descrZoo(message):
    if message.text == 'Построить маршрут':
        bot.send_message(message.chat.id, 'Вот ссылка по которой вы сможете построить маршрут:\n https://yandex.ru/maps/-/CDBpnWK0 \n\n Адрес \n  Большая Грузинская ул., 1, стр. 1, Москва \n\n Контакты \n ТЕЛЕФОН ДЛЯ СПРАВОК \n+7 (499) 252-29-51 \n ЗАКАЗ ЭКСКУРСИЙ \n +7 (499) 255-53-75 \n ПО ВОПРОСАМ ОРГАНИЗАЦИИ МЕРОПРИЯТИЙ \n +7 (499) 255-57-63')
        message.text = "Животные и Природа"
        MSK(message)
    elif message.text == 'Назад':
        message.text = "Животные и Природа"
        MSK(message)
    else:
        message.text = 'Московский зоопарк'
        MSK_NAT(message)




@bot.message_handler(commands=['help'])
def main(message):
    bot.send_message(message.chat.id, 'Бог в помощь :) <3')

@bot.message_handler()
def info(message):
    if message.text.lower()== 'привет':
        bot.send_message(message.chat.id,f'Привет, {message.from_user.first_name}! Это самый обычный ботик, который расскажет и проведет вас по самым лучшим местам разных городов России😉')
    elif message.text.lower()== 'id':
        bot.reply_to(message, f'ID: {message.from_user.id}')

@bot.message_handler(content_types=['photo'])
def get_photo(message):
    bot.reply_to(message, 'Отличное фото!')\



bot.polling(none_stop=True)