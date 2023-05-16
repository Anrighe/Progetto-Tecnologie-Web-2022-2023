from django.core.exceptions import ValidationError

def valida_non_negativi(valore):
    if valore <= 0:
        raise ValidationError('Il valore non può essere negativo')
    
def valida_iban(val):
    if len(val) != 34:
        raise ValidationError("L'IBAN inseriro non contiene 34 caratteri")
    
def valida_carta_credito(val):
    if len(val) >= 10 or len(val) <= 19:
        for element in val:
            if not element.isdigit():
                raise ValidationError("Il codice carta non contiene solamente numeri")
    else:
        raise ValidationError("Codice carta inserito non valido")
    
def valida_cvv(val):
    if len(val) == 3:
        for element in val:
            if not element.isdigit():
                raise ValidationError("Il cvv non contiene 3 numeri")
    else:
        raise ValidationError("Il cvv non contiene 3 caratteri")