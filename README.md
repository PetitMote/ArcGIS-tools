# ArcGIS-tools

Collection de scripts pour les outils ArcGIS, développés pendant mes besoins.

## ArcGIS Pro

- [Toolbox paysages alimentaires](arcgis-pro/paysages-alimentaires)
  - En récupérant les deux dossiers, il est possible d’ouvrir la toolbox dans ArcGIS Pro directement et de lancer les scripts Python comme des outils natifs
  - [Médiane pondérée](arcgis-pro/paysages-alimentaires/Python/mediane_ponderee.py)
    - Utilise l’environnement natif d’ArcGIS Pro (pas besoin de créer un nouvel environnement ou d’installer des paquets python)
  - [Comptage du nombre d’intersections d’une couche de polygones dans d’autres polygones, avec agrégation en médiane pondérée](arcgis-pro/paysages-alimentaires/Python/mediane_nb_isochrones.py)
    - Script d’automatisation de certaines tâches
    - Utilise les géotraitements ArcGIS natifs + le script médiane pondérée au-dessus
