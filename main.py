import flet as ft
from flet.core.cupertino_button import CupertinoButton
from alert import AlertManager
from autonoleggio import Autonoleggio
from automobile import Automobile
from flet import Row


FILE_AUTO = "automobili.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DALL'AUTONOLEGGIO DEL LAB03 ---
    autonoleggio = Autonoleggio("Polito Rent", "Alessandro Visconti")
    try:
        autonoleggio.carica_file_automobili(FILE_AUTO) # Carica il file
    except Exception as e:
        alert.show_alert(f"❌ {e}") # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile dell'autonoleggio
    txt_titolo = ft.Text(value=autonoleggio.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {autonoleggio.responsabile}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=autonoleggio.responsabile, label="Responsabile")

    # ListView per mostrare la lista di auto aggiornata
    lista_auto = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere una nuova automobile (marca, modello, anno, contatore posti)
    # TODO



    def minus_click(e):
        if txt_number.value== "0":
            pass
        else:
            txt_number.value = str(int(txt_number.value) - 1)
        page.update()

    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 1)
        page.update()

    # --- FUNZIONI APP ---
    def aggiorna_lista_auto():
        lista_auto.controls.clear()
        for auto in autonoleggio.automobili_ordinate_per_marca():
            stato = "✅" if auto.disponibile else "⛔"
            lista_auto.controls.append(ft.Text(f"{stato} {auto}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        autonoleggio.responsabile = input_responsabile.value
        txt_responsabile.value = f"Responsabile: {autonoleggio.responsabile}"
        page.update()

    # Handlers per la gestione dei bottoni utili all'inserimento di una nuova auto
    # TODO
    txt_marca = ft.TextField(label='inserire la marca')
    txt_modello = ft.TextField(label='inserire la modello')
    txt_auto = ft.TextField(label="inserire l' anno")
    txt_number = ft.TextField(value="0", text_align="right",width=75)
    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)

    # Bottoni per la gestione dell'inserimento di una nuova auto
    # TODO
    icon_più=ft.IconButton(ft.Icons.REMOVE_CIRCLE_OUTLINE_OUTLINED,on_click=minus_click,icon_color="red")
    icon_meno=ft.IconButton(ft.Icons.ADD_PHOTO_ALTERNATE,on_click=plus_click,icon_color="white")
    ANNI=Row([icon_meno,txt_number,icon_più],alignment=ft.MainAxisAlignment.CENTER)


    def aggiungi_auto(e):
        try:
            anno_int = int(txt_auto.value)
            posti_int = int(txt_number.value)
        except ValueError:
            alert.show_alert("❌ ERRORE nell'inserimento dell'anno o dei posti")
        if not txt_marca.value:
                alert.show_alert("❌ Inserisci la marca")
                return
        if not txt_modello.value:
                alert.show_alert("❌ Inserisci il modello")
                return
        try:
                autonoleggio.aggiungi_automobile(txt_marca.value, txt_modello.value, anno_int, posti_int)

                txt_marca.value = ""
                txt_modello.value = ""
                txt_auto.value = ""
                txt_number.value = "0"
                aggiorna_lista_auto()
                page.update()
        except Exception as e:
            alert.show_alert(f"❌ {e}")
            page.update()




    button = CupertinoButton(text='Aggiungi',on_click=aggiungi_auto)
    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        # TODO
        ft.Divider(),
        ft.Text("Aggiungi nuova auto", size=10),
        ft.Row(spacing=10,
               controls=[txt_marca,txt_modello,txt_auto,ANNI],
               alignment=ft.MainAxisAlignment.CENTER),
        button,
        # Sezione 4
        ft.Divider(),
        ft.Text("Automobili", size=20),
        lista_auto,
    )
    aggiorna_lista_auto()

ft.app(target=main)
