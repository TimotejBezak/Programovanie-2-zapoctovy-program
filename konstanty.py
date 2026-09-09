SIRKA_OBRAZOVKY, VYSKA_OBRAZOVKY = 1800,900
FARBA_POZADIA = (30, 30, 30)
FARBA_POZADIA_SUFLIKA = (100, 100, 100)
MAX_VZDIALENOST_NA_ZAPASOVANIE = 20 # ak su dieliky blizsie ako toto, tak zapasuju
DIELIK_ANCHOR_POSITION = 20 # ze kazdy obrazok mam posunut o tolkoto pixelov dolava a hore, aby bol spravne
POCET_RIADKOV_SUFLIKA = 2
MEDZERY_DIELIKOV_V_SUFLIKU = 40 #pixelov
VYSKA_ZACIATKU_SUFLIKU = 700 # v akej vyske od laveho horneho rohu zacina suflik
RYCHLOST_POSUVANIA_SUFLIKU = 70 # ako rychlo sa pri kruteni kolieckom myse bude posuvat suflik
RYCHLOST_ZOOMOVANIA = 1/10 # ako rychlo sa pri kruteni kolieckom myse bude zoomovat na skladaciu plochu

POCET_DIELIKOV_NA_SIRKU_OBRAZKA = 4 # bude to stvorcovy obrazok, tolko isto aj na vysku teda
SIRKA_STRANY_DIELIKU_PRE_OBRAZOK = 250 # maximalna velkost obrazku pre skladanie, pri vyrazne vecsich sirkach dielikov, uz dielik moze vyzerat rozpixelovane kvoli zlemu skalovaniu
SIRKA_STRANY_DIELIKU_NAOZAJ = 50 # velkost obrazku dieliku ak zoomovanie je nulove
OBRAZOK_SCALE_OFFSET = SIRKA_STRANY_DIELIKU_NAOZAJ / SIRKA_STRANY_DIELIKU_PRE_OBRAZOK # o kolko musim kazdy obrazok este preskalovat, aby mal spravnu velkost
DIELIK_ANCHOR_POSITION_OBRAZOK = int(DIELIK_ANCHOR_POSITION / OBRAZOK_SCALE_OFFSET)