from aux import getOntology, loadKnownTerms, expandOntology
import os
import sys
import shutil

####Dictionaries with known terms, classes and properties from foaf and schema ontologies
terms, classes, dataprops, objprops = loadKnownTerms('knownDict.txt')

inline = ['Image','Imagem','Picture','Foto','Photo']

###Writes HTML for the listing of Classes 
def writeClassTable(classes, individuals):
    text = '''
           <div class="w3-container">
                <div class="w3-card-4">
                    <header class="w3-container w3-blue w3-margin-top">
                        <h3>  Classes </h3>
                    </header>
                    <table class="w3-table-all">
        '''

    for c in classes:
        tuples = classes[c]
        row = '''
            <tr>
                <td><a href="./class_%s.html">%s %s %s</a></td>
            <tr>
        '''
        indsOfClass = []
        for ind in individuals:
            ts = individuals[ind]
            for t in ts:
                if t[0] == 'a' and t[1] == c:
                    indsOfClass.append(ind)

        if len(tuples) > 1:
            text += row % (c, c,'('+tuples[1][0], tuples[1][1]+')')
            writeClassPage(c,tuples[1][1], indsOfClass)
        else:
            text += row % (c, c, '', '')
            writeClassPage(c,'', indsOfClass)

    text += '''
                </table>
            </div>
        </div>
        '''
    return text

###Writes HTML for each class page, which the individuals that belong to the class
def writeClassPage(idclass,subclass,individuals):
    with open('./html/class_'+idclass+'.html', 'w') as myFile:
        top = '''
            <!DOCTYPE html>
            <html>
                <head>
                <title>%s</title>
                <link rel="stylesheet" type="text/css" href="style.css">
                </head>

                <body>
            '''

        row = '''
            <div class="w3-container">
                <header class="w3-container w3-light-blue w3-margin-top">
                <h3>Class: %s</h3>
                <h4>%s</h4>
                </header>

                '''

        text = top % idclass
        if subclass != '':
            text += row % (idclass, '(subClassOf ' + subclass +')')
        else: 
            text += row % (idclass, '')

        if idclass in classes:
            row2 = '''
            <p class="w3-panel w3-pale-blue w3-ul w3-border">
               Equivalent to => <b>%s</b>
            </p> 
                '''
            text += row2 % classes[idclass]
                          
                
        text += ''' 
                <ul class="w3-panel w3-pale-blue w3-ul w3-border">
                    <li><h3>Individuals:</h3></li>
            '''

        for ind in individuals:
            text += '<li><a href="./individual_%s.html">%s</a></li>' % (ind, ind)
    

        text += '''
                        </ul>
                    </div>
                    <div align="center">
                        <a href="./mainPage.html"><button class="w3-button w3-black w3-margin">Main Page</button></a>
                    </div>
                </body>
            </html>
            '''
        
      
        myFile.write(text)

###Writes HTML for the listing of Properties 
def writePropsTable(dataprops, objprops):
    text = '''
           <div class="w3-container">
                <div class="w3-card-4">
                    <header class="w3-container w3-blue w3-margin-top">
                        <h3>  Properties </h3>
                    </header>
                    <table class="w3-table-all">
        '''

    props = dict(dataprops)
    props.update(objprops)

    for k, v in sorted(props.items()):
        writePropPage(k, v)
        row = '''
            <tr>
                <td><a href="./property_%s.html">%s</a></td>
            </tr>
            '''
        text += row % (k,k)

    text += '''
                </table>
            </div>
        </div>
    '''    
    return text

###Writes HTML page of each property, datatype and object
def writePropPage(idprop, tuples):
    with open('./html/property_'+idprop+'.html', 'w') as myFile:
        top = '''
            <!DOCTYPE html>
            <html>
                <head>
                <title>%s</title>
                <link rel="stylesheet" type="text/css" href="style.css">
                </head>

                <body>
                    <div class="w3-container">
                    <header class="w3-container w3-light-blue w3-margin-top">
                        <h3>Property: %s</h3>
                    </header>
            '''

        row = '''
                <div class="w3-panel w3-pale-blue w3-border">
                    <table class="w3-table">
                        <tr><th>Property Type</th><td>%s</td></tr>
                        <tr><th>Domain</th><td>%s</td></tr>
                        <tr><th>Range</th><td>%s</td></tr>
                        <tr><th>Inverse Of</th>%s</td></tr>
                    </table>
                </div>
            </div>
        '''
        domain = '' 
        range = ''
        inv =''

        for t in tuples:
            if t[0] == 'domain':
                domain = t[1]
            if t[0] == 'range':
                range = t[1]
            if t[0] == 'inverseOf':
                inv = t[1]

        text = top % (idprop,idprop)

        ok = True
        if tuples[0][1] == 'DatatypeProperty':
            propTipo = "DataType Property"
            if idprop in dataprops:
                if ok and dataprops[idprop][1] != 'Thing' and domain !='' and dataprops[idprop][1] != domain:
                    ok = False
                elif ok and dataprops[idprop][2] != 'Thing' and range !='' and dataprops[idprop][2] != range:
                    ok = False
                else: 
                    row2 = '''
                    <p class="w3-panel w3-pale-blue w3-ul w3-border">
                    Equivalent to => <b>%s</b>
                    </p> 
                    '''
                    text += row2 % dataprops[idprop][0]
        else:
            propTipo = "Object Property"
            if idprop in objprops:
                if ok and objprops[idprop][1] != 'Thing' and domain !='' and objprops[idprop][1] != domain:
                    ok = False
                elif ok and objprops[idprop][2] != 'Thing' and range !='' and objprops[idprop][2] != range:
                    ok = False
                else: 
                    row2 = '''
                    <p class="w3-panel w3-pale-blue w3-ul w3-border">
                    Equivalent to => <b>%s</b>
                    </p> 
                    '''
                    text += row2 % objprops[idprop][0]

        
        text += row % (propTipo, domain, range, inv)

        
        if domain != '' and range != '':
            r = '''
                <div> 
                    <h4 align="center"> <b>%s</b> <u>%s</u> <b>%s</b></h4>
                </div>
            '''
            if propTipo == "DataType Property":
                range = '[' + range + ']'
            text += r % (domain,idprop,range)
        
        text += '''
                    <div align="center">
                        <a href="./mainPage.html"><button class="w3-button w3-black w3-margin">Main Page</button></a>
                    </div>
                </body>
            </html>
            '''
        myFile.write(text)


###Writes HTML for the listing of Individuals 
def writeIndividualsTable(ontology):
    individuals = ontology['Individuals']
    text = '''
           <div class="w3-container">
                <div class="w3-card-4">
                    <header class="w3-container w3-blue w3-margin-top">
                        <h3>  Individuals </h3>
                    </header>
                    <table class="w3-table-all">
        '''

    for k, v in sorted(individuals.items()):
        writeIndividualPage(k, v, ontology)
        row = '''
            <tr>
                <td><a href="./individual_%s.html">%s</a></td>
            </tr>
            '''
        text += row % (k,k)

    text += '''
                </table>
            </div>
        </div>
    '''    
    return text

###Writes the HTML page of each individual, with their respective properties
def writeIndividualPage(idIndividual, tuples, ontology):
    individuals = ontology['Individuals']
    dataprops = ontology['DatatypeProperties']
    objprops = ontology['ObjectProperties']
    with open('./html/individual_'+idIndividual+'.html', 'w') as myFile:
        top = '''
            <!DOCTYPE html>
            <html>
                <head>
                <title>%s</title>
                <link rel="stylesheet" type="text/css" href="style.css">
                </head>

                <body>
                <div class="w3-container">
                    <header class="w3-container w3-light-blue w3-margin-top">
                    <h3>Individual: %s</h3>
                    </header>
                    <div class="w3-panel w3-pale-blue w3-border">
                        <table class="w3-table">
                            <tr><th>Class</th><td><a href="./class_%s.html">%s</a></td></tr>
                        </table>
                    </div>
                </div>
            '''
        
        dataps = []
        rels = []
        for t in tuples:
            if t[0]  == 'a' and t[1] != 'Individual':
                classe = t[1]
            elif t[0] != 'a':
                if t[0] in dataprops:
                    dataps.append(t)
                elif t[0] in objprops:
                    rels.append(t)

        text = top % (idIndividual,idIndividual,classe,classe)
        #############Datatype Properties table
        topTable = '''
            <div class="w3-container">
                    <header class="w3-container w3-light-blue w3-margin-top">
                    <h3>DataType Properties:</h3>
                    </header>
                    <div class="w3-panel w3-pale-blue w3-border">
                        <table class="w3-table">
        '''
        text += topTable
        for dt in dataps:
            text += '<tr><th>%s</th><td>%s</td></tr>' % (dt[0],dt[1])
                  
        text += '''
                </table>
            </div>
        </div>
        '''
        #############Object Properties listing
        text += '''
            <div class="w3-container">
                    <header class="w3-container w3-light-blue w3-margin-top">
                    <h3>Object Properties:</h3>
                    </header>
                    <ul class="w3-panel w3-pale-blue w3-ul w3-border">
        '''

        for r in rels:
            urlObj = ifImageGetLink(individuals[r[1]])
            urlSubj = ifImageGetLink(tuples)
            if urlObj != '':
                text += '<li>%s &rarr; %s &rarr; <a href="./individual_%s.html"><img src="%s" alt="%s" width="150" height="150"></a></li>' % (idIndividual, r[0], r[1], urlObj, r[1])
            elif urlSubj != '':
                text += '<li><img src="%s" alt="%s"  width="150" height="150"> &rarr; %s &rarr; <a href="./individual_%s.html">%s</a></li>' % (urlSubj, idIndividual,r[0], r[1], r[1])
            else:
                text += '<li>%s &rarr; %s &rarr; <a href="./individual_%s.html">%s</a></li>' % (idIndividual, r[0], r[1], r[1])

        text += '''
                        </ul>
                    </div>
                    <div align="center">
                    <a href="./mainPage.html"><button class="w3-button w3-black w3-margin">Main Page</button></a>
                    </div>
                </body>
            </html>
            '''      
        myFile.write(text)

###Get URL of image if it is to display an image
def ifImageGetLink(tuples):
    flag = 0
    for t in tuples:
        if t[0] == 'a' and t[1] in inline:
            flag = 1
        elif flag and t[0] == 'contentUrl':
            return "../"+t[1].replace('"','')
    return ''
            
def mainPageHtml(ontology):
    with open('./html/mainPage.html', 'w') as myFile:
        text = ''
        top = '''
            <!DOCTYPE html>
            <html>
                <head>
                <title>%s</title>
                <link rel="stylesheet" type="text/css" href="style.css">
                </head>

                <body>
            '''
        tableClasses = writeClassTable(ontology['Classes'], ontology['Individuals'])
        tableProps = writePropsTable(ontology['DatatypeProperties'], ontology['ObjectProperties'])
        tableInds = writeIndividualsTable(ontology)
        end = '''
                </body>
            </html>
            '''

      
        text += top % ontology['ID'] + tableClasses + tableProps + tableInds + end
        myFile.write(text)



def helpInfo():
    print('##############################################################')
    print('[USAGE]: ontology2html.py <filename>\n')
    print('The file should consist of a simplified ontology in Turtle:\n')
    print('Ontology OntologyName.\n')
    print('<Class Examples>')
    print('ClassName1   a   Class;')
    print('             subClass   ClassName2.\n')
    print('ClassName2   a   Class.\n')
    print('<DatatypeProperties Examples>')
    print('prop1   a   DatatypeProperty;')
    print('        domain   ClassName1.\n')
    print('prop2   a   DatatypeProperty;')
    print('        domain   ClassName2;')
    print('        range   String.\n')
    print('<ObjectProperties Examples>')
    print('prop3   a   ObjectProperty;')
    print('        inverseOf   prop4.\n')
    print('prop4   a   ObjectProperty;')
    print('        domain   ClassName2;')
    print('        range   ClassName3.\n')
    print('<Individuals Examples>')
    print('Ind1   a   Individual;')
    print('       a   ClassName1.\n')
    print('Ind2   a   Individual;')
    print('       a   ClassName2;')
    print('       prop2  "text text";')
    print('       prop4  Ind1.\n\n')
    print('To represent images in your ontology define the datatypeproperty contentUrl as a String corresponding to the path of the image.')
    print('##############################################################')

def program():
    arg = sys.argv[1]
    if arg == '-h':
        helpInfo()
    else:
        ##Parse simplified ontology
        ont = getOntology(arg)
        ##Expand ontology with namespaces and known classes/properties
        expandOntology(ont)
        ##Write HTML
        mainPageHtml(ont)
    
                

###Create HTML folder and move style.css there
if os.path.isdir('./html') == False:
    os.mkdir('./html')
    shutil.move('./style.css','./html/style.css')
    

program()




                
            
