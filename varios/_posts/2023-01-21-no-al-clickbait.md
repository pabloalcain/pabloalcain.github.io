---
title: "No al clickbait: un botcito con GPT3"
category: varios
---


Terminó el 2022, comenzó el 2023 y con él se refrescan los hypes: dejamos pasar el hype de crypto (por un ratito,
seguramente en un tiempo vuelva) que tuvo pico en el 2021 y bienvenimos al hype de la inteligencia artificial gracias,
entre otros, a los desarrollos de openAI. Esta vez el hype de la inteligencia artificial viene con el sabor del 
lenguaje natural (otros años fue con imágenes) y con la capacidad generativa de texto a través de los LLM (Large 
Language Models). Las experiencias con plataformas como [chatGPT3](https://chat.openai.com/chat) son realmente
impresionantes, a pesar de que (como pasa siempre) no van a poder vivir a la altura del hype que se generó.

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">The current climate in AI has so many parallels to 2021 web3 it&#39;s making me uncomfortable. Narratives based on zero data are accepted as self-evident. Everyone is expecting as a sure thing &quot;civilization-altering&quot; impact (&amp; 100x returns on investment) in the next 2-3 years</p>&mdash; François Chollet (@fchollet) <a href="https://twitter.com/fchollet/status/1612142423425138688?ref_src=twsrc%5Etfw">January 8, 2023</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

Hay una moda que no cambia desde que la internet se volvió un espacio de publicidad y métricas de *engagement*: el
clickbait. Poner un titular que diga algo sospechoso, que hasta te enoja, pero entrás a la nota y... no dice lo que el
titular sugiere. ¡Ahí está el truco! Mentira no es (necesariamente), es *técnicamente* cierto y, en la realidad
concreta, una práctica bastante miserable. Hace unas semanas, por ejemplo, me pasó con este titular:

<figure>
  <img
  src="{{site.url}}/assets/posts/no-al-clickbait/infobae_clickbait.png"
  alt="Titular de Infobae: Se vuelven a encarecer los vuelos: desde el lunes rige un nuevo impuesto para pasajes aéreos"/>
  <figcaption>Clickbait de Infobae</figcaption>
</figure>


"Se vuelven a encarecer los vuelos", parece que va a ser algo gravísimo. Cuando leés el cuerpo de la nota, la tasa es
de entre 200 y 500 pesos (menos de dos dólares). Nuevamente: técnicamente es correcto, pero todos sabemos que es
mentira, que el titular insinúa algo tan exagerado que es incluso falso. En las redes sociales también pasa un montón.
El objetivo es conseguir dirigir tráfico hacia el sitio. Otra estrategia para dirigir el tráfico al sitio es, por
ejemplo, este tuit de ámbito:

<blockquote class="twitter-tweet"><p lang="es" dir="ltr">🎞ARGENTINA, 1985 VA POR MÁS: CUÁNDO Y POR DÓNDE VER LOS CRITICS&#39; CHOICE AWARDS<br><br>👉 Este domingo se entregan los premios elegidos por la crítica de Estados Unidos. Tras los Globos de Oro, la película argentina buscará repetir la hazaña.<br><br>📲 Leé más: <a href="https://t.co/AyqbbMjBY2">https://t.co/AyqbbMjBY2</a> <a href="https://t.co/nPirJLx83k">pic.twitter.com/nPirJLx83k</a></p>&mdash; Ámbito Financiero (@Ambitocom) <a href="https://twitter.com/Ambitocom/status/1614631302191251459?ref_src=twsrc%5Etfw">January 15, 2023</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

El tuit plantea una pregunta que se responde en la nota, pero que no hace falta. El tuit podría ser:
ARGENTINA, 1985 VA POR MÁS: ESTE DOMINGO A LAS 21 HS POR TNT PODÉS VER LOS CRITICS' CHOICE AWARDS. No les conviene
hacerlo de esa manera porque pierden visitas. Pero claro, encima tienen que escribir toda una nota para justificarlo,
de manera que la información está escondida en un montón de relleno bastante inútil. Ahí hay un uso posible de los
modelos generativos: podríamos pedirle a GPT-3 que invente una nota de relleno "alrededor" de la información importante,
el día y horario de la transmisión. La consecuencia es una peor calidad periodística, lectores menos informados y,
encima, los editores pueden elegir títulos que sugieran cosas inexistentes. Es un juego que no se puede ganar, todos
los incentivos van para generar más tráfico, que es más ingresos por publicidad, más "prestigio" en alguna métrica.
Nosotres, les pobres lectores, tenemos que caer sí o sí en ese juego para informarnos.

## Enter GPT-3

Pero si podemos usar GPT-3 para generar el "relleno", también podemos usarlo para sacárnoslo de encima. Resumir las
notas, tratar de extraer la información más relevante que entre en un tuit y disponibilizarla. Usar a la máquina para
deshacer los esfuerzos de estos medios de ocultarnos la información. Eso es, esencialmente,
[Te ahorro tu click](https://twitter.com/teahorrotuclick), un bot (aún en desarrollo[^1]) que sigue a cuentas de "noticias",
lee la nota asociada y responde los tuits con un resumen. No creo en la infalibilidad de GPT-3 (ni de cualquier
modelo posterior), a pesar de que hasta ahora sus resultados me sorprendieron y casi siempre los resúmenes fueron
fieles. Pero sí creo que este tipo de desarrollos puede ayudar a generar aunque sea algún incentivo para disminuir los
clickbaits. No va a ser este el bot que acabe con ellos, pero fue **muy** sencillo de hacer. Lo que más tiempo tomó fue
que twitter me aceptara la solicitud de los permisos para automatizarlo.

El resumen que da a la nota original de infobae es:

> Desde el lunes 9 de enero se aplicará un nuevo impuesto a los pasajes aéreos en todos los aeropuertos del SNA.
> La Tasa de Seguridad de la Aviación tendrá un costo base de $260 para vuelos domésticos y de USD 1,40 para vuelos
> internacionales y regionales. La tasa de uso aeroportuario también subirá a partir del 2 de febrero.

El resumen de la de ámbito es:

> Tras el triunfo en los Globos de Oro, la película argentina "Argentina, 1985" busca repetir la hazaña este domingo
> en los Critics' Choice Awards. Se emitirá en TNT y HBO Max desde las 21hs con comentarios de Ileana Rodríguez
> y Rafael Sarmiento.'

Un par de problemas: el primero es que le cuesta mantener un límite de caracteres. A pesar de que el requisito es que
el resumen tenga un máximo de 200 caracteres, el primer resumen tiene 325 y el segundo 244. Por ahora el bot corta
el mensaje hasta 280 caracteres para garantizarse que entre en un tuit. El otro problema es que le cuesta reconocer
qué es un clickbait y qué no (a nosotros los humanos nos cuesta ponernos de acuerdo incluso). La decisión por ahora
es resumir todas las notas (incluso las que no son clickbaits) y agregar una pequeña encuesta después de la respuesta
para ver si, en general, los usuarios consideran el tuit original como un clickbait. La respuesta al tuit de ámbito se
ve así:

<figure>
  <img
  src="{{site.url}}/assets/posts/no-al-clickbait/respuesta_ambito.png"
  alt="Dos tuits de Te Ahorro Un Click. Primer tuit: Tras el triunfo en los Globos de Oro, la película argentina Argentina, 1985 busca repetir la hazaña este domingo en los Critics' Choice Awards. Se emitirá en TNT y HBO Max desde las 21hs con comentarios de Ileana Rodríguez y Rafael Sarmiento. Segundo tuit: una encuesta por Sí o No preguntando si el tuit original es clickbait"
/>
  <figcaption>Clickbait de Ámbito</figcaption>
</figure>

Por ahora responde automáticamente a las cuentas de [Ambito](https://twitter.com/ambitocom) y
[Minuto Uno](https://twitter.com/minutounocom). Para [Infobae](https://twitter.com/infobae) hay que etiquetar al bot
en las replies para que la resuma. No se puede hacer automáticamente porque tuitean mucho **mucho** y termina siendo
muy costoso. Si bien es relativamente fácil agregar más fuentes, también es cierto que los medios pueden usar algunas
estrategias para complicar la solución de este lado o incluso encarecerla. En general, el bot es más una prueba de
concepto que un anti clickbait a prueba de balas.

Ojo, no es esto un canto a la tecnología. Fueron los propios desarrollos tecnológicos los que generaron los incentivos
para esta situación actual, de clickbait insoportable. Pero a veces hay alguna manera de usar algunas herramientas de la
tecnología para reclamar el control que otras herramientas nos quitan. Incluso quizás resulta que esta herramienta
en concreto no es tan buena como parece, que puede terminar siendo más perjudicial que beneficiosa. Porque no es la
tecnología la que va a resolver los problemas, sino los incentivos que queremos construir y, en gran medida, los usos
que les demos.

[^1]: Que no me comprometo a mantener, quizás se rompa, yo qué sé, es un jueguito. Sin compromiso.