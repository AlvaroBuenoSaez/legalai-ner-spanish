from re import T
from bs4 import BeautifulSoup
from bs4.element import Tag

class Sentence:
    main_link="https://hj.tribunalconstitucional.es/"
    name=""
    link=""
    sections={
            "header":"",
            "previous":"",
            "precedent":"",
            "fundaments":"",
            "dictamen":"",
            "votos":""
        }
    info={
        "órgano":"",
            "magistrados":"",
            "BOE":"",
            "tipo":"",
            "fecha":""
        }
    extracts=list()
    quotes=list()
    concepts={"law":[],"material":[],"process":[]}

    def __init__(self,content):

        soup = BeautifulSoup(content, 'html.parser')
        self.name = soup.title.text
  
        self.link = self.get_link(soup)
        self.sections=self.get_sections(soup)
        self.info=self.get_info(soup)


    def get_link(self,soup):
        out=""
        results=soup.find("div", {"id": "language_selector-container"})
        link = results.find("a",{"id":"es-language_link"})
        link =link["href"]
        return self.main_link+link.strip("/")

    ''' Detects and splits the diferent sections'''    
    def get_sections(self,soup):

        def get_section_1(section:Tag)->dict:#para fundamentos y antecedentes
            title=section.find("h4",{"class":"section-title"}).text.strip()
            items_raw=section.find_all("div",{"class":"section_item-container"})
            items=[item.find("p").text.split(". \n")[1].strip() for item in items_raw]
            return {"title":title,"items":items}

        def get_section_2(section:Tag)->dict:# para dictamen
            header=section.find("p",{"id":"dictamen-cabecera"}).text.strip()
            text=section.find("p",{"id":"dictamen-texto"}).text.strip()
            footer=section.find("p",{"id":"dictamen-pie"}).text.strip()
            return {"header":header,"text":text,"footer":footer}
                
        def get_section_3(section:Tag)->dict:# para cabecera
            for cabecera_section in section:
                if cabecera_section.find("h4"):
                    cabecera_title=cabecera_section.find("h4").text.strip()
                elif cabecera_section.find("p",{"id":"resolucion-sentencia"}):
                    items_raw=cabecera_section.find_all("p",{"id":"resolucion-sentencia"})
                    cabecera_items=[item.text.strip() for item in items_raw]  
            return {"title":cabecera_title,"items":cabecera_items}  

        out={}

        main=soup.find("div",{"class":"main-section","id":"complete_resolucion"})
           
        cabecera=main.find_all("div",{"id":"","class":"section"})
        antecedentes=soup.find("div",{"class":"section","id":"antecedentes-container"})
        fundamentos=soup.find("div",{"class":"section","id":"fundamentos-container"})
        dictamen=soup.find("div",{"class":"section","id":"dictamen-container"})
        votos=soup.find("div",{"class":"section","id":"votos-container"})
        
        out["cabecera"]=get_section_3(cabecera)
        out["antecedentes"]=get_section_1(antecedentes)
        out["fundamentos"]=get_section_1(fundamentos)
        out["dictamen"]=get_section_2(dictamen)
        out["votos"]={"title":"","items":""}
        
        return out

    ''' Detects the info printed on tables '''
    def get_info(self,soup):
        def get_table(table):
            out={}
            for row in table.find_all("tr"):
                elements=row.find_all("td")
                if len(elements)==2:
                    out[elements[0].text.strip()]=elements[1].text.strip()

            return out

        out={}
        result=soup.find("div", {"id": "ficha-tecnica"})
        tables=result.find_all("table")
        for table in tables:
            out|=get_table(table)
        return out

    def get_concepts(self,soup):
        out={}

        return out

    def get_extracts(self,soup):
        out=[]

        return out

    def get_quotes(self,soup):
        out=[]

        return out

