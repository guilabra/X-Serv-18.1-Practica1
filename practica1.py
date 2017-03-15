#!/usr/bin/python3

"""
Guillermo Labrador Vazquez
Práctica 1
"""
import urllib.parse
import webapp

class contentApp(webapp.webApp):

    diccionario = {}
    diccionarioInverso = {}

    #Esta funcion hay que llamarla en el process.
    def writeCSV(self, element, url):
        fich = open('lista.csv', 'w')

        for element in self.diccionario:
            fich.write(str(element) + "," + url + '\n')
        fich.close()

    #Esta funcion hay que llamarla antes del parse.
    def readCSV(self):
        import os.path
        if os.path.isfile('lista.csv'):
            fich = open('lista.csv', 'r')
            for lines in fich.readlines():
                urlacortada, url = lines.split(',')
                url = url.replace("\n", "")
                self.diccionario[urlacortada] = url
                self.diccionarioInverso[url] = urlacortada
            fich.close()

    def parse(self, request):

        return (request, request.split(' ', 1)[0], request.split(' ', 2)[1], request.split('=')[-1])
                #Devuelve el metodo       #Devuelve el recurso      #Devuelve el cuerpo

    def process(self, parsedRequest):

        if(len(self.diccionario)== 0):
            self.readCSV()

        requestHttp, method, resourceName, content = parsedRequest

        if method == "GET":
            if resourceName == "/":
                formulario = """<form action="" method="post" >
                    <label for="url">Introduce una url:</label>
                    <input type="text" name="value" />
                    <input type="submit" value="Enviar" />
                    </form></body></html>"""
                for i in self.diccionario:
                    formulario +=  str(i) + " " + self.diccionario[i] + "<br>"

                return ("200 OK", "<html><body>" + formulario + "</body></html")
            else:
                #Redirigir.
                resourceName = int(resourceName.replace("/", ""))
                if resourceName in self.diccionario:
                    return("302 FOUND", "<html><head><meta http-equiv='refresh' content='0; " +
                        "url=" + self.diccionario[resourceName] +"'></head>")
                else:
                    return("404 NOT FOUND", "<html><body>No esta el recurso en el diccionario</body></html>")

        if method == "POST":
            #Diferenciar que haya qs o que no haya.
            if 'value' not in requestHttp:
                return("404 NOT FOUND", "<html><body><h1>No hay body(qs)</h1></body></html>")

            #Para eliminar el 2F, 3F...
            content = urllib.parse.unquote(content)
            #Si no metemos url en el formulario
            if content == "":
                return("404 NOT FOUND", "<html><body>No se ha introducido una url</body></html>")
            #Si metemos url
            else:
                if content.find("http") == -1:
                    content = "http://" + content

                if not content in self.diccionarioInverso:
                    element = len(self.diccionario)
                    self.diccionario[element] = content
                    self.diccionarioInverso[content] = element
                    self.writeCSV(element, content)
                    print (content)
                    return("200 OK", "<html><body>" + "<a href='" + self.diccionario[element] + "'>" + str(element) + "</a>" +
                            "   " + "<a href='" + content + "'>" + content + "</a></body></html>")
                else:
                    return("200 OK", "<html><body>La url ya esta cogida</body></html>")

if __name__ == "__main__":
    testWebApp = contentApp("localhost", 1234)
