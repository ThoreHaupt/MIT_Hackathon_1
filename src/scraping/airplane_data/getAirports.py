import pandas as pd

def getAirportsAsDict():
    df = pd.read_csv('/media/nils/Nils_Data/MIT-Hackathon/GlobalAirportDatabase/GlobalAirportDatabase.txt', sep=':', header=None)
    df = df[df.columns[[1, 14, 15]]]
    df = df[(df[df.columns[1]]!=0.0) | (df[df.columns[1]]!=0.0)]
    return dict(zip(df[df.columns[0]], zip(df[df.columns[1]], df[df.columns[2]])))

