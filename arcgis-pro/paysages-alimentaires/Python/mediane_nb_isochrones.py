import arcpy
from arcpy.analysis import SpatialJoin
from arcpy.management import AddJoin

# Lecture des paramètres
zones_pop = arcpy.GetParameterAsText(0)
champ_pop = arcpy.GetParameterAsText(1)
champ_aggreg = arcpy.GetParameterAsText(2)
isochrones = arcpy.GetParameterAsText(3)
zones_aggreg = arcpy.GetParameterAsText(4)
champ_jointure = arcpy.GetParameterAsText(5)
sortie_medianes = arcpy.GetParameterAsText(6)
sortie_resumes = arcpy.GetParameterAsText(7)
sortie_zones_pop = arcpy.GetParameterAsText(8)

# Importe la toolbox locale, si son nom n’a pas changé
arcpy.ImportToolbox("toolbox.tbx", "toolbox")

# Création d’une couche temporaire
tmp_couche_sortie = arcpy.CreateScratchName(workspace=arcpy.env.scratchGDB)
# Jointure spatiale
SpatialJoin(target_features=zones_pop,
            join_features=isochrones,
            out_feature_class=tmp_couche_sortie,
            join_operation="JOIN_ONE_TO_ONE",
            join_type="KEEP_ALL",
            field_mapping="",
            match_option="INTERSECT",
            search_radius="",
            distance_field_name="",
            )

# Calcul des médianes
arcpy.MedianePonderee_toolbox(source=tmp_couche_sortie,
                              champ_mediane="Join_Count",
                              champ_poids=champ_pop,
                              champ_aggregation=champ_aggreg,
                              table_sortie=sortie_medianes,
                              )

# Jointure
join = AddJoin(
    in_layer_or_view=zones_aggreg,
    in_field=champ_jointure,
    join_table=sortie_medianes,
    join_field=champ_aggreg,
    join_type="KEEP_ALL",
    index_join_fields="NO_INDEX_JOIN_FIELDS",
)

# Copie de la jointure dans la couche de résultat
arcpy.CopyFeatures_management(join, sortie_resumes)

# Copie de la couche avec jointure spatiale si une sortie a été indiquée
if sortie_zones_pop:
    arcpy.CopyFeatures_management(tmp_couche_sortie, sortie_zones_pop)
