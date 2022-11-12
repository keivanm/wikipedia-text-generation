#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import pgf
from int2numeral import int2numeral_in_tree
import sys
from collections import namedtuple
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

pgf_file = 'linkoping.pgf'
s = sys.argv[1]

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
        if 'capitalLabel' in r:
            municipalities[r['capitalLabel']['value']] = r['municipalityLabel']['value']
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
            if 'capitalLabel' in r:
                counties[r['capitalLabel']['value']] = r['countyLabel']['value']
    return counties


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
    city_pop = {k: v for k, v in sorted(city_pop.items(), key=lambda item: item[1], reverse=True)}
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
    for r in results['results']['bindings']:
            city = r['cityLabel']['value']
            

            if not city.startswith('Q'):
                location = r['locationLabel']['value']
                if city not in city_municipality and location.endswith(' kommun'):
                    city_municipality[city] = location
                
                #else:
                #    l = r['locationLabel']['value']
                #    cities[city] = [l]
    
    municipalities_counties = get_municipalities_in_counties()
    city_county = {}
    for city in city_municipality:
        city_county[city] = municipalities_counties[city_municipality[city]]
    
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

def round_population(population):
    population_str = str(population)
    if len(population_str) == (2 or 3):
        return population - (population%5)
    else:
        zeroes = len(population_str) - 3
        d = int(str(5) + '0' * zeroes)
        return population - (population%d)

def toDigits(population):
    population_str = str(population)
    l = len(population_str)
    c = population_str[-1]
    digits_gf = pgf.Expr('mkDigit{}'.format(c),[])
    for i in range(2,l+1, 1):
        c = population_str[-i]
        digits_gf = pgf.Expr('mkDigits{}'.format(c),[digits_gf])

    return digits_gf


def main():
    gr = pgf.readPGF(pgf_file)
    #countries = get_countries(country_file)
    swe = gr.languages['linkopingSwe']
    fre = gr.languages['linkopingFre']
    #jpn = gr.languages['linkopingJpn']
    eng = gr.languages['linkopingEng']
    city1 = s
    cities = get_cities()
    (rank, population) = get_rank_and_population(cities, city1)
    population = int(population)
    population_old = population
    population = round_population(population)
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
        line1 = pgf.Expr('Line1_one',[stad, city_in_county_gf, list_gf[0]])
    else:
        line1 = pgf.Expr('Line1_none',[stad, city_in_county_gf])


    rank_gf = pgf.readExpr('RankObject "{}"'.format(rank))
    population_gf1 = pgf.readExpr('PopulationObject "{}"'.format(population))
    #inhabitants = pgf.Expr('IntNumber', [inhabitants])

        
    text = None

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

    #numerals = {2: "second", 3: "third", 4: "fourth", 5: "fifth", 6: "sixth", 7: "seventh", 8: "eight", 9: "ninth",
               # 10: "tenth", 11: "eleventh"}
    population_gf = toDigits(population)

    if rank == 1:
        line3 = pgf.Expr('Line3_largest',[stad, population_gf])
    elif rank < 11:
        rank_gf = pgf.Expr('mkNumeral{}'.format(rank),[])
        line3 = pgf.Expr('Line3',[stad, rank_gf, population_gf])
    else:
        line3 = pgf.Expr('Line3_norank',[stad, population_gf])



    if line2 == None:
        text = pgf.Expr('Final_without_line2',[line1, line3])
    else:
        text = pgf.Expr('Final',[line1, line2, line3])

    print('\n')
    print(swe.linearize(text))
   
    print('\n')
    print(fre.linearize(text))

    print('\n')
    print(eng.linearize(text))
if __name__ == "__main__":
    main()

