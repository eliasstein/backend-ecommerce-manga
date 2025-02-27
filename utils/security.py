import os
import datetime
import jwt
import pytz
from dotenv import dotenv_values

class Security():
    #Obtenemos la clave de encriptacion
    secret = {
        "access_token":os.getenv("JWT_KEY"),
        "refresh_token":os.getenv("JWT_KEY")+"refresh"
    }
    #Ajustamos la zona horaria a argentina
    tz = pytz.timezone("America/Argentina/Buenos_Aires")

    #Metodo para generar token
    @classmethod
    def generate_token(cls, payload, minutes=.0, days=.0, refresh=False):
        '''
        Metodo que recibe como parametros un diccionario con el contenido del jwt,
        minutos para que expire el token y dias para que expire
        '''
        # payload = {
        #     'iat': datetime.datetime.now(tz=cls.tz),
        #     'exp': datetime.datetime.now(tz=cls.tz) + datetime.timedelta(minutes=10),
        #     'id': authenticated_user["id"],
        #     'username': authenticated_user["username"],
        #     'roles': ['Administrator', 'Editor']
        # }
        payload["iat"]=datetime.datetime.now(tz=cls.tz)
        payload["exp"]=datetime.datetime.now(tz=cls.tz) + datetime.timedelta(minutes=minutes, days=days)

        return jwt.encode(payload, 
                          cls.secret["refresh_token"] if refresh else cls.secret["access_token"], 
                          algorithm="HS256")
        # return jwt.encode(payload, cls.secret, algorithm="HS256")


    @classmethod
    def verify_token(cls, headers, refresh_token=False):
        '''Metodo que verifica si el token es valido recibe el encabezado
        de la peticion'''
        try:
            #Busca el header "authorization" para obtener el bearer token
            if 'authorization' in headers.keys():
                authorization = headers['Authorization']
                encoded_token = authorization.split(" ")[1] #Borra bearer 
                #Comprobamos que el token este correcto
                if ((len(encoded_token) > 0) and (encoded_token.count('.') == 2)):
                    try:
                        #Si esta correcto lo decodificamos y retornamos
                        payload = jwt.decode(encoded_token,
                                             cls.secret["refresh_token"] if refresh_token else cls.secret["access_token"],
                                             algorithms=["HS256"])
                        payload["success"]=True
                        return payload
                    except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
                        #en caso de que este expirado o tenga una firma invalida retornamos un falso
                        return {"success":False, "error":"Token expirado o invalido"}
            return {"success":False,"error":"No se encontro el jwt"}
        except Exception as ex:
            return {"success":False,"error":f"{ex}"}    #Error excepcion no controlada.
