---
title: "Índice de Confianza en el Gobierno - Cómo no comunicar en estadística"
category: varios
---

El mes pasado el gobierno festejó que el Índice de Confianza al Gobierno había subido 6.4% comparado con el mes anterior.
Este mes probablemente se lamentará de que el mismo índice bajó 5.9%.
Lo más probable es que ni el mes pasado subiera ni este bajara, sino que sean todas fluctuaciones estadísticas sobre una tendencia a la baja sostenida desde principios de año.



## ¿Qué mide y qué comunica el ICG?

Un colega me decía regularmente, a modo de broma, "no vamos a permitir que nos confundan con estadísticas".
Después de trabajar un tiempo haciendo estadística de una forma u otra, siempre es simpático encontrar estadísticas que confunden.
Una que me llama mucho la antención hace tiempo es la encuesta del Índice de Confianza en el Gobierno, encargado por la Universidad Torcuato di Tella y llevada adelante por Poliarquía.
El Índice de Confianza de Gobierno es un número del 0 al 5 que mide (de alguna manera) hace muchos años cuánto confía la gente en el gobierno.
El mes pasado la noticia era que este índice había subido brutalmente, de 1.94 a 2.06 puntos.
El gobierno festejando.
Este mes (hoy) la noticia es que el índice bajó brutalmente, de 2.06 a 1.94 puntos.
El gobierno probablemente no vaya a festejar tanto.

Todo esto es ruido.
No digo sólo ruido en los medios, sino literalmente ruido estadístico.
Me explico: en los comunicados de prensa de la UTDT (por ejemplo, éste de [Septiembre 2026](https://www.utdt.edu/download.php?fname=_179060603218536000.pdf)) al final abajo da algunos detalles metodológicos, donde podemos ver el intervalo de confianza del índice.
En este caso, dice que el rango de valores está entre 1.81 y 2.06.

<figure>
  <img
  src="{{site.url}}/assets/posts/indice-confianza-gobierno/ficha_tecnica.png"
  alt="Ficha técnica del Índice de Confianza en el Gobierno de Septiembre de 2026, con el rango de valores del ICG entre 1.81 y 2.06."/>
  <figcaption>Ficha técnica del Índice de Confianza en el Gobierno de Septiembre de 2026, con el rango de valores del ICG entre 1.81 y 2.06.</figcaption>
</figure>

¿Qué quiere decir el intervalo de confianza?
Lo podemos pensar como las divisiones de una regla[^1].
En una regla normal podemos ver hasta 1mm de diferencia; sería un poco tramposo decir que con una regla podemos decir que una mesa es medio milímetro más corta que la otra.
Del mismo modo, es tramposo decir que podemos distinguir una diferencia de 0.12 puntos si el índice tiene un rango de 0.25 puntos.

Cuando consideramos este error muestral la foto cambia bastante[^2].
Ésta es la serie temporal agregando las bandas de error.

<figure>
  <img
  src="{{site.url}}/assets/posts/indice-confianza-gobierno/serie_error.png"
  alt="Serie temporal del ICG con bandas de error desde 2023 hasta la fecha. Las variaciones de los últimos meses están dentro del ruido estadístico."/>
  <figcaption>Serie temporal del ICG con bandas de error desde 2023 hasta la fecha. Las variaciones de los últimos meses están dentro del ruido estadístico.</figcaption>
</figure>

Claramente se puede ver que las variaciones de los últimos meses fueron puro ruido.
Un fenónemo similar sucedió por ejemplo cerca de abril de 2025, 5 meses de ruido donde probablemente el ICG no cambió sensiblemente: simplemente dio valores distintos al medirlo en la encuesta.

## Entonces, ¿qué sí se puede ver?

Algunas cosas se pueden ver del gráfico, por ejemplo:

- El salto en el cambio de gobierno (bueno, no hacía falta una encuesta para ver esto: asumió el gobierno que ganó las elecciones)
- Una tendencia a la baja hasta Octubre de 2024, cuando subió notablemente.
- A partir de ahí tiene otra tendencia decreciente, con un descenso justo antes de las elecciones de medio término.
- Recuperó los valores anteriores al ganar las elecciones nacionales de medio término.
- Una tendencia a la baja con un claro bajo en Abril 2026
- A partir de ahí una muy leve tendencia a la baja que se sostiene hasta ahora.

<figure>
  <img
  src="{{site.url}}/assets/posts/indice-confianza-gobierno/serie_error_tendencias.png"
  alt="Serie temporal del ICG con bandas de error desde 2023 hasta la fecha, mostrando algunas tendencias y saltos discernibles en el ruido estadístico."/>
  <figcaption>Serie temporal del ICG con bandas de error desde 2023 hasta la fecha, mostrando algunas tendencias y saltos discernibles en el ruido estadístico.</figcaption>
</figure>


Esto es todo lo que dicen los datos, el resto es ruido.
El ICG viene bajando desde principios de año, ahora un poquito más lento que antes.
Ni el mes pasado subió 6.4% ni éste bajó 5.9%.

## El problema no es la estadística, sino la comunicación.

No tengo motivos para dudar de que las cuentas estén bien hechas, que efectivamente éste sea el intervalo del índice y eso.
Para ser justos, incluso, el final del documento dice que "[desde mayo se observan] oscilaciones mensuales de magnitud modesta y sin una tendencia clara".
El problema es cómo se elige comunicar.

<figure>
  <img
  src="{{site.url}}/assets/posts/indice-confianza-gobierno/banner.png"
  alt="Comunicación principal de la UTDT sobre la encuesta del ICG, haciendo foco en una diferencia que es puramente aleatoria."/>
  <figcaption>Comunicación principal de la UTDT sobre la encuesta del ICG, haciendo foco en una diferencia que es puramente aleatoria.</figcaption>
</figure>

Aquí la UTDT elige comunicar un número que, más que probablemente, sea fluctuación estadística.
Aunque entiendo que uno no puede escribir un texto de nosécuántos caracteres para hacer "una salvedad" cada vez que comunica algo, este tipo de comunicación termina siendo contraproducente para la misma UTDT.
Por ejemplo, el [mes pasado](https://www.utdt.edu/download.php?fname=_178759164784605000.pdf) tuvo que aclarar que "[los] altibajos podrían deberse al error muestral más que a cambios reales en los parámetros de interés", una aclaración correcta y necesaria porque nadie esperaba ver que el indicador subiera.

Seguir comunicando variaciones mensuales del 5% como si tuvieran algún tipo de significado más allá del ruido es, a mi parecer, una comunicación muy engañosa.
No me voy a poner a especular por qué.

### Apéndice: Algunos comentarios metodológicos

- Habría que ver cuán correlacionados están los intervalos de confianza mes a mes, para poder hacer la comparación estadística más precisamente. Por la descripción, parece que están descorrelacionados y cada vez es un muestreo estadístico nuevo.
- Ni me quiero imaginar el intervalo de confianza que hay cuando esto es medido separando por género. Debe ser muy difícil sacar conclusiones mes a mes de ahí.
- Éste análisis es muy crudo, lo hice rápido cuando volví del trabajo. Así que espero que perdonen cualquier desliz y lo entiendan simplemente como una reflexión sobre la comunicación y una crítica constructiva.


[^1]: A riesgo de robarles frases a otras disciplinas, *es más complejo*. Espero que esta explicación sea óptima para los pocos caracteres que lleva.
[^2]: Me tomé la libertad de darle a todos los días el mismo rango que el último mes, porque implicaría revisar todos los reportes uno por uno si no. Por los que chusmeé, parece que la diferencia es muy menor.
