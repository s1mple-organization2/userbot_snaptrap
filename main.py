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
        order_id = tmp[0]
        user_id = tmp[1]
        manager_id = tmp[2]
        list_product = tmp[3]
        total_price = tmp[4]
        order_message = 'Order #' + order_id + '\n' + list_product + "\nTotal price:" + total_price + '$'
        print('userbot_id: ' + userbot_id)
        print('user_id: ' + str(user_id))

        await app.create_group('snaptrap.online Order #' + order_id, [userbot_id, user_id, 5031837131])
        await send_msg(order_id, order_message)


app.run()
