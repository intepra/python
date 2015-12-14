# Домашнее задание 3

Развитие социальной сети Zwitter сформировало перед основателями стартапа новые более сложные типы задач. 
Основатели построили социальный граф по пользователям своего стартапа, и теперь они хотят эффективно решать итеративные 
Map-Reduce задачи на построенном социальном графе. Основатели также хотели бы для ряда метрик иметь возможность узнавать 
актуальные значения в режиме реального времени.

## Что надо делать?

В третьем домашнем задании вам необходимо помочь основателями решить следующие задачи:
 
  * Настроить ежедневный расчет и сохранение метрик по социальному графу пользователей.
  * Настроить вычисление потоковой метрики по потоку событий из Apache Kafka.
  * Предоставить доступ к сохраненным и вычисленным по потоку событий данным через HTTP API.

Ниже вы можете найти более подробную информацию по следующим вопросам:

  * [Исходные данные](#Исходные-данные)
  * [Рассчитываемые метрики](#Рассчитываемые-метрики)
  * [Требования](#Требования)
  * [Критерии сдачи задания](#Критерии-сдачи-задания)
  * [Процесс сдачи задания](#Процесс-сдачи-задания)
  * [Спецификация HTTP API](#Спецификация-http-api)
  * [Дополнительные комментарии](#Дополнительные-комментарии)


## Исходные данные

В этом задании для вычисления метрик используется заранее построенный социальных граф, хранящийся по адресу
`hdfs://hadoop2.yandex.ru:8020/user/shtokhov/social_graph/social_graph.net`. Пример содержимого файла:

```
id00066	id14272
id00066	id14271
id00066	id14269
id00066	id14267
id00066	id14266
id00066	id14260
id00066	id14258
id00066	id14257
id00066	id14256
id00066	id14255
```

Каждая строка файла представляет собой ребро социального графа, вершины начала и окончания ребра разделены знаком табуляции.
Ребро социального графа формирует отношение "дружит с" для профилей социальной сети. Для каждой строки в социальном графе 
вначале идет вершина (профиль) "кто дружит", через знак табуляции идет вершина (профиль) "с кем дружит".
Для приведенного выше примера следует:
 
```
Профиль id00066 дружит с профилем id14272
Профиль id00066 дружит с профилем id14271
...
```

Для вычисление метрики по потоку данных из Apache Kafka используются те же исходные данные, что и в предыдущих заданиях:
логи доступа к веб-серверу.

Из каждой записи в логе можно выделить **пользователя** и **посещенный профиль**: пользователь определяется IP-адресом,
а посещенный профиль -- идентификатором, закодированном в URI запроса в виде `idNNNNN`.

К примеру, по записи

```
195.206.123.39 - - [24/Sep/2015:12:32:53 +0400] "GET /id18222 HTTP/1.1" 200 10703 "http://bing.com/" "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 Safari/537.36"
```

Можно сказать, что пользователь **195.206.123.39** посетил профиль **id18222** и посещение было 24 сентября 2015 года в 12:32:53 по времени GMT+4.

Как и в предыдущих заданиях, для расчета метрик вам стоит рассматривать только успешные (HTTP-код 200)
запросы к веб-сайту. Неуспешные запросы стоит игнорировать.

## Рассчитываемые метрики

По социальному графу для пары вершин необходимо рассчитать следующие метрики:

  * `minimal_path` -- путь минимальной длины и лексикографически первый, связывающий заданные две вершины в социальном графе.
  * `circles_intersection` -- пересечение второго круга профиля A и профиля B (заранее заданных).

Второй круг профиля определяется следующим образом:

  * назовем друзьями профиля X такое множество профилей p, которые связаны с X отношением "X дружит с p";
  * назовем первым кругом X -- множество друзей профиля X; вторым кругом X -- множество друзей друзей профиля X
(то есть такие профили q, что X дружит p, а p дружит с q).

По потоку событий из Kafka необходимо рассчитать следующие метрики:

  * `disconnected_users` -- количество отключившихся пользователей. 

Отключившиеся пользователи определяются по следующим правила:

 * разобъем временную ось на 20-минутные интервалы; каждый интервал будет отождествлять с моментом его начала (13:00, 13:20, 13:40, 14:00, 14:20 и т. д.);
   правая граница (13:20 в случае интервала 13:00-13:20) не включается в интервал;
 * множество активных пользователей в интервал I -- это множество пользователей, сгенерировавших хотя бы 1 хит к веб-серверу в интервале X;
 * множество отключившихся пользователей в интервал I -- это множество пользователей, которые были активны в интервале I-4, но не были активны в интервалах I-3, I-2 и I-1.

К примеру, если пользователь генерировал хиты в моменты времени 13:14, 13:20, 13:29, 13:39, то он является активным пользователем
в интервалах 13:00-13:20, 13:20-13:40; в интервалы времени 13:40-14:00, 14:00-14:20, 14:20-14:40 пользователь неактивен,
и в интервал 14:40-15:00 он считается отключившимся.

## Требования

Ваше решение должно удовлетворять следующим требованиям:

  * вычисленные данные должны быть готовы к 9 утра следующего дня (к примеру, результаты за 25.11 должны быть готовы к 09:00 26.11);
    готовность вычисленных данных определяется возможностью выполнения запросов через HTTP API;
  * время ответа HTTP API не должно превышать 5 секунд;
  * ваш процесс расчета должен стабильно работать начиная с момента сдачи задания и до окончания курса,
    при этом ваше решение _не должно_ терять просчитанные данные за прошедшие дни
    (в том числе и после удаления исходных данных из HDFS).

## Критерии сдачи задания

В данном задании 1 попугай выдается за одну реализованную метрику.

Реализованная метрика засчитывается, если:

  * до **7-го декабря** реализован HTTP API выдающий результат по данной метрике;
  * в период **с 7 декабря по 17 декабря** метрика корректно работает хотя бы три дня;

## Процесс сдачи задания

По адресу `http://hadoop2-00.yandex.ru:8888/sample/hw3?date=2015-11-25` доступен JSON с информацией о вершинах (профилях),
для которых необходимо произвести расчет для дня, указанного в параметрах запроса. Обратите внимание, что данные предоставляются
только за прошедшие дни (начиная с 25 ноября) и за текущий день.
 
Пример запроса:

```
GET http://hadoop2-00.yandex.ru:8888/sample/hw3?date=2015-11-25
```
 
Пример ответа:

```json
{
   "minimal_path": {"from": "id29759", "to": "id62558"},
   "circles_intersection": {"A": "id20479", "B":"id18689"}
}
```
 
## Спецификация HTTP API

Ваше решение должно уметь отвечать на множество запросов типа `GET` по URI `/api/hw3/XXX`,
соответствующие вычисляемым метрикам. Если вы умеете вычислять запрашиваемую метрику,
то ваше решение должно отвечать с HTTP-кодом 200; в качестве ответа должен быть JSON-документ
с указанной в описании запроса структурой. Если вы не умеете вычислять запрашиваемую метрику,
то ваше решение должно отвечать с HTTP-кодом 404.

### `/api/hw3/minimal_path`

Параметры запроса:
  * `start_date` -- начальная дата в формате `YYYY-MM-DD`,
  * `end_date` -- конечная дата в формате `YYYY-MM-DD`,

Формат ответа:
  * Ключами JSON-документа ответа являются временные метки в указанном временном диапазоне.
    Для данной метрики временная гранулярность дневная; метки имеют вид `YYYY-MM-DD`, например:
    `2015-10-01`, `2015-10-02` и т. д.
  * Значениями JSON-документа ответа являются массивы, кодирующие минимальный по длине путь для заданных двух профилей, 
    соответствующих дню в ключе документа (при нескольких путях минимальной длины необходимо выдавать лексикографически первый путь).
    Начальную и конечную вершины необходимо включить в ответ. Если пути не существует, необходимо вернуть пустой список.
    Каждая вершина (профиль) кодируется как `idNNNNN`.
  * Если у вас нету значения за какие-либо временные интервалы, то используйте `null` в качестве ответа.

Пример запроса:

```
GET /api/hw3/minimal_path?start_date=2015-10-01&end_date=2015-10-05
```

Пример ответа:

```json
{
  "2015-10-01": ["id10001", "id10002", "id10003"],
  "2015-10-02": ["id10003", "id10005"],
  "2015-10-03": [],
  "2015-10-04": ["id10001", "id10006"],
  "2015-10-05": null
}
```

### `/api/hw3/circles_intersection`

Параметры запроса:
  * `start_date` -- начальная дата в формате `YYYY-MM-DD`,
  * `end_date` -- конечная дата в формате `YYYY-MM-DD`,

Формат ответа:
  * Ключами JSON-документа ответа являются временные метки в указанном временном диапазоне.
    Для данной метрики временная гранулярность дневная; метки имеют вид `YYYY-MM-DD`, например:
    `2015-10-01`, `2015-10-02` и т. д.
  * Значениями JSON-документа ответа являются массивы, соотвествующие множеству профилей, являющихся одновременно друзьями 
    первого и второго заданных профилей. Если таковых нет, то ответом является пустой список.
    Каждый профиль кодируется как `idNNNNN`.
  * Если у вас нету значения за какие-либо временные интервалы, то используйте `null` в качестве ответа.

Пример запроса:

```
GET /api/hw3/circles_intersection?start_date=2015-10-01&end_date=2015-10-05
```

Пример ответа:

```json
{
  "2015-10-01": ["id10001", "id10002"],
  "2015-10-02": ["id10003"],
  "2015-10-03": ["id10001"],
  "2015-10-04": [],
  "2015-10-05": null
}
```

### `/api/hw3/disconnected_users`

Параметры запроса:
  * `start_date` -- начальная дата в формате `YYYY-MM-DD`,
  * `end_date` -- конечная дата в формате `YYYY-MM-DD`,

Формат ответа:
  * Ключами JSON-документа ответа являются временные метки в указанном временном диапазоне.
    Для данной метрики временная гранулярность получасовая; метки имеют вид `YYYY-MM-DDTHH:mm`, например:
    `2015-10-01T10:00`, `2015-10-01T10:30`, `2015-10-01T11:00` и т. д.
  * Значениями JSON-документа ответа являются числа, определяющие количество отключившихся пользователей в данный временной интервал.
  * Если у вас нету значения за какие-либо временные интервалы, то используйте `null`.

Пример запроса:

```
GET /api/hw3/disconnected_users?start_date=2015-10-01&end_date=2015-10-01
```

Пример ответа:

```json
{
  "2015-10-01T00:00": 1056,
  "2015-10-01T00:30": 1433,
  "2015-10-01T01:00": 945,
  "2015-10-01T01:30": 1234,
  "2015-10-01T02:00": 0,
  "2015-10-01T02:30": 0,
  "2015-10-01T03:00": 0,
  "2015-10-01T03:30": null,
  ...
  "2015-10-01T23:30": null
}
```

## Дополнительные комментарии

Возьмем в качестве примера социальный граф:

```
id00001	id00002
id00002	id00003
id00001	id00004
id00004	id00003
id00005	id00003
id00007	id00003
id00006	id00005
id00006	id00007
```

Запросим исходные условия к заданию:

```
GET http://hadoop2-00.yandex.ru:8888/sample/hw3?date=2015-11-11
```

```json
{
  "minimal_path": {"from": "id00001", "to": "id00003"},
  "circles_intersection": {"A": "id00001", "B": "id00006"}
}
```

Тогда правильный ответ для метрики `minimal_path` выглядит следующим образом:

```
GET /api/hw3/minimal_path?start_date=2015-11-11&end_date=2015-11-11
```

```json
{
  "2015-11-11": ["id10001", "id10002", "id10003"]
}
```

Для метрики `circles_intersection` правильный ответ выглядит следующим образом:

```
GET /api/hw3/circles_intersection?start_date=2015-11-11&end_date=2015-11-11
```

```json
{
  "2015-11-11": ["id00003"]
}
```