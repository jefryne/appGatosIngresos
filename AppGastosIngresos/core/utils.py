import secrets
import string


#funcion para generar un ID de usuario aleatorio
def generate_user_id(length=30):
    #caracteres posibles para el Id aleatorio 
    characters = string.ascii_letters + string.digits
    
    #gerear el Id aleatorio de la longitud deseada
    random_id = ''.join(secrets.choice(characters) for _ in range(length))
    
    return random_id






