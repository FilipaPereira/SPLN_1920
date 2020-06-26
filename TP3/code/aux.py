import re
import sys

def loadKnownTerms(filename):
    file = open(filename, 'r', encoding='utf-8')

    for line in file.read().split('\n'):
            if line.startswith('###'):
                dictName = line.split('###')[1]
                currentDict = dictName
                if dictName == 'Terms':
                    terms = {}      
                elif dictName == 'Classes':
                    classes = {}
                elif dictName == 'DatatypeProperties':
                    dataprops = {}
                elif dictName == 'ObjectProperties':
                    objprops = {}
            else:
                if currentDict == 'Terms':
                    ts = line.split()
                    if len(ts) == 2:
                        terms[ts[0]] = ts[1]
                elif currentDict == 'Classes':
                    ts = line.split()
                    if len(ts) == 2:
                        classes[ts[0]] = ts[1]
                elif currentDict == 'DatatypeProperties':
                    ts = line.split()
                    if len(ts) == 4:
                        dataprops[ts[0]] = (ts[1],ts[2],ts[3])
                elif currentDict == 'ObjectProperties':
                    ts = line.split()
                    if len(ts) == 4:
                        objprops[ts[0]] = (ts[1],ts[2],ts[3])

    return terms, classes, dataprops, objprops


def getOntology(filename):
    print(f'Parsing ontology from {filename}.')
    ontology = {}
    numTriploLidos = 0
    currentSubject = ''
    newSubject = True
    currentKey = ''
    with open(filename, 'r') as file:
        ontology['Classes'] = {}
        ontology['DatatypeProperties'] = {}
        ontology['ObjectProperties'] = {}
        ontology['Individuals'] = {}
        for line in file:
            res = re.findall(r"\".+\"", line)
            if len(res) > 0:
                string = res[0]
                ws = line.replace(string,'').split()
                string = string + ws[-1:][0]
                words = ws[:-1]
                words.append(string)
            else:
                words = line.split()
            if len(words) >= 2:
                if words[0] == 'Ontology':
                    ontology['ID'] = words[1].replace('.','')
                else:
                    if len(words) >= 3: ## se tem suj pred e obj
                        key = words[2].replace('.','').replace(';','')
                        if key == 'Class':
                            currentKey = 'Classes'
                        elif key == 'DatatypeProperty':
                            currentKey = 'DatatypeProperties'
                        elif key == 'ObjectProperty':
                            currentKey = 'ObjectProperties'
                        elif key == 'Individual':
                            currentKey = 'Individuals'

                    if newSubject == True:
                        currentSubject = words[0]
                        ontology[currentKey][currentSubject] = []
                        pred = words[1]
                        obj = words[2]
                    else:
                        pred = words[0]
                        obj = words[1]
                        
                    if words[-1][-1] == '.' or words[-1] == '.':
                        obj = obj.replace('.','')
                        newSubject = True
                    elif words[-1][-1] == ';' or words[-1] == ';':
                        obj = obj.replace(';','')
                        newSubject = False

                    tup = (pred,obj)
                    ontology[currentKey][currentSubject].append(tup)
                    numTriploLidos += 1
    print(f'Read {numTriploLidos} triples.')
    return ontology


prefixes = '''
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix schema: <http://schema.org/> .
@prefix dc: <http://purl.org/dc/elements/1.1/>.
'''

terms, classes, dataprops, objprops = loadKnownTerms('knownDict.txt')

def checkDomainRange(prop, tuples, knownProps):
    ret = ':'+prop
    ts = knownProps[prop]
    domain = ts[1]
    range = ts[2]
    ok = True
    
    for t in tuples:
        if ok and t[0] == 'domain':
            if domain != 'Thing' and t[1] != domain:
                ok = False
                print('Domain [%s] of property [%s] incompatible with domain for known property [%s].' % (t[1], prop, ts[0]))
            else:
                ret = ts[0]
        elif ok and t[0] == 'range':
            if range != 'Thing' and t[1] != range:
                ok = False
                print('Range [%s] of property [%s] incompatible with range for known property [%s].' % (t[1], prop, ts[0]))
            else:
                ret = ts[0]

    return ret

def groupTuples(tuples):
    grp = dict()

    for pred,obj in tuples:
        if pred not in grp:
            grp[pred] = [obj]
        else:
            grp[pred].append(obj)

    return grp


def writeClasses(out, namespace, cls):
    out.write(f'########## Classes ##########\n\n')
    
    for c in cls:
        if c in classes:
            curSubj = classes[c]
        else: 
            curSubj = ':'+c
        last = False
        out.write(f'### {namespace}{c}\n')
        tuples = cls[c]
    
        for t in tuples:
            pred = terms[t[0]]
            obj = ':'+t[1]
            if t[1] in terms:
                obj = terms[t[1]] 
            elif t[1] in classes:
                obj = classes[t[1]]
            if t == tuples[-1]:
                last = True
            if t != tuples[0]:
                curSubj = '\t'

            if last:
                out.write(f'{curSubj} {pred} {obj} .\n\n')
            elif not last:
                out.write(f'{curSubj} {pred} {obj} ;\n')

def writeDataprops(out, namespace, dprops):
    out.write(f'########## DataType Properties ##########\n\n')
    for pr in dprops:
        tuples = dprops[pr]
        if pr in dataprops:
            curSubj = checkDomainRange(pr, tuples, dataprops)
        else: 
            curSubj = ':'+pr
        last = False
        out.write(f'### {namespace}{pr}\n')
       
        for t in tuples:
            pred = terms[t[0]]
            obj = ':'+t[1]
            if t[1] in terms:
                obj = terms[t[1]] 
            elif t[1] in classes:
                obj = classes[t[1]]
            elif t[1] in dataprops:
                obj = checkDomainRange(t[1], dprops[t[1]], dataprops)
            if t == tuples[-1]:
                last = True
            if t != tuples[0]:
                curSubj = '\t'

            if last:
                out.write(f'{curSubj} {pred} {obj} .\n\n')
            elif not last:
                out.write(f'{curSubj} {pred} {obj} ;\n')

def writeObjprops(out, namespace, oprops):
    out.write(f'########## Object Properties ##########\n\n')
    for p in oprops:
        tuples = oprops[p]
        if p in objprops:
            curSubj = checkDomainRange(p, tuples, objprops)
        else: 
            curSubj = ':'+p
        last = False
        out.write(f'### {namespace}{p}\n')
       
        for t in tuples:
            pred = terms[t[0]]
            obj = ':'+t[1]
            if t[1] in terms:
                obj = terms[t[1]] 
            elif t[1] in classes:
                obj = classes[t[1]]
            elif t[1] in objprops:
                obj = checkDomainRange(t[1], oprops[t[1]], objprops)
            if t == tuples[-1]:
                last = True
            if t != tuples[0]:
                curSubj = '\t'

            if last:
                out.write(f'{curSubj} {pred} {obj} .\n\n')
            elif not last:
                out.write(f'{curSubj} {pred} {obj} ;\n')

def getObjWithType(prop, dprops):
    ret = ''
    ts = dict(dprops[prop])
    if 'range' in ts:
        range = ts['range'].lower()
        if range != 'int':
            ret = "^^xsd:%s" % range
    return ret
    
def getKnown(obj, cls):
    ret = obj
    if obj in terms:
        ret = terms[obj]
    elif obj in classes:
        ret = classes[obj]
    elif obj in cls:
        ret = ':' + obj
    return ret
            

def writeIndividuals(out, namespace, individuals, ontology):
    out.write(f'########## Individuals ##########\n\n')
    for ind in individuals:
        tuples = individuals[ind]
        out.write(f'### {namespace}{ind}\n')
        curSubj = ':'+ind
        grp = groupTuples(tuples)
        
        for pred in grp:
            curPred = ':'+pred
            objIndividual = False
            xsd = ''

            if pred in ontology['ObjectProperties']:
                objIndividual = True
            elif pred in ontology['DatatypeProperties']:
                xsd = getObjWithType(pred, ontology['DatatypeProperties'])
                

            if pred in terms:
                curPred = terms[pred]
            elif pred in objprops and pred in ontology['ObjectProperties']:
                curPred = checkDomainRange(pred, ontology['ObjectProperties'][pred], objprops)
            elif pred in dataprops and pred in ontology['DatatypeProperties']:
                curPred = checkDomainRange(pred, ontology['DatatypeProperties'][pred], dataprops)
                
            
            lastObj = False
            if len(grp[pred]) == 1:
                lastObj = True
            ##Se so tiver um predicado
            if len(list(grp)) == 1:
                for obj in grp[pred]:
                    if objIndividual:
                        curObj = ':'+obj
                    else:
                        curObj = getKnown(obj, ontology['Classes'])
                    if obj == grp[pred][-1]:
                        lastObj = True
                    if obj == grp[pred][0] and not lastObj:
                        out.write(f'{curSubj} {curPred} {curObj}{xsd} ,\n')
                        curSubj = '\t'
                        curPred = '\t'
                    elif lastObj:
                        out.write(f'{curSubj} {curPred} {curObj}{xsd} .\n\n')
                    else:
                        out.write(f'{curSubj} {curPred} {curObj}{xsd} ,\n')
            ##Se tiver no primeiro predicado
            elif pred == list(grp)[0]:
                for obj in grp[pred]:
                    if objIndividual:
                        curObj = ':'+obj
                    else:
                        curObj = getKnown(obj, ontology['Classes'])
                    if obj == grp[pred][-1]:
                        lastObj = True
                    if obj == grp[pred][0] and not lastObj:
                        out.write(f'{curSubj} {curPred} {curObj}{xsd} ,\n')
                        curSubj = '\t'
                        curPred = '\t'
                    elif lastObj:
                        out.write(f'{curSubj} {curPred} {curObj}{xsd} ;\n')
                    else:
                        out.write(f'{curSubj} {curPred} {curObj}{xsd} ,\n')

            ###Se tiver no ultimo predicado:
            elif pred == list(grp)[-1]:
                for obj in grp[pred]:
                    if objIndividual:
                        curObj = ':'+obj
                    else:
                        curObj = getKnown(obj, ontology['Classes'])
                    if obj == grp[pred][-1]:
                        lastObj = True
                    if lastObj:
                        out.write(f'{curSubj} {curPred} {curObj}{xsd} .\n\n')
                    elif obj == grp[pred][0]:
                        out.write(f'{curSubj} {curPred} {curObj}{xsd} ,\n')
                        curPred = '\t'
                    else:
                        out.write(f'{curSubj} {curPred} {curObj}{xsd} ,\n')
            else:
                for obj in grp[pred]:
                    if objIndividual:
                        curObj = ':'+obj
                    else:
                        curObj = getKnown(obj, ontology['Classes'])
                    if obj == grp[pred][-1]:
                        lastObj = True
                    if lastObj:
                        out.write(f'{curSubj} {curPred} {curObj}{xsd} ;\n')
                    elif obj == grp[pred][0]:
                        out.write(f'{curSubj} {curPred} {curObj}{xsd} ,\n')
                        curPred = '\t'
                    else:
                        out.write(f'{curSubj} {curPred} {curObj}{xsd} ,\n')
            
                
def expandOntology(ontology):
    id = ontology['ID']
    prefs = prefixes
    prefs += "@prefix : <http://ontology/2020/%s#> ." % id
    base = "<http://ontology/2020/%s>" % id
    prefs += '\n@base ' + base + ' .'

    fileOut = id + "_expanded.ttl"
    out = open(fileOut, "w")

    out.write(prefs)
    out.write(f'\n\n{base} rdf:type owl:Ontology .\n\n\n')

    namespace = "http://ontology/2020/%s#" % id
    print(f'Creating expanded ontology with namespace {namespace} to file: {fileOut}')
    print('Creating %d classes...' % len(ontology['Classes']))
    writeClasses(out, namespace, ontology['Classes'])

    print('Creating %d datatype properties...' % len(ontology['DatatypeProperties']))
    writeDataprops(out, namespace, ontology['DatatypeProperties'])

    print('Creating %d object properties...' % len(ontology['ObjectProperties']))
    writeObjprops(out, namespace, ontology['ObjectProperties'])
    print('Creating %d individuals...' % len(ontology['Individuals']))
    writeIndividuals(out, namespace, ontology['Individuals'], ontology)

    