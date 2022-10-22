from decimal import setcontext
from lib2to3.pgen2.token import TILDE
from re import T
from bs4 import BeautifulSoup
from bs4.element import Tag

class Sentence:
    main_link="https://hj.tribunalconstitucional.es/"
    name=""
    link=""
    sections=dict()
    info=dict()
    extracts=list()
    quotes=list()
    concepts={"law":[],"material":[],"process":[]}

    def __init__(self,pdf,content):

        soup = BeautifulSoup(content, 'html.parser')
        self.pdf = pdf
        self.name = soup.title.text

        try:
            self.link = self.get_link(soup)
            self.sections=self.get_sections(soup)
            self.info=self.get_info(soup)
            self.quotes=self.get_quotes(soup)
            self.concepts=self.get_concepts(soup)
            self.extracts=self.get_extracts(soup)
        except Exception as e:
            print("Error en ",self.pdf)
            raise e



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
            try:
                items=[item.find("p").text.strip() if item.find("p") else item.text.strip() for item in items_raw]
                items=[item.split(". \n")[1].strip() if ". \n" in item else item for item in items]
            except Exception as e:
                print(items_raw)
                raise e
            return {"title":title,"items":items}

        def get_section_2(section:Tag)->dict:# para dictamen
            header=section.find("p",{"id":"dictamen-cabecera"}).text.strip() if section.find("p",{"id":"dictamen-cabecera"}) else ""
            text=section.find("p",{"id":"dictamen-texto"}).text.strip() if section.find("p",{"id":"dictamen-texto"}) else ""
            footer=section.find("p",{"id":"dictamen-pie"}).text.strip() if section.find("p",{"id":"dictamen-pie"}) else ""
            return {"header":header,"text":text,"footer":footer}
                
        def get_section_3(section:Tag)->dict:# para cabecera
            cabecera_title=""
            cabecera_items=[]
            for cabecera_section in section:
                if cabecera_section.find("h4"):
                    cabecera_title=cabecera_section.find("h4").text.strip()
                elif cabecera_section.find("p",{"id":"resolucion-sentencia"}):
                    items_raw=cabecera_section.find_all("p",{"id":"resolucion-sentencia"})
                    cabecera_items=[item.text.strip() for item in items_raw] 
                else:
                    print("Campo en cabecera nuevo.")
            
            return {"title":cabecera_title,"items":cabecera_items}  
        
        def get_section_4(section:Tag)->dict:
            title=""
            items=[]
            header=""
            result=section.find("h4",{"id":"votos-section-title"})
            if result:
                title=result.text.strip() 

            voto_container=section.find("div",{"class":"section_item-container"})
            if  voto_container:
                if voto_container.find("p",{"id":"cabecera-voto"}):
                    header=voto_container.find("p",{"id":"cabecera-voto"}).text.strip()
                if voto_container.find_all("p",{"id":""}):
                    items=[item.text.strip() for item in voto_container.find_all("p",{"id":""})]
            return {"title":title,"items":items,"header":header}

        out={}

        main=soup.find("div",{"class":"main-section","id":"complete_resolucion"})
           
        cabecera=main.find_all("div",{"id":"","class":"section"})
        antecedentes=soup.find("div",{"class":"section","id":"antecedentes-container"})
        fundamentos=soup.find("div",{"class":"section","id":"fundamentos-container"})
        dictamen=soup.find("div",{"class":"section","id":"dictamen-container"})
        votos=soup.find("div",{"class":"section","id":"votos-container"})
   
        out["cabecera"]=get_section_3(cabecera) if cabecera else {"title":"","items":[]}
        out["antecedentes"]=get_section_1(antecedentes) if antecedentes else {"title":"","items":""}
        out["fundamentos"]=get_section_1(fundamentos) if fundamentos else {"title":"","items":""}
        out["dictamen"]=get_section_2(dictamen) if dictamen else {"header":"","text":"","footer":""}
        out["votos"]=get_section_4(votos) if votos else {"title":"","items":"","header":""}
        
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
        types=["constitucionales","procesales"]
        for t in types:
            out[t]=[]
            result_ul=soup.find("ul",{"id":"conceptos-"+t})
            if result_ul:
                result_li=result_ul.find_all("li")
                out[t]=[item.text.strip() for item in result_li if item]

        return out

    def get_extracts(self,soup):
        out=[]
        results=soup.find("div",{"id":"extractos"}).find_all("li")
        if results:
            items=[item.find("p").text.strip() for item in results if item]
        else:
            items=[]
        return items

    def get_quotes(self,soup):
        out=[]
        result=soup.find("ul", {"id": "disposiciones-citadas"})
        if result:
            items=[item.text.strip() for item in result.find_all("li") if item]
        else:
            items=[]
        return items

    def report(self):
        def compress_dict(d:dict,up_name=""):
            out={}
            for k in d.keys():
                new_key= "{}.{}".format(up_name,k) if up_name!="" else k
                if type(d[k])==dict:
                    out|=compress_dict(d[k],new_key)
                else:
                    out[new_key]=d[k]
            return out
        
        data=compress_dict(self.__dict__,"")
        out ={}
        for k in data.keys():
            if not data[k] or len(data)==0 or data=="":
                out[k]=False
            else:
                out[k]=True
        return out
