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


async def get_chat_link(title):
    global link
    async for dialog in app.iter_dialogs(5):
        if (dialog.chat.title == title):
            link = app.export_chat_invite_link(dialog.chat.id)
            await app.send_message(dialog.chat.id, link)


""" 
Получить сообщение от бота
Если сообщение пришло от snaptrap_bot или от бота 
то парсим сообщение и создаём группу
затем вызываем метод send_msg что бы отправить в чат список с заказом 
"""


@app.on_message()
async def hello(client, message):
    global order_id, order_message, title
    text = 'Hello, Welcome to SnapTrap.Online \'Your Plug’s Plug\' \nTo make an account please click the blue link\n👇👇👇👇👇👇👇👇👇👇👇👇👇\n\t\t\t@snaptrap_bot\nThen click the Start button & Registration button to create an account. Please allow 2-3 Hours for Verification.\nIf you have any questions please click\n👉 @barelanded to message us.'

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
                title = 'snaptrap.online Product info ' + product_name + user_id
                await app.create_group(title,
                                       [int(user_id), int(manager_id)])
                await get_chat_link(title)

                # await send_msg(order_id, order_message)
            except Exception as err:
                await app.send_message('me', err)

    elif message.text == 'hello' or message.text == 'Hello':
        await app.send_message(message.chat.id, text)
    elif message.text == 'Hi' or message.text == 'hi':
        await app.send_message(message.chat.id, text)

    elif message.text == 'tg':
        await app.create_group('test_group1', [5031837131])


app.run()
