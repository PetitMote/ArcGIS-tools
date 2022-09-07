import arcpy
import pandas as pd
import numpy as np

# Lis les valeurs de paramètres
arcpy.AddMessage("Lecture des paramètres")
source = arcpy.GetParameterAsText(0)
champ_mediane = arcpy.GetParameterAsText(1)
champ_poids = arcpy.GetParameterAsText(2)
champ_aggregation = arcpy.GetParameterAsText(3)
table_sortie = arcpy.GetParameterAsText(4)


def mediane_ponderee(dataframe: pd.DataFrame) -> float:
    # Calcul d’une médiane pondérée. Vient de : https://stackoverflow.com/a/35349142
    arcpy.AddMessage("Début du calcul d’une médiane")
    dataframe.sort_values("valeur", inplace=True)
    cumsum = dataframe.poids.cumsum()
    cutoff = dataframe.poids.sum() / 2.0
    mediane = dataframe.valeur[cumsum >= cutoff].iloc[0]
    arcpy.AddMessage("Fin du calcul")
    return mediane


# Lis les valeurs de champs
arcpy.AddMessage("Lecture de la table de données")
table = [row for row in arcpy.da.SearchCursor(source, (champ_aggregation, champ_mediane, champ_poids))]
print(table[0])
# Convertit la table en dataframe de pandas
arcpy.AddMessage("Conversion de la table")
dataframe = pd.DataFrame.from_records(table, columns=["aggregation", "valeur", "poids"])

# Groupe les données par le champ d’aggrégation
dataframe_groupe = dataframe.groupby("aggregation", as_index=False)
# Crée une liste de tuples avec le champ d’aggrégation et la médiane pondérée
medianes = [(nom, mediane_ponderee(groupe)) for nom, groupe in dataframe_groupe]

# Construit un dataframe pour la conversion dans une table arcgis
# Cela peut être simplifié par la conversion directement dans un array Numpy, mais je trouvais plus simple comme ça
arcpy.AddMessage("Conversion des résultats")
data_sortie = pd.DataFrame.from_records(medianes, columns=[champ_aggregation, f"med_{champ_mediane}"])
data_sortie = data_sortie.to_records(index=False, column_dtypes={
    champ_aggregation: f"<S{data_sortie[champ_aggregation].str.len().max()}"})
# Il est nécessaire de passer un dtype sur le champ d’aggrégation. S’il s’agit d’un champ texte, il le crée de base en
# dtype object, ce qui fait planter l’import. La formule sert à définir la taille du champ texet.

# Import des résultats dans la table de destination
arcpy.AddMessage("Écriture des résultats")
arcpy.da.NumPyArrayToTable(data_sortie, table_sortie)
