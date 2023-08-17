from django.core.exceptions import ValidationError

def valida_non_negativi(valore):
    '''Controlla che il valore sia maggiore di 0, e se non lo è solleva un ValidationError'''
    if valore <= 0:
        raise ValidationError('Il valore non può essere negativo')
    
def valida_iban(val):
    '''Controlla che l'IBAN inserito sia lungo 34 caratteri, e se non lo è solleva un ValidationError'''
    if len(val) != 34:
        raise ValidationError("L'IBAN inseriro non contiene 34 caratteri")
    
def valida_carta_credito(val):
    '''
    Controlla che il codice carta inserito sia lungo tra 10 e 19 caratteri, e che contenga solamente numeri. 
    Nel caso in cui non lo sia solleva un ValidationError
    '''
    if len(val) >= 10 and len(val) <= 19:
        if not val.isdigit():
            raise ValidationError("Il codice carta non contiene solamente numeri")
    else:
        raise ValidationError("Codice carta inserito non valido")
    
def valida_cvv(val):
    '''
    Controlla che il cvv inserito sia lungo 3 caratteri, e che contenga solamente numeri.
    Nel caso in cui non lo sia solleva un ValidationError
    '''
    if len(val) == 3:
        for element in val:
            if not element.isdigit():
                raise ValidationError("Il cvv non contiene 3 numeri")
    else:
        raise ValidationError("Il cvv non contiene 3 caratteri")