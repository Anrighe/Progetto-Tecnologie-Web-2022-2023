from django.contrib import admin
from store.models import TipologiaBiglietto, IstanzaBiglietto, Carrello, Gestore_Circuito, Notifica, Ordine, Utente

admin.site.register(TipologiaBiglietto)
admin.site.register(IstanzaBiglietto)
admin.site.register(Carrello)
admin.site.register(Gestore_Circuito)
admin.site.register(Notifica)
admin.site.register(Ordine)
admin.site.register(Utente)
