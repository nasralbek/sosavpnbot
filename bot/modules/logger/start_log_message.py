

horizontal_line = "-"*20
def new_line(sizeX,text = '',):
    coef = sizeX - len(text)//2 
    # coef += len(text)%2
    left_leveler = ' '* coef
    right_leveler = ' '* (coef + (1 if len(text)%2==0 else 0))

    line = f'|{left_leveler}{text}{right_leveler}|\n'
    return line

def get_start_log_message(sizeX,sizeY,*args,**kwargs):
    message = '\n'
    horizontal_line = ' '+'- '*(sizeX+1)+"\n"
    message += horizontal_line
    lines_count = len(args) + len(kwargs)
    paddingX = sizeY-lines_count
    
    for _ in range(paddingX):
        message += new_line(sizeX)

    for arg in args:
        message +=new_line(sizeX,str(arg))

    for kwarg in kwargs:
        
        line_text = f"{kwarg}:{kwargs[kwarg]}"
        message+=new_line(sizeX,line_text)

    for _ in range(paddingX):
        message += new_line(sizeX)
    message +=horizontal_line
    return message


if __name__=="__main__":
    print(
        get_start_log_message(20,10,"started",'','','','','','',keyword_arg = "hello", webhook = 'url/webhook')
    )