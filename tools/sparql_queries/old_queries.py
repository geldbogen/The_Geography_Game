# Woman died at least 500 years ago
historical_women_query = '''SELECT DISTINCT ?pageid ?novelist ?novelistLabel ?countryLabel ?sitelinks WHERE {
    
                            SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
                            hint:Query hint:optimizer "None".
                            
                            VALUES ?country {'''+item+'''}
                            
                            
                            {?novelist wdt:P27 ?country;
                                        wikibase:sitelinks ?sitelinks
                            filter(?sitelinks>0)} 
                            UNION
                            {?novelist wdt:P19 [wdt:P17 ?country];
                                        wikibase:sitelinks ?sitelinks.
                            filter(?sitelinks>0)}
                                    
                            ?novelist wdt:P21 wd:Q6581072.
                            ?novelist wdt:P570 ?date.
                            filter(YEAR(?date)<=1523)
                            
                            }
                            ORDER BY DESC(?sitelinks)
                            LIMIT 50
                            
                            '''

# most famous desert in a country
desert_query = '''
            SELECT DISTINCT ?pageid ?novelist ?novelistLabel ?countryLabel ?sitelinks WHERE {
    
            SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
            hint:Query hint:optimizer "None".
            
            VALUES ?country {'''+item+'''}
            
            
            {?novelist wdt:P17 ?country;
                        wikibase:sitelinks ?sitelinks
            filter(?sitelinks>0)} 
            UNION
            {?novelist wdt:P276 [wdt:P17 ?country];
                        wikibase:site ?sitelinks.
            filter(?sitelinks>0)}
                    
            wd:Q8514 ^wdt:P279*/^wdt:P31 ?novelist
            
            }
            ORDER BY DESC(?sitelinks)
            
            '''

# most famous companies in a country (except Airlines and National Banks)
geographical_object_query = '''SELECT DISTINCT ?pageid ?novelist ?novelistLabel ?countryLabel ?sitelinks WHERE {
    
            SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
            hint:Query hint:optimizer "None".
            
            VALUES ?country {'''+item+'''}
            
            wd:Q4830453 ^wdt:P279*/^wdt:P31 ?novelist.
            
            ?novelist wdt:P17 ?country;
                      wikibase:sitelinks ?sitelinks.
            MINUS {?novelist wdt:P31 wd:Q46970}
            MINUS {?novelist wdt:P31 wd:Q6579042}
  
            
            }
            ORDER BY DESC(?sitelinks)
            LIMIT 50
            '''

# most famous beverage in a country
beverage_query = '''
            SELECT DISTINCT ?pageid ?novelist ?novelistLabel ?countryLabel ?sitelinks WHERE {
    
            SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
            hint:Query hint:optimizer "None".
            
            VALUES ?country {'''+item+'''}
            
            wd:Q40050 ^wdt:P279*/^wdt:P31* ?novelist.
            ?novelist wdt:P495 ?country;
                      wikibase:sitelinks ?sitelinks
            }
            ORDER BY DESC(?sitelinks)
            LIMIT 50
            '''
# most famous young person in a country
young_women_and_men_query = '''
            SELECT DISTINCT ?pageid ?novelist ?novelistLabel ?countryLabel ?sitelinks WHERE {
    
            SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
            hint:Query hint:optimizer "None".
            
            VALUES ?country {''' + item + '''}
            
            
            {?novelist wdt:P27 ?country;
                        wikibase:sitelinks ?sitelinks
            filter(?sitelinks>0)} 
            UNION
            {?novelist wdt:P19 [wdt:P17 ?country];
                        wikibase:sitelinks ?sitelinks.
            filter(?sitelinks>0)}
                    
            ?novelist wdt:P569 ?date.
            filter(YEAR(?date)>=2000)
            
            }
            ORDER BY DESC(?sitelinks)
            LIMIT 50
            '''
# query where things are located (museums, hotels, etc.)
where_located_query = '''  
            SELECT DISTINCT ?novelist ?novelistLabel ?countryLabel ?sitelinks WHERE {
            SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". } 
            VALUES ?country {'''+item+'''}
            wd:Q33506 ^wdt:P279*/^wdt:P31 ?novelist.
            ?novelist wdt:P17 ?country;
                        wikibase:sitelinks ?sitelinks.
            filter(?sitelinks>0)
            
            
            }
            ORDER BY DESC(?sitelinks)
            LIMIT 10
            '''

most_famous_person_born_after_query = '''
            SELECT ?pageid ?novelist ?novelistLabel (COUNT(?person) AS ?sitelinks) ?countryLabel WHERE {
            SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
            VALUES ?country {''' + item + '''}
            {?person wdt:P27 ?country.}
            UNION
            {?person wdt:P19 [ wdt:P17 ?country]}
            ?person wdt:P569 ?dateofbirth.
            ?person wikibase:sitelinks ?real_sitelinks.
            
            filter(?real_sitelinks >0)
            filter(YEAR(?dateofbirth)>1900)
            }
            GROUP BY ?countryLabel ?pageid ?novelist ?novelistLabel
            '''

# query for most famous architectural structure in a country
architectural_structure_query = '''
            SELECT DISTINCT ?novelist ?novelistLabel ?countryLabel ?sitelinks WHERE { 
            SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
            hint:Query hint:optimizer "None".
                        VALUES ?country {'''+item + '''}
                        ?novelist wdt:P17 ?country.
                        ?novelist wikibase:sitelinks ?sitelinks.    
                        filter(?sitelinks>70)
                        
                        
                        wd:Q811979 ^wdt:P279*/^wdt:P31 ?novelist
                        
            MINUS {?novelist wdt:P31 wd:Q1248784}
            MINUS {?novelist wdt:P31 wd:Q644371}
            }
            ORDER BY DESC(?sitelinks)
            
            
            '''

# most famous airlines in a country
airline_query = '''
            SELECT DISTINCT ?pageid ?novelist ?novelistLabel ?countryLabel ?sitelinks WHERE {
    
            SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
            hint:Query hint:optimizer "None".
            
            VALUES ?country {'''+item + '''}
            
            ?novelist wdt:P159 [wdt:P17 ?country].
            ?novelist wdt:P17 ?country;
             wikibase:sitelinks ?sitelinks
            filter(?sitelinks>0) 
            
                    
            wd:Q46970 ^wdt:P279*/^wdt:P31 ?novelist
            
            }
            ORDER BY DESC(?sitelinks)
            LIMIT 200
            
            '''

# query for most famous geographical object in a country
geographical_object_query = '''
            SELECT DISTINCT ?novelist ?novelistLabel ?sitelinks ?countryLabel WHERE {
            hint:Query hint:optimizer "None".
            VALUES ?country {'''+item + '''}
            ?novelist wdt:P17 ?country.
            ?novelist wikibase:sitelinks ?sitelinks.
            filter(?sitelinks>20)
            wd:Q35145263 ^wdt:P279*/^wdt:P31 ?novelist.
            ?novelist rdfs:label ?novelistLabel.
            filter(LANG(?novelistLabel)="en")
            ?country rdfs:label ?countryLabel.
            filter(LANG(?countryLabel)="en")
            }
            ORDER BY DESC(?sitelinks)
            '''

# query for weird historical event with a weird duration
weird_historical_event_query = '''
            SELECT DISTINCT ?novelist ?novelistLabel ?sitelinks ?country ?countryLabel ?pointtime ?duration WHERE
            {
            hint:Query hint:optimizer "None".
            VALUES ?country {''' + item + '''
            }
            {?novelist wdt:P276 [ wdt:P17 ?country]}
            UNION 
            {?novelist wdt:P17 ?country}
            UNION
            {?novelist wdt:P276 ?country}
            
            ?novelist wikibase:sitelinks ?sitelinks.
            filter(?sitelinks>0)
            
            {?novelist wdt:P585 ?pointtime
            OPTIONAL {?novelist wdt:P580 ?s_time.
            ?novelist wdt:P582 ?e_time.
            BIND(?e_time - ?s_time AS ?duration)}
            }
            UNION
            {?novelist wdt:P580 ?s_time.
            ?novelist wdt:P582 ?e_time.
            BIND(?e_time - ?s_time AS ?duration)
            }
            
            MINUS {?novelist wdt:P31/wdt:P279* wd:Q27020041}
            MINUS {?novelist wdt:P31 wd:Q82414}
            MINUS {?novelist wdt:P31 wd:Q159821}
            filter(YEAR(?pointtime)<2001 && YEAR(?pointtime)>1949 || (YEAR(?s_time)<2001 && YEAR(?s_time)>1949))
            filter(?duration<3 || !BOUND(?duration))
            SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
            }
            ORDER BY DESC(?sitelinks)
            LIMIT 100
            
            
            
            '''

# query for cities with at most 1 million inhabitants
city_query_with_bound_population = '''
            
            SELECT DISTINCT ?pageid ?novelist ?novelistLabel ?countryLabel ?sitelinks ?dateofbirth WHERE {
            SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
            VALUES ?country {''' + item + '''}
            
            ?novelist wdt:P17 ?country.
            ?novelist wikibase:sitelinks ?sitelinks.
            filter(?sitelinks>0)
            wd:Q702492 ^wdt:P279*/^wdt:P31 ?novelist.
            ?novelist wdt:P1082 ?population.
            filter(?population<1000000)
            
            
            }
            ORDER BY DESC(?sitelinks)
            LIMIT 100
            
            '''

# TODO interpret the query
# query='''
# SELECT DISTINCT ?pageid ?novelist ?novelistLabel ?countryLabel ?sitelinks ?dateofbirth WHERE {

# SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
# hint:Query hint:optimizer "None".

# VALUES ?country {'''+ item + '''}

# {?novelist wdt:P27 ?country.
#             ?novelist wdt:P569 ?dateofbirth.
# BIND(YEAR(?dateofbirth) AS ?sitelinks)
#             filter(?sitelinks<1800)}
# UNION
# {?novelist wdt:P19 [wdt:P17 ?country].
#             ?novelist wdt:P569 ?dateofbirth.
# BIND(YEAR(?dateofbirth) AS ?sitelinks)
# filter(?sitelinks<2000)}

# }
# ORDER BY ASC(?dateofbirth)
# LIMIT 20
# '''
