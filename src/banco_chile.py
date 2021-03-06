import re
import requests
from urllib.parse import urljoin, urlparse, urlunparse, urlencode

from src.exceptions import LoginFailedException


class BancoChile:
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
    RUT_REGEX = r"\d{1,2}[.]?\d{3}[.]?\d{3}-?[\dk]"
    API_BASE_URL = "https://portalpersonas.bancochile.cl/mibancochile/rest/persona/"
    LOGIN_URL = "https://login.bancochile.cl/bancochile-web/persona/login/index.html"
    API_REFERER = "https://portalpersonas.bancochile.cl/mibancochile-web/front/persona/index.html"

    def __init__(self, username, password):
        if not re.match(self.RUT_REGEX, username):
            raise ValueError("Rut Inválido.")
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": self.USER_AGENT,
                "Referer": self.LOGIN_URL,
                "Origin": self._get_origin(self.LOGIN_URL),
            }
        )
        self.logged_in = False

    def login(self):
        response = self.session.get(self.LOGIN_URL)
        response.raise_for_status()
        self._call("perfilamiento/home", enforce_login=False)
        raw_username = self.username.replace(".", "").replace("-", "")
        rut_number = f"{int(raw_username[:-1]):,d}".replace(",", ".")
        formatted_username = f"{rut_number}-{raw_username[-1]}"
        data = {
            "username2": [raw_username, formatted_username],
            "userpassword": self.password,
            "request_id": "",
            "ctx": "persona",
            "username": raw_username,
            "password": f"00000000{self.password}"[-8:],
        }
        response = self.session.post(
            "https://login.bancochile.cl/oam/server/auth_cred_submit", data
        )
        if (
                response.status_code != 200
                or urlunparse(urlparse(response.url)._replace(fragment="")) != self.API_REFERER
        ):
            raise LoginFailedException("Error al hacer Login.")
        self.session.headers["Referer"] = self.API_REFERER
        self.session.headers["Origin"] = self._get_origin(self.API_REFERER)
        self.logged_in = True

    def session_key(self):
        try:
            session_key = self._call('pec/cuentas/sesionKey')
        except Exception:
            raise ValueError("Could not get session key")
        return session_key.content

    def products(self):
        try:
            products = self._call('selectorproductos/selectorProductos/obtenerProductos').json()
        except Exception:
            raise ValueError("No se pudieron obtener productos")
        return products

    def transactions(self):
        products = self.products()
        accounts = [product for product in products["productos"] if product["tipo"] == "cuenta"]

        cartola_request = {
            "cuentasSeleccionadas": [{
                "nombreCliente": products["nombre"],
                "rutCliente": products["rut"],
                "numero": accounts[0]["numero"],
                "mascara": accounts[0]["mascara"],
                "selected": True,
                "codigoProducto": accounts[0]["codigo"],
                "claseCuenta": accounts[0]["claseCuenta"],
                "moneda": accounts[0]["codigoMoneda"]
            }],
            "cabecera": {"paginacionDesde": {}, "statusGenerico": True}}
        try:
            transactions = self._call('movimientos/getcartola', method="post", json=cartola_request).json()
        except Exception:
            raise ValueError("No se pudieron obtener los movimientos")
        return transactions

    def recipients(self, pagina='1', cantidad_items='100', prioriza_favorito='true'):
        try:
            recipients = self._call(
                f"tef-agenda/agenda/search?pagina={pagina}&cantidadItems={cantidad_items}&priorizaFavorito={prioriza_favorito}"
            ).json()
        except Exception:
            raise ValueError("No se pudieron obtener los destinatarios")

        return recipients

    def cards(self):
        try:
            cards = self._call("tarjetas/widget/informacion-tarjetas", "post").json()
        except Exception:
            raise ValueError("Could not get cards")

        return cards

    def profile(self):
        try:
            profile = self._call("perfilamiento").json()
        except Exception:
            raise ValueError("No se pudo obtener datos de usuario")

        return profile

    def userdata(self):
        try:
            profile = self._call("miperfil/datos").json()
        except Exception:
            raise ValueError("No se pudo obtener datos de usuario")

        return profile

    def registered_bills(self):
        try:
            session_key = self.session_key()
            params = urlencode({ 'sesionKey' : session_key })
            bills = self._call("pec/cuentas/inscritas?" + params).json()
        except Exception:
            raise ValueError("No se pudieron obtener cuentas")

        return bills

    def _call(self, url, method="get", enforce_login=True, *args, **kwargs):
        if enforce_login and not self.logged_in:
            raise LoginFailedException("Debe iniciar sesión.")
        response = self.session.request(
            method,
            urljoin(self.API_BASE_URL, url),
            *args,
            **kwargs,
        )
        response.raise_for_status()
        return response

    @staticmethod
    def _get_origin(referer):
        parsed = urlparse(referer)
        return f"{parsed.scheme}://{parsed.netloc}"
