#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 1.0.1 on Tue Feb  9 16:37:47 2021
#

import wx
from wxautocompletectrl import AutocompleteTextCtrl
import time
from oggetti import OggettoRicerca
import json
from searcher import Searcher
from preprocesser import Preprocesser
import whoosh.index as index
from whoosh.support.levenshtein import distance as edit_distance
from nltk.corpus import wordnet as wn
from indexer import preprocess_and_index
import pathlib
# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade
    

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = kwds.get("style", 0)
        wx.Frame.__init__(self, *args,size = (1000,440), **kwds)
        
        self.SetTitle("Game Searcher")
        #self.SetIcon(wx.Icon("icon.png"))

        self.panel_1 = wx.Panel(self, wx.ID_ANY)

        sizer_1 = wx.GridBagSizer(2, 0)

        self.titolo = wx.StaticText(self.panel_1, wx.ID_ANY, "Game Searcher")
        self.titolo.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        sizer_1.Add(self.titolo, (0, 0), (1, 8), wx.ALIGN_CENTER | wx.TOP, 10)

        label_inserisci = wx.StaticText(self.panel_1, wx.ID_ANY, "Inserisci la query:")
        sizer_1.Add(label_inserisci, (1, 0), (1, 1), wx.EXPAND | wx.LEFT, 4)

        #self.query = wx.TextCtrl(self.panel_1, wx.ID_ANY, "", style=wx.TE_PROCESS_ENTER)
        self.query = AutocompleteTextCtrl(parent=self.panel_1, completer=self.completer)
        sizer_1.Add(self.query, (2, 0), (1, 6), wx.EXPAND | wx.LEFT | wx.TOP, 2)

        sizer_1.Add(5, 20, (2, 6), (1, 1), wx.ALL | wx.EXPAND, 1)

        self.Cerca = wx.Button(self.panel_1, wx.ID_ANY, "Cerca")
        self.Cerca.Enable(False)
        sizer_1.Add(self.Cerca, (2, 7), (2, 1), wx.EXPAND | wx.RIGHT | wx.TOP, 2)
        
        self.choices = ["pos_scor", "tf_idf", "BM25"]
        self.tipo_ricerca = wx.Choice(self.panel_1, wx.ID_ANY, choices=self.choices)
        self.tipo_ricerca.SetMinSize((200, 30))
        self.tipo_ricerca.SetSelection(0)
        sizer_1.Add(self.tipo_ricerca, (3, 0), (1, 1), wx.EXPAND | wx.TOP, 2)
    

        """Per le 3 checkbox fai scegliere la modalità (and, or, or ponderato (ricorda di mettere le label ti spiegazione))"""
        self.radio_1 = wx.RadioButton(self.panel_1, wx.ID_ANY, "OR", style=wx.RB_GROUP)
        sizer_1.Add(self.radio_1, (3, 1), (1, 1), wx.RIGHT | wx.TOP, 4)

        self.radio_2 = wx.RadioButton(self.panel_1, wx.ID_ANY, "AND")
        sizer_1.Add(self.radio_2, (3, 2), (1, 1), wx.RIGHT | wx.TOP, 4)

        self.radio_3 = wx.RadioButton(self.panel_1, wx.ID_ANY, "OR ponderato")
        sizer_1.Add(self.radio_3, (3, 3), (1, 1), wx.RIGHT | wx.TOP, 4)

        self.button_1 = wx.Button(self.panel_1, wx.ID_ANY, "importa")
        self.button_1.SetMinSize((75, 29))
        sizer_1.Add(self.button_1, (3, 4), (1, 1), wx.LEFT | wx.RIGHT | wx.TOP, 4)

        self.button_2 = wx.Button(self.panel_1, wx.ID_ANY, "esporta")
        self.button_2.SetMinSize((75, 29))
        #self.button_2.Enable(False)
        sizer_1.Add(self.button_2, (3, 5), (1, 1), wx.LEFT | wx.TOP, 4)

        sizer_1.Add(5, 20, (3, 6), (1, 1), wx.ALL | wx.EXPAND, 1)



        # """Prova funzionamento oggetti e vettore di oggetti"""
        # obj1 = OggettoRicerca(1,"primo","descrizione sensata","03-07-1999",5)
        # obj2 = OggettoRicerca(2,"secondo","descrizione sensata 2","03-07-1999",2)
        # obj3 = OggettoRicerca(3,"terzo","descrizione sensata 3","03-07-1999",1)
        # global VettoreRisultati
        # VettoreRisultati = [obj1, obj2, obj3]

        self.list_box_1 = wx.html.SimpleHtmlListBox(self.panel_1, wx.ID_ANY, choices=[]) 
        sizer_1.Add(self.list_box_1, (4, 0), (13, 8), wx.ALL | wx.EXPAND, 2)

        self.label_tempo = wx.StaticText(self.panel_1, wx.ID_ANY, "Ricerca completata in 0.00 ms")
        self.label_tempo.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.label_tempo.Hide()
        sizer_1.Add(self.label_tempo, (17, 0), (1, 8), wx.RESERVE_SPACE_EVEN_IF_HIDDEN | wx.ALIGN_CENTER, 0)

        sizer_1.AddGrowableCol(0)
        self.panel_1.SetSizer(sizer_1)

        self.Layout()
        self.Centre()

        self.Bind(wx.EVT_TEXT, self.abilitaCerca, self.query)
        self.Bind(wx.EVT_TEXT_ENTER, self.cerca, self.query)
        self.Bind(wx.EVT_BUTTON, self.importa, self.button_1)
        self.Bind(wx.EVT_BUTTON, self.esporta, self.button_2)
        self.Bind(wx.EVT_BUTTON, self.cerca, self.Cerca)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.summary, self.list_box_1)
        
        # end wxGlade  



    def abilitaCerca(self, event):
        """abilita il tasto "Cerca" solo quando è presente del testo nel campo query"""
        if self.query.GetLineText(0) == "":
            self.Cerca.Enable(False)
        else:
            self.Cerca.Enable(True)
    
        
    def completer(self, val):
        # da effettuare parsing / stemming o roba sul testo della query, guarda roba di marco
        sugg = list(reader.expand_prefix("keywords", self.query.GetLineText(0)))
        return sugg, sugg
        
        
        

    def summary(self, event):
        """mostra il popup con il summary / descrizione"""
        popup = PopupInfo(self.list_box_1.GetSelection())
        popup.Show()

    def cerca(self, event):  # wxGlade: MyFrame.<event_handler>
        
        # cancella i dati già presenti nella lista
        self.list_box_1.Clear()
        self.list_box_1.SetItems([])
        global VettoreRisultati
        VettoreRisultati = []
        
        start_time = time.time()
        
        # TODO: implementa il controllo dello spelling (forse intendevi...) -> usi un thesaurus (wordnet) -> whoosh
        # TODO: implementa la possibilità di usare le regex
        
        # TODO: gestisci il vettore coi risultati (elimina ad ogni ricerca, popola il vettore ad ogni ricerca ecc..)
        # TODO: chiedi di aggiungere campi all'hit per popolare il vettore ecc.. -> cambia l'export e l'import accordingly
        
        if self.radio_1.GetValue():
            group = "factory_or"
        elif self.radio_2.GetValue():
            group = "and"
        elif self.radio_3.GetValue():
            group = "or"
        
        model = self.choices[self.tipo_ricerca.GetSelection()]
        
        plain = self.query.GetLineText(0)
        terms = plain.split(" ")

        # Find the wildcards to not preprocess them
        wildcards = [terms.pop(terms.index(t)) for t in plain.split(" ") if "*" in t or "?" in t]
        
        query_preprocesser = Preprocesser()
        
        if wildcards == [] and group != "and" and model != "pos_scor":
            #Complete query with the synonyms of each term
            terms = query_preprocesser.stopwords_elim(terms)   
            terms = query_expansion(terms)
            terms = query_preprocesser.lemmatize(terms)
            terms = query_preprocesser.stem(terms)
            terms = list(set(terms))
            print(f"Query expanded: {terms}")
            
        #Re-add the wildcards after preprocess            
        queryterms = query_preprocesser.preprocess(" ".join(terms)) + wildcards
            
        global indexpath
        search = Searcher(indexpath,model)
        
        search.group(group)
        search.parse(" ".join(queryterms))
        res = search.search()
        if res.is_empty() == False:
            i = 0 
            for x in res:
                i +=1
                obj = OggettoRicerca(i,x.fields()['title'],x.fields()['description'],"",x.fields().get("rating", 0))
                VettoreRisultati.append(obj)
                
                print(x)
                print(x.matched_terms())
                
                htmlmatch = x.highlights("content", text=x.fields()["description"])
                if htmlmatch:
                    htmlmatch = " Found match in: <i>..." + x.highlights("content", text=x.fields()["description"]) + "...</i>"

                print("---------")
                
                self.list_box_1.Append(x.fields().get('title') + htmlmatch)
                text_label = f"Ricerca completata in {(time.time() - start_time) * 1000:.2f} ms"
        else:
            
                text_label = "Non ho trovato alcun risultato"
                
                #Query correction, Did you mean?
                corrector = search.searcher.corrector("keywords")
                eds = []
                for term in plain.split(" "):
                    #print(search.searcher.suggest("keywords",terms))
                    sugg = corrector.suggest(term,limit=3)
                    if sugg != []:
                        eds = [(edit_distance(s,term),s,term) for s in sugg]
                        finalsugg = min(eds, key = lambda x: x[0])
                        text_label += f" forse cercavi: ...{finalsugg[1]}?"

                    
        self.label_tempo.Show()
        self.label_tempo.SetLabel(text_label)
        
        
        # abilita o disabilita il bottone "esporta"
        if not self.list_box_1.IsEmpty():
            self.button_2.Enable(True)
        else:
            self.button_2.Enable(False)   
        

    def importa(self, event):  # wxGlade: MyFrame.<event_handler>
        """permette di importare dati da un file in formato JSON"""
        dlg = wx.FileDialog(
            self, message="Scegli un file da importare",
            defaultFile="",
            wildcard= "File JSON (*.json)|*.json",
            style=wx.FD_OPEN | wx.FD_CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
        else:
            dlg.Destroy() 
            return
        dlg.Destroy()      
        
        self.list_box_1.Clear()
        global VettoreRisultati
        VettoreRisultati = []
        
        f = open(path,'r')
        contenuto = f.read()
        lista_contenuto = contenuto.split('\n')[:-1]
        for x in lista_contenuto:
            vals = list(json.loads(x).values())
            idg = vals[0]
            nome = vals[1]
            summary = vals[2]
            data = vals[3]
            rating = vals[4]
            VettoreRisultati.append(OggettoRicerca(idg,nome,summary,data,rating))
            self.list_box_1.Append(VettoreRisultati[-1].nome+"\t\t"+VettoreRisultati[-1].rating*'*')
        f.close()
        
        
        
    def esporta(self, event):
        """permette di salvare su file in formato JSON i risultati della query"""
        dlg = wx.FileDialog(
            self, message="Salva il file",
            defaultFile="risultati.json", style=wx.FD_SAVE
            )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
        else:
            dlg.Destroy()
            return
        dlg.Destroy()
        
        f = open(path,"w")        
        for res in VettoreRisultati:
            f.write(json.dumps(vars(res))+'\n')
        f.close()            

# end of class MyFrame

class PopupInfo(wx.Frame):
    def __init__(self, sel):
        wx.Frame.__init__(self, None, title=VettoreRisultati[sel].nome)
        self.panel = wx.Panel(self)
        sizer = wx.GridBagSizer(0,0)
        txt = wx.StaticText(self.panel, label=VettoreRisultati[sel].summary)
        sizer.Add(txt, (0,0), (1,1), wx.ALIGN_CENTER, 0)
        sizer.AddGrowableCol(0)
        sizer.AddGrowableRow(0)
        self.panel.SetSizer(sizer)
        self.Layout()
        self.Centre()

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

# end of class MyApp
#funzione per query expansion
def query_expansion(terms):
    synonyms = []
    for t_i in terms:    # t_i is target term
        selSense = None
        selScore = 0.0
    for s_ti in wn.synsets(t_i, wn.NOUN):
        score_i = 0.0
        for t_j in terms:    # t_j term in t_i's context window
            if (t_i==t_j):
                continue
            bestScore = 0.0
            for s_tj in wn.synsets(t_j, wn.NOUN):
                tempScore = s_ti.wup_similarity(s_tj)
                if (tempScore>bestScore):
                    bestScore=tempScore
                    score_i = score_i + bestScore
                    if (score_i>selScore):
                        selScore = score_i
                        selSense = s_ti
        
        if selSense is not None:
            synonyms += [l.name() for l in selSense.lemmas() if l.name()!=t_i]
    return terms+synonyms

if __name__ == "__main__":
    VettoreRisultati = []
    
    collectionpath = str(pathlib.Path().parent.absolute()) + "\\collection"
    indexpath = collectionpath + "\\indexdir"
    
    try:
        ix = index.open_dir(indexpath)
    except:
        temp = input("Indice non trovato, vuoi crearlo?y/n")
        if temp == "y":
            preprocess_and_index(collectionpath,indexpath)
    finally:
        reader = ix.reader()
        app = MyApp(0)
        app.MainLoop()
