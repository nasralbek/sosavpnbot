topup_text = (f'⚡️ <b>Выберите количество дней</b>'
              )

def method_selected_text(days,price,method):
    return (
            f'⏱️ Количество: <b>{days} дней</b>\n'
            f'💸 Сумма: <b>{price}₽</b>\n'
            f'💳 Метод оплаты: <b>{method}</b>\n\n'
            f'⚡️ <b>Оплатите кнопкой ниже в течение 10 минут</b>' 
            )

def days_selected_text(days,price):
    return (
            f'⏱️ Количество: <b>{days} дней</b>\n'
            f'💸 Сумма: <b>{price}₽</b>\n\n'
            f'<b>⚡️ Выберите способ оплаты</b>'

            )
