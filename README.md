# canciondelveranopredictor
Esta aplicación Python/Flask se inspira en este [trabajo](https://github.com/xuwenyihust/Wine-Quality). Con metodología similar utilizamos sklearn y RandomForestClassifier para estimar si una canción será éxito del verano. La lista de canciones para el training se ha extraido del histórico semanal de canciones que han sido canción número uno durante al menos una semana. Solo aquellas que han estado más 4 semanas en el top, que son vistas comunmente como canción del verano, o que llegaron al top de ventas de canciones de PROMUSICAE se incluyen en el label 1, éxito del verano.
Las features de todo este dataset se extraen de la API de Spotify. Las features extraídas son (loudnes,danceability,valence, tempo, energy,liveness,key, accoustic)
[Información sobre definición.](https://beta.developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/)

## Metodología
Todas las variable son continuous, excepto key, que es categorical. 
El dataset utilizado para entrenar es musicot1.csv. En esa tabla están todas las features de todas la canciones que llegaron al top semanal de los 40 principales entre 2000 y 2017. No tenemos en cuenta años previos porque la tipología musical cambia demasiado y desvirtúa la estimación. El test dataset se extrae cuando el usuario busca una canción en la app. Se graba como test2.csv
Para evitar las variaciones en los resultados con RandomForest realizamos 50 predicciones RandomForest y hacemos la media de todas ellas.
TODO.
La estimación tiene algo de overfitting. 
Hemos estimado que toda canción que supere el 33 por ciento es muy probable que sea canción del verano.
