#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import pgf
import sys
from collections import namedtuple
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
from random import randrange

pgf_file = 'linkoping.pgf'

def get_stiftstad():
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')
    sparql.setQuery("""
    SELECT ?churchLabel WHERE {
        SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],sv". }
        ?church wdt:P31 wd:Q66818387.
        ?church wdt:P17 wd:Q34.
    }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    churches = []
    for r in results['results']['bindings']:
            churches.append(r['churchLabel']['value'])
    #for church in churches:
        #print(church)
    return churches

def get_municipalities_shortname(municipality):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')
    sparql.setQuery("""
    SELECT ?municipalityLabel ?shortnameLabel WHERE {
        SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],sv". }
        ?municipality wdt:P31 wd:Q127448.
        OPTIONAL {?municipality wdt:P1813 ?shortname}
    }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    municipalities_shortnames = {}
    for r in results['results']['bindings']:
            if 'shortnameLabel' in r:
                municipalities_shortnames[r['municipalityLabel']['value']] = r['shortnameLabel']['value']
    municipalities_shortnames['Håbo kommun'] = 'Håbo'
    municipalities_shortnames['Mölndals kommun'] = 'Mölndal'
    municipalities_shortnames['Götene kommun'] = 'Götene'
    municipalities_shortnames['Vårgårda kommun'] = 'Vårgårda'
    municipalities_shortnames['Säffle kommun'] = 'Säffle'
    municipalities_shortnames['Vellinge kommun'] = 'Vellinge'
    municipalities_shortnames['Kungälvs kommun'] = 'Kungälv'
    municipalities_shortnames['Hagfors kommun'] = 'Hagfors'
    municipalities_shortnames['Vänersborgs kommun'] = 'Vänersborg'
    municipalities_shortnames['Stenungsunds kommun'] = 'Stenungsund'
    municipalities_shortnames['Hultsfreds kommun'] = 'Hultfred'
    municipalities_shortnames['Eksjö kommun'] = 'Eksjö'
    municipalities_shortnames['Jokkmokks kommun'] = 'Jokkmokk'
    municipalities_shortnames['Kävlinge kommun'] = 'Kävlinge'
    municipalities_shortnames['Härjedalens kommun'] = 'Härjedalen'
    municipalities_shortnames['Krokoms kommun'] = 'Krokom'
    municipalities_shortnames['Nordmalings kommun'] = 'Nordmaling'
    municipalities_shortnames['Ljusnarsbergs kommun'] = 'Ljusnarsberg'
    municipalities_shortnames['Mörbylånga kommun'] = 'Mörbylånga'
    municipalities_shortnames['Strömsunds kommun'] = 'Strömsund'
    municipalities_shortnames['Nordanstigs kommun'] = 'Nordanstig'
    municipalities_shortnames['Bromölla kommun'] = 'Bromölla'
    municipalities_shortnames['Lindesbergs kommun'] = 'Lindesberg'
    municipalities_shortnames['Ljusdals kommun'] = 'Ljusdal'
    municipalities_shortnames['Mönsterås kommun'] = 'Mönsterås'
    municipalities_shortnames['Skurups kommun'] = 'Skurup'
    municipalities_shortnames['Lekebergs kommun'] = 'Lekeberg'
    municipalities_shortnames['Kinda kommun'] = 'Kinda'
    municipalities_shortnames['Nybro kommun'] = 'Nybro'
    municipalities_shortnames['Laxå kommun'] = 'Laxå'
    municipalities_shortnames['Ragunda kommun'] = 'Ragunda'
    municipalities_shortnames['Lidköpings kommun'] = 'Lidköping'
    municipalities_shortnames['Ronneby kommun'] = 'Ronneby'
    municipalities_shortnames['Sölvesborgs kommun'] = 'Sölvesborg'
    municipalities_shortnames['Västerviks kommun'] = 'Västervik'
    municipalities_shortnames['Tingsryds kommun'] = 'Tingsryd'
    municipalities_shortnames['Uppvidinge kommun'] = 'Uppvidinge'
    municipalities_shortnames['Tomelilla kommun'] = 'Tomelilla'
    municipalities_shortnames['Torsås kommun'] = 'Torsås'
    municipalities_shortnames['Ydre kommun'] = 'Ydre'
    municipalities_shortnames['Svedala kommun'] = 'Svedala'
    municipalities_shortnames['Vilhelmina kommun'] = 'Vilhelmina'
    municipalities_shortnames['Vadstena kommun'] = 'Vadstena'
    municipalities_shortnames['Heby kommun'] = 'Heby'
    municipalities_shortnames['Södertälje kommun'] = 'Södertälje'
    municipalities_shortnames['Vaggeryds kommun'] = 'Vaggeryd'
    municipalities_shortnames['Borås kommun'] = 'Borås'
    municipalities_shortnames['Nacka kommun'] = 'Nacka'
    municipalities_shortnames['Lycksele kommun'] = 'Lycksele'
    municipalities_shortnames['Sundbybergs kommun'] = 'Sundbyberg'
    municipalities_shortnames['Karlskrona kommun'] = 'Karlskrona'
    municipalities_shortnames['Eslövs kommun'] = 'Eslöv'
    municipalities_shortnames['Säters kommun'] = 'Säter'
    municipalities_shortnames['Gagnefs kommun'] = 'Gagnef'
    municipalities_shortnames['Lidingö kommun'] = 'Lidingö'
    return municipalities_shortnames[municipality]

def get_municipalities():
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')
    sparql.setQuery("""
    SELECT ?municipalityLabel ?capitalLabel WHERE {
        SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],sv". }
        ?municipality wdt:P31 wd:Q127448.
        OPTIONAL {?municipality wdt:P36 ?capital.}
    }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    municipalities = {}
    for r in results['results']['bindings']:
            municipalities[r['capitalLabel']['value']] = r['municipalityLabel']['value']
   #for municipality in municipalities:
        #print(municipality, ':', municipalities[municipality])
    return municipalities


def get_county_residensstad():
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')
    sparql.setQuery("""
    SELECT ?countyLabel ?capitalLabel WHERE {
        SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],sv". }
        ?county wdt:P31 wd:Q200547.
        OPTIONAL {?county wdt:P36 ?capital.}
        
    }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    counties = {}
    for r in results['results']['bindings']:
            #print('hej')
            if 'capitalLabel' in r:
                counties[r['capitalLabel']['value']] = r['countyLabel']['value']
    #for county in counties:
        #print(county, ':', counties[county])
    return counties


"""def get_cities():
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')
    sparql.setQuery(
    SELECT ?cityLabel ?population WHERE {
    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],sv". }
    VALUES ?town_or_city {
        wd:Q1549591
        wd:Q515
    }
    ?city wdt:P31 ?town_or_city;
        wdt:P17 wd:Q34.
    OPTIONAL { ?city wdt:P1082 ?population. }
    
    }
    )
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    city_pop = {}
    for r in results['results']['bindings']:
        if 'population' in r:
            city_pop[r['cityLabel']['value']] = int(r['population']['value'])
    city_pop = {k: v for k, v in sorted(city_pop.items(), key=lambda item: item[1], reverse=True)}
    for city in city_pop:
        print(city, ':', city_pop[city])
    return city_pop """

def get_cities():
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')
    sparql.setQuery("""
    SELECT ?cityLabel ?population WHERE {
    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],sv". }
    VALUES ?town_or_city {
        wd:Q12813115
    }
    ?city wdt:P31 ?town_or_city;
        wdt:P17 wd:Q34.
    OPTIONAL { ?city wdt:P1082 ?population. }
    
    }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    city_pop = {}
    for r in results['results']['bindings']:
        if 'population' in r:
            city_pop[r['cityLabel']['value']] = int(r['population']['value'])
        else:
            city_pop[r['cityLabel']['value']] = 0
    city_pop = {k: v for k, v in sorted(city_pop.items(), key=lambda item: item[1], reverse=True)}
    #for city in city_pop:
        #print(city, ':', city_pop[city])
    return city_pop

def get_municipalities_in_counties():
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')
    sparql.setQuery("""
    SELECT ?municipalityLabel ?countyLabel WHERE {
        SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],sv". }
        ?municipality wdt:P31 wd:Q127448.
        OPTIONAL {?municipality wdt:P131 ?county.}
    }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    municipalities = {}
    for r in results['results']['bindings']:
            municipalities[r['municipalityLabel']['value']] = r['countyLabel']['value']
    #for municipality in municipalities:
     #   print(municipality, ':', municipalities[municipality])
    return municipalities


def get_cities_in_counties():
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')
    sparql.setQuery("""SELECT ?cityLabel ?locationLabel WHERE {
    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],sv". }
    VALUES ?town_or_city {
        wd:Q12813115
    }
    ?city wdt:P31 ?town_or_city;
        wdt:P17 wd:Q34.
    OPTIONAL { ?city wdt:P131 ?location.}
    
    }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    city_municipality = {}
    #print(results['results']['bindings'])
    for r in results['results']['bindings']:
            city = r['cityLabel']['value']
            

            if not city.startswith('Q'):
                location = r['locationLabel']['value']
                if city not in city_municipality and (location.endswith(' kommun') or location == 'Region Gotland'):
                    city_municipality[city] = location
                
                #else:
                #    l = r['locationLabel']['value']
                #    cities[city] = [l]
    
    municipalities_counties = get_municipalities_in_counties()
    city_county = {}
    for city in city_municipality:
        city_county[city] = municipalities_counties[city_municipality[city]]
        #print(city, ':', municipalities_counties[city_municipality[city]])
    
    return city_county

def get_universities():
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')
    sparql.setQuery("""SELECT ?universityLabel ?locationLabel ?dateLabel WHERE {
        SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],sv". }
        ?university wdt:P31 wd:Q3918.
        ?university wdt:P17 wd:Q34.
        OPTIONAL {?university wdt:P276 ?location.}
        OPTIONAL {?university wdt:P571 ?date.}
    }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    universities = {}
    #print(results['results']['bindings'])
    for r in results['results']['bindings']:
            university = r['universityLabel']['value']
            
            location = None 
            if 'locationLabel' in r:
                location = r['locationLabel']['value']
            
            date = r['dateLabel']['value']
            i = date.find('-')
            date = date[0:i]            #only get the year

            if not location in universities:
                universities[location] = []
                universities[location].append((university, date))
            else:
                universities[location].append((university, date))

            universities[location]
    
    #for l in universities:
        #print(l, ": ", universities[l])
    
    return universities

#can be done because no county normally ends with an 's'
def remove_ending_county(name): 
    name = name.rsplit(' ', 1)[0]
    if name[-1] == 's':
        name = name[:-1]  #västra götalands län => västra götaland
    
    return name

def remove_ending_diocese(name): 
    name = name.rsplit(' ', 1)[0]
    if name.startswith('Strängnäs') or name.startswith('Västerås'):
        return name
    if name[-1] == 's':
        name = name[:-1]  #västra götalands län => västra götaland
    
    return name

#return rank with index starting at 1
def get_rank_and_population(cities, cityName):
    return (list(cities).index(cityName) + 1, cities[cityName])

def get_city2(cities, rank):
    return list(cities)[rank-2]

def create_nameobject(name):
    isFem = check_gender(name)
    lastletter = name[-1]
    # Alingsås Höganäs Tranås Kalix Kalmar
    if lastletter in "aeiouyåäösx" or name == "Kalmar":
        nameObject = pgf.readExpr('NameObject_vowel "{}"'.format(name))
    else:
        nameObject = pgf.readExpr('NameObject_consonant "{}"'.format(name))
    
    if isFem:
        return pgf.Expr('pn_fem',[nameObject])
    
    else:
        return pgf.Expr('pn_masc',[nameObject])


def check_gender(name):
    lastletter = name[-1]
    isFem = False
    if lastletter == 'e':
        isFem = True
    return isFem

def run_gf(city):
    gr = pgf.readPGF(pgf_file)
    #countries = get_countries(country_file)
    swe = gr.languages['linkopingSwe']
    fre = gr.languages['linkopingFre']
    #jpn = gr.languages['linkopingJpn']
    eng = gr.languages['linkopingEng']
    city1 = city
    cities = get_cities()
    (rank, population) = get_rank_and_population(cities, city1)
    #print(population)
    #print(rank)
    municipalities = get_municipalities()

    line1_list = []
    if city1 in municipalities:
        centralort = municipalities[city1]
        centralort = get_municipalities_shortname(centralort)
        centralort_gf = create_nameobject(centralort)
        line1_2 = pgf.Expr('Line1_2',[centralort_gf])
        line1_list.append(line1_2)

    counties = get_county_residensstad()
    if city1 in counties: 
        residensstad = counties[city1]
        residensstad = remove_ending_county(residensstad)
        #residensstad = counties[city1].rsplit(' ', 1)[0]
        #residensstad = residensstad[:-1]
        #print(residensstad)
        residensstad_gf = create_nameobject(residensstad)
        line1_3 = pgf.Expr('Line1_3',[residensstad_gf])
        line1_list.append(line1_3)
    

    churches = get_stiftstad()
    for c in churches:           
        if city1 in c:
            stiftstad = c
            stiftstad = remove_ending_diocese(stiftstad)
            stiftstad_gf = create_nameobject(stiftstad)
            line1_4 = pgf.Expr('Line1_4',[stiftstad_gf])
            line1_list.append(line1_4)
            break
    

    cities_counties = get_cities_in_counties()
    city_in_county = cities_counties[city1]
    city_in_county = remove_ending_county(city_in_county)

    
    stad = pgf.readExpr('NameObject "{}"'.format(city1))

    city_in_county_gf = create_nameobject(city_in_county)

    #line1_list_gf = pgf.Expr('create_list',line1_list)
    if len(line1_list) == 2:
        list_gf = pgf.Expr('create_list',line1_list)
        line1 = pgf.Expr('Line1',[stad, city_in_county_gf, list_gf])
    elif len(line1_list) > 2:
        length = len(line1_list)
        list_gf = pgf.Expr('create_list',[line1_list[length-2], line1_list[length-1]])
        for i in range(length-3, -1, -1):
            list_gf = pgf.Expr('add_line',[line1_list[i], list_gf])
        line1 = pgf.Expr('Line1',[stad, city_in_county_gf, list_gf])
    elif len(line1_list) == 1: 
        line1 = pgf.Expr('Line1_one',[stad, city_in_county_gf, line1_list[0]])
    else:
        line1 = pgf.Expr('Line1_none',[stad, city_in_county_gf])


    rank_gf = pgf.readExpr('RankObject "{}"'.format(rank))
    inhabitants = pgf.readExpr('InhabitantsObject "{}"'.format(population))
    
        
    text = None

    #if rank == 1:
     #   line2 = pgf.Expr('Line2_storsta',[stad])


    #else:
        #city2 = get_city2(cities, rank)
        #print(city2)
        #_,tree = swe.parse("{}".format(rank)).__next__()
        #tf = int2numeral_in_tree("IntNumber","NumeralNumber",tree)
        #bj = pgf.readExpr('NumeralNumber "{}"'.format(tf))
        #print(bj)
        #bj = pgf.Expr('NumeralNum',[tf])
        #print(tf)
    universities = get_universities()
    if city1 in universities: 
        universities_in_city = universities[city1]
        universities_gf = []
        for university in universities_in_city:
            name = university[0]
            inception_year = university[1]
            name_gf = pgf.readExpr('UniversityObject "{}"'.format(name))
            inception_year_gf = pgf.readExpr('YearObject "{}"'.format(inception_year))
            university_gf = pgf.Expr('create_university',[name_gf, inception_year_gf])
            universities_gf.append(university_gf)

        #list_gf = pgf.Expr('create_universities_list',universities_gf)
        if len(universities_gf) == 2:
            list_gf = pgf.Expr('create_universities_list',universities_gf)
            line2 = pgf.Expr('Line2',[stad, list_gf])
        elif len(universities_gf) > 2:
            list_gf = pgf.Expr('create_universities_list',[universities_gf[0], universities_gf[1]])
            for i in range(2, len(universities_gf)):
                list_gf = pgf.Expr('add_university',[universities_gf[i], list_gf])
            line2 = pgf.Expr('Line2',[stad, list_gf])
        elif len(universities_gf) == 1: 
            line2 = pgf.Expr('Line2_one',[stad, universities_gf[0]])
    else:
        line2 = None

    
    line3 = pgf.Expr('Line3',[stad, rank_gf, inhabitants])

    if line2 == None:
        text = pgf.Expr('Final_without_line2',[line1, line3])
    else:
        text = pgf.Expr('Final',[line1, line2, line3])


    print('\n')
    print(swe.linearize(text))
    print('\n')
    print(fre.linearize(text))
    """
    print('\n')
    print(jpn.linearize(text))
   """
    print('\n')
    print(eng.linearize(text))
    print('\n')
    print("-----------------------------------------------")


def run_100():
    cities = get_100_cities()
    for city in cities:
        run_gf(city)

def get_100_cities():
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')
    sparql.setQuery("""
    SELECT ?cityLabel WHERE {
    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],sv". }
    VALUES ?town_or_city {
        wd:Q12813115
    }
    ?city wdt:P31 ?town_or_city;
        wdt:P17 wd:Q34.
    }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    cities = []
    for r in results['results']['bindings']:
        cities.append(r['cityLabel']['value'])
    
    limit = len(cities)
    _100_cities = []
    for i in range(0, 100):
        rand = randrange(limit)
        _100_cities.append(cities[rand])

    return _100_cities

def main():
    run_100()

if __name__ == "__main__":
    main()

