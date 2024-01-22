import pandas as pd

import additional_explanations

from Category import Category
from Country import preAllCountries
from helpFunctions import callcountrybyname
from globalDefinitions import reverse_countries_alternative_names


def setupdata(data,
              column,
              namecolumn,
              nameofattribute,
              ascending,
              treatmissingdataasbad=False,
              applyfrac=False,
              additional_information=False,
              additional_information_column=2):

    def append_dataframe(series, nameofattribute, numberofranked):
        additional_informations = []
        try:
            countryname = reverse_countries_alternative_names[
                series.iloc[0].lower()]
        except KeyError:
            return None
        except AttributeError:
            return None
        if not callcountrybyname(countryname) in preAllCountries:
            return None
        value = series.iloc[1]
        if additional_information:
            additional_informations = list()
            for item in additional_information_column:
                additional_informations.append(series.iloc[item])  # error
        mylist = list()
        mylist.append(value)
        mylist.append((series.loc["ranking"] + 1))
        mylist.append(numberofranked + 1)
        mylist += additional_informations
        callcountrybyname(
            countryname).dictofattributes[nameofattribute] = mylist
        pass

    if not treatmissingdataasbad:
        data = data[data["1"] != float(-1)]
    else:
        if not ascending:
            data["1"] = data["1"].apply(lambda x: float(0)
                                        if x == float(-1) else x)
        else:
            data["1"] = data["1"].apply(lambda x: float(9999999999)
                                        if x == float(-1) else x)
    data.sort_values(by=str(column), ascending=ascending, inplace=True)
    data = data.reset_index(drop=True)
    dList = data.iloc[:, 0].tolist()

    dataDict = {'0': [], '1': []}
    for index, item in enumerate(dList):
        try:
            dList[index] = reverse_countries_alternative_names[item]
        except KeyError:
            pass
    data.iloc[:, 0] = dList
    if treatmissingdataasbad:
        for countryclass in preAllCountries:
            if countryclass.name not in dList:
                if not ascending:
                    dataDict['0'].append(countryclass.name)
                    dataDict['1'].append(float(0))
                else:
                    dataDict['0'].append(countryclass.name)
                    dataDict['1'].append(float(9999999999))

    data = pd.DataFrame(dataDict)

    rankinglist = list(range(len(data.index)))

    data["ranking"] = rankinglist
    data.apply(lambda x: append_dataframe(
        x, nameofattribute=nameofattribute, numberofranked=len(rankinglist)),
               axis=1)


def better_setup_data(name,
                    column=1,
                    namecolumn=0,
                    ascending=False,
                    treatmissingdataasbad=False,
                    applyfrac=False,
                    dif=0,
                    additional_information=False,
                    additional_information_column=[2],
                    cluster=None,
                    is_end_only: bool = False):

    if "lower is better" in name:
        ascending = True
    data = pd.read_csv("data/" + name, index_col=None)
    setupdata(data,
              column,
              namecolumn,
              name,
              ascending=ascending,
              treatmissingdataasbad=treatmissingdataasbad,
              applyfrac=applyfrac,
              additional_information=additional_information,
              additional_information_column=additional_information_column)

    # get additional explanations, if it is provided
    try:
        explanation = additional_explanations.additional_explanations[name]
    except KeyError:
        explanation = ""

    # create Category with information provided
    Category(name,
             isActive=additional_information,
             treatMissingDataAsBad=treatmissingdataasbad,
             difficulty=dif,
             explanation=explanation,
             is_end_only=is_end_only)
