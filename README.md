## Как запустить проект?
1. Установить и запустить докер
2. Клонировать репозиторий к себе на компьютер, перейти в него и открыть терминал
3. вводим команду ```docker-compose build```
4. вводим команду ```docker-compose up```
5. Далее переходим в бразуер по http://localhost:5000/crawl

## Документация
Документация проекта доступна по http://localhost:5000/apidocs после выполнения предыдущих шагов

## Демонстрация
[Нажмите для перехода к демонстрации работы проекта](https://drive.google.com/drive/folders/1Be0uX9hxx26hExc662ZiCB9fqPDMHbRv?usp=sharing)

## Презентация
[Нажмите для перехода к презентации](https://docs.google.com/presentation/d/1rWlbE59T9rf51uZCyttu-_zSQqED27bm/edit?slide=id.p1#slide=id.p1)

## Пример для запуска с кастомными селекторами:
curl -X POST http://127.0.0.1:5000/crawl -H "Content-Type: application/json" -d '{"start_url":"https://skillfactory.ru", "max_depth":5, "header_selectors":[ "header", "div[class*=\"header\"]", "div[id*=\"header\"]", "div[class*=\"top\"]", "div[id*=\"top\"]", "div[class*=\"menu\"]", "div[id*=\"men
u\"]", "nav[class*=\"nav\"]", "nav[id*=\"nav\"]" ], "footer_selectors":[ "footer", "div[class*=\"footer\"]", "div[id*=\"footer\"]", "div[class*=\"bottom\"]", "div[class*=\"contacts\"]", "div[id*=\"contacts\"]" ]}'

## Пример для запуска с кастомными селекторами + пресеты селекторов в зависимости от CMS. Например, с bitrix:
curl -X POST http://127.0.0.1:5000/crawl -H "Content-Type: application/json" -d '{"start_url":"https://skillfactory.ru", "max_depth":5, "type": "bitrix", "header_selectors":[ "header", "div[class*=\"header\"]", "div[id*=\"header\"]", "div[class*=\"top\"]", "div[id*=\"top\"]", "div[class*=\"menu\"]", "div[id*=\"men
u\"]", "nav[class*=\"nav\"]", "nav[id*=\"nav\"]" ], "footer_selectors":[ "footer", "div[class*=\"footer\"]", "div[id*=\"footer\"]", "div[class*=\"bottom\"]", "div[class*=\"contacts\"]", "div[id*=\"contacts\"]" ]}'

Ответ:
{
   "pages":[
      {
         "url":"https://skillfactory.ru/frontend-razrabotchik-pro/?utm_source=blog&utm_medium=glossary&utm_campaign=none_coding_frpro_blog_glossary_course_none_none_all_sf_css_bigbanner&utm_content=css&utm_term=bigbanner",
         "header_found":true,
         "footer_found":true,
         "title":"Курс «Frontend-Разработчик с нуля до PRO»: обучение frontend-разработке онлайн",
         "meta_description":"Онлайн-курс «Frontend-Разработчик с нуля до PRO» с сертификатом и помощью в трудоустройстве ✔️Получите знания и опыт уровня middle в фронтенд-разработке. Обучение основам JavaScript, TypeScript и React в связке с Next.js. Станьте профессионалом в IT.",
         "is_media":false,
         "image_urls":[
            "https://mc.yandex.ru/watch/38813825",
            "https://vk.com/rtrg?p=VK-RTRG-506420-4wpVF",
            "https://thb.tildacdn.com/tild3231-3937-4465-a634-356462616332/-/empty/1.jpeg",
            "https://thb.tildacdn.com/tild3938-6164-4865-a461-303738336632/-/empty/Frame_20_1.png",
            "https://thb.tildacdn.com/tild3438-3138-4239-b038-633066326439/-/empty/Frame_22_1.png",
            "https://thb.tildacdn.com/tild3132-6438-4535-b564-643837343939/-/empty/Frame_21_2.png",
            "https://thb.tildacdn.com/tild3266-3066-4731-b333-623339333364/-/empty/Frame_23_1.png",
            "https://static.tildacdn.com/tild6339-3164-4232-a235-303231353866/Frame_82_1.svg",
            "https://static.tildacdn.com/tild6339-3164-4232-a235-303231353866/Frame_82_1.svg",
            "https://static.tildacdn.com/tild6339-3164-4232-a235-303231353866/Frame_82_1.svg",
            "https://static.tildacdn.com/tild6663-3366-4231-b666-343634633136/Frame_82_1.svg",
            "https://static.tildacdn.com/tild6339-3164-4232-a235-303231353866/Frame_82_1.svg",
            "https://static.tildacdn.com/tild6663-3366-4231-b666-343634633136/Frame_82_1.svg",
            "https://static.tildacdn.com/tild6663-3366-4231-b666-343634633136/Frame_82_1.svg",
            "https://static.tildacdn.com/tild6339-3164-4232-a235-303231353866/Frame_82_1.svg",
            "https://static.tildacdn.com/tild6130-6235-4664-b539-613333633335/Frame_82_1.
         ],
         "published_date":null,
         "links":[
            "https://skillfactory.ru/frontend-razrabotchik",
            "https://skillfactory.ru/frontend-razrabotchik-pro/?utm_source=blog&utm_medium=glossary&utm_campaign=none_coding_frpro_blog_glossary_course_none_none_all_sf_css_bigbanner&utm_content=css&utm_term=bigbanner",
            "https://skillfactory.ru/",
            "https://skillfactory.ru/free-events",
            "https://skillfactory.ru/career-center",
            "https://skillfactory.ru/contacts",
            "https://blog.skillfactory.ru/",
            "https://new.skillfactory.ru/corporativnoye-obuchenye",
            "https://skillfactory.ru/courses",
            "https://skillfactory.ru/courses/data-science",
            "https://skillfactory.ru/courses/analitika-dannyh",
            "https://skillfactory.ru/courses/programmirovanie",
            "https://skillfactory.ru/courses/intensive",
            "https://skillfactory.ru/courses/web-razrabotka",
            "https://skillfactory.ru/courses/backend-razrabotka",
            "https://skillfactory.ru/courses/testirovanie",
            "https://skillfactory.ru/courses/razrabotka-mobilnyh-prilozheniy",
            "https://skillfactory.ru/courses/kiberbezopasnost",
            "https://skillfactory.ru/courses/network-infrastructure",
            "https://skillfactory.ru/courses/razrabotka-igr",
            "https://skillfactory.ru/courses/marketing",
            "https://skillfactory.ru/courses/design",
            "https://skillfactory.ru/courses/management-i-upravlenie",
            "https://new.skillfactory.ru/vyssheye-obrazovaniye",
            "https://skillfactory.ru/courses/sozdanie-saytov",
            "https://skillfactory.ru/frontend-razrabotchik-pro/\\\"https:\\/\\/skillfactory.ru\\/position_of_user_personal_data\\\"",
            "https://skillfactory.ru/job-guarantee",
            "https://skillfactory.ru/position_of_user_personal_data",
            "https://blog.skillfactory.ru/pravda-li-chto-ajtishnikam-polozhena-otsrochka/",
            "https://skillfactory.ru/qa-engineer-python-testirovshchik-programmnogo-obespecheniya-b",
            "https://blog.skillfactory.ru/lichnyj-opyt/",
            "https://blog.skillfactory.ru/ya-sam-nauchilsya-programmirovat-i-stal-timlidom/",
            "https://blog.skillfactory.ru/diana-gromova-ya-obozhala-himiyu-no-razocharovalas-v-nauke-i-stala-frontend-razrabotchikom/",
            "https://blog.skillfactory.ru/ya-sluzhil-v-policzii-a-teper-razrabatyvayu-obrazovatelnye-servisy/",
         ]
      },
      {"etc": "..."}
   ]
}


