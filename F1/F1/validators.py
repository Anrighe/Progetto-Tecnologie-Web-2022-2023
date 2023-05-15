from django.core.exceptions import ValidationError

def valida_non_negativi(valore):
    if valore <= 0:
        raise ValidationError('Il valore non può essere negativo')
    
def valida_iban(val):
    if val.length() != 34:
        raise ValidationError("L'IBAN inseriro non contiene 34 caratteri")
    
def valida_carta_credito(val):
    if val.length() < 10 or val.length() > 20:
        raise ValidationError("Codice carta inserito non valido")
    
def valida_cvv(val):
    if val.length() != 3:
        raise ValidationError("Il cvv non contiene 3 caratteri")