
topup_text = 'выберите кол-во дней'

def method_selected_text(days,price,method):
    return (f'{days}-{price}-{method}\n')

def days_selected_text(days,price):
    return (f'{days} - {price}\n'
        f'выберите способ оплаты')
