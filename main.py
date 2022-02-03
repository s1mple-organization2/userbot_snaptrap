from pyrogram import Client

app = Client("straptrapone")

"""
Функция ищет из 5 последних диалогов диалог с название заказа 
и отправляет сообщение в чат по чат айди
"""


async def send_msg(order_id, order_message):
    async for dialog in app.iter_dialogs(5):
        if (dialog.chat.title == 'snaptrap.online Order #' + order_id):
            await app.send_message(dialog.chat.id, order_message)


""" 
Получить сообщение от бота
Если сообщение пришло от snaptrap_bot или от бота 
то парсим сообщение и создаём группу
затем вызываем метод send_msg что бы отправить в чат список с заказом 
"""


@app.on_message()
async def hello(client, message):
    global order_id, order_message
    chat_id = message.chat.id
    # id юзербот
    userbot_id = '5031837131'
    if message.chat.username == 'snaptrap_bot' or message.chat.type == 'bot':
        tmp = message.text.split(":")
        if tmp[0] != 'chat':
            order_id = tmp[0]
            user_id = tmp[1]
            manager_id = tmp[2]
            list_product = tmp[3]
            total_price = tmp[4]
            order_message = 'Order #' + order_id + '\n' + list_product + "\nTotal price:" + total_price + '$'
            print('userbot_id: ' + userbot_id)
            print('user_id: ' + str(user_id))
            manager = app.get_users(manager_id)

            try:
                await app.create_group('snaptrap.online Order #' + order_id,
                                       [int(user_id), int(manager_id)])
                await send_msg(order_id, order_message)


            except Exception as err:
                await app.send_message(chat_id,
                                       'I can\'ht create a group with a manager, '
                                       'please allow me to add you to the group in the settings and make an order again. Or write to the manager @' + manager.username)
                await app.send_message('me', err)
        elif tmp[0] == 'chat':
            product_name = tmp[1]
            product_price = tmp[2]
            user_id = tmp[3]
            manager_id = tmp[4]
            message = 'Product: ' + product_name + '\nPrice: ' + '$' + product_price
            try:
                await app.create_group('snaptrap.online Product info' + product_name,
                                       [int(user_id), int(manager_id)])
                # await send_msg(order_id, order_message)

            except Exception as err:
                await app.send_message('me', err)

    elif message.text == 'hello':
        await app.send_message(message.chat.id,
                               'Hello ' + message.chat.username + ', please send "/start" to bot @snaptrap_bot')


app.run()
