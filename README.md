# canciondelveranopredictor
Esta aplicación Python/Flask se inspira en este [trabajo](https://github.com/xuwenyihust/Wine-Quality). Con metodología similar utilizamos sklearn y RandomForestClassifier para estimar si una canción será éxito del verano. La lista de canciones para el training se ha extraido del histórico semanal de canciones que han sido canción número uno durante al menos una semana. Solo aquellas que han estado más 4 semanas en el top, que son vistas comunmente como canción del verano, o que llegaron al top de ventas de canciones de PROMUSICAE se incluyen en el label 1, éxito del verano.
Las features de todo este dataset se extraen de la API de Spotify. Las features extraídas son (loudnes,danceability,valence, tempo, energy,liveness,key, accoustic)
[Información sobre definición.](https://beta.developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/)

## Metodología
Todas las variable son continuous, excepto key, que es categorical. 