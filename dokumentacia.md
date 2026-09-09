Používateľský manuál:

Spúšťa sa to súborom main.py, treba mať nainštalovanú knižnicu pygame

V dolnej časti je zásoba dielikov zoradená do niekoľkých riadkov, v hornej časti je skladacia plocha. Z dolnej časti sa dajú dieliky dragovať do hornej, kde sa dajú tiež dragovať. Ťuknutím pravým tlačidlom myse na dielik sa dielik otočí o deveťdesiat stupňov. Ak sú dva pasujúce dieliky dostatočne blízko seba a správne otočené, tak sa spoja dokopy. Spojený kus sa dá tiež dragovať a spájať ďalej.

Ak je myš v priestore skladacej plochy, tak krútením koliečka myse dokážeme od/pri zoomovať skladaciu plochu, čím je možné získať detailnejší pohľad na vybranú časť dielikov. Podobne, držaním koliečka myse a posúvaním myse dokážeme skladaciu plochu posúvať, čo je tiež veľmi užitočné.

Ak je myš v priestore zásoby dielikov v dolnej časti, tak hýbaním koliečka myse dokážeme posúvať dieliky, pretože ich môže byť aj viac, ako sa naraz na obrazovku zmestí. Toto umožňuje možnosť mať k dispozícii všetky dieliky celého puzzle.

Dielik zo skladacej plochy sa dá vrátiť do zásoby dielikov jednoduchým dragnutím do oblasti zásoby dielikov. Tento dielik sa pridá úplne na koniec zásoby dielikov.

Dokumentácia:

Generovanie dielikov: (všetko toto sa deje v súbore *generator.py*)
- najprv rozsekám vstupný obrázok na príslušný počet štvorcových dielikov, pre každý dielik si zapametám, na akú pozíciu (riadok, stĺpec) vrámci obrázku patrí.
- potom dielikom vylepším hrany - to znamená že zo štvorcových dielikov spravím také všelijaké (na to slúži funkcia *vylepsi_hranu*)
    - pre toto je kľúčová class *Hraná_medzi*, ktorá náhodne vygeneruje nejakú funkciu, ktorá pre hranu určitej dĺžky povie, ktoré pixely okolo danej hrany majú byť vyplnené a ktoré nie
    - preto obrázok každého dielika je v skutočnosti o konštantu večší ako jeho pôvodná šírka, aby sa tam zmestili aj tie vylepšenia. Pri zobrazovaní potom každý dielik zobrazím o toľko inde, aby bol na správnej pozícii
    - dieliky generujem tak, že si vyberiem nejaké dva náhodné body nie príliš ďaleko od seba. Spravím kružnicu určitého polomeru cez tieto dva body (túto funkciu som si požičal od umelej inteligencie). Kružnica a priestor pod spojnicami krajov hrany a daných bodov tvoria priestor, určený na vyplnenie pixelami jedného z dielikov susediacich s touto hranou, zvyšné pixely susedných dielikov nastavím na priesvitné
    - pre konkrétnu dvojicu dielikov teda dokážem pomocou tejto funkcie vytvoriť ich okraje tak, aby pasovali a boli príslušného tvaru
    - teda pre každú (neusporiadanú) dvojicu dielikov spravím príslušné operácie

Dieliky v skladacej ploche reprezentujem ako súvislé komponenty spojených dielikov, tj. na začiatku každý dielik je v separátnej komponente. Takúto komponentu reprezentuje *Komponenta* v komponenta.py
- komponenta si pametá všetky svoje dieliky, rotáciu
- komponenty dokážem otáčať - to funguje v podstate tak, že pootáčam všetky dieliky v nej a všetky vektory relatívnych pozícii dielikov
- posúvanie komponent dragovaním je priamočiare celkom
- Takto funguje zisťovanie či daná komponenta práve s niečím pasuje:
    - najprv musím zistiť, ktoré komponenty by vôbec dokázali s danou komponentou pasovať, keby boli správne natočené a na správnej pozícii
    - kvôli tomu si pre každý dielik v komponente pametám jeho *vysledny_pos*, teda jeho pozíciu vo finálnom obrázku. Hľadám teda nejakú komponentu, ktorá obsahuje dielik, ktorý má susedný *vysledny_pos* k nejakému dieliku z danej komponenty.
    - mám teda funkciu *offset_ze_pasujem_do_komponenty*, ktorá zistí či daná komponenta dokáže pasovať do nejakej konkrétnej inej, ak áno vráti jej pozíciu, kde by mala byť, ak majú pasovať
    - táto funkcia pomocou dfs (kde vrcholy sú dieliky a hrany ak dieliky susedia v finálnom obrázku) zistí či existuje dvojica vrcholov takých, že jeden je z jednej komponenty a druhý z druhej a pasujú k sebe. Ak sa takéto nájdu, potom už len dopočítam pozíciu druhej komponenty tak aby to sedelo

*plocha.py* rieši komponenty vrámci skladacej plochy, napríklad spájanie komponent
- spájanie komponent riešim len v okamihu keď nejaká komponenta bude položená (teda prestane byť dragovaná)
- vtedy zistím aké komponenty k nej dokážu pasovať a kde majú byť aby pasovali, ak sú dostatočne blízko, tak ich spojím do jednej
- spájanie komponent je jednoduché, proste len všetky dieliky z jednej pridám do druhej a nastavím im správne pozície

*suflik.py* rieši veci týkajúce sa zásoby dielikov v dolnej časti
- zakaždým keď sa so zásobou dielikov niečo zmení, tak zavolám *pozicie_update*, čo uprace dieliky do riadkov
- *pridaj_komponentu* pridá nový dielik na koniec
- *posúvanie_update* rieši posúvanie zásoby dielikov koliečkom myse

*main.py* je ten súbor, ktorý treba spúšťať, v podstate spúšťa všetky funkcie, ktoré treba aby bežali každý frame
zobrazovanie
- všetky objekty, ktoré niečo zobrazujú majú funkciu *zobraz*, ktorá vráti inštrukcie pre zobrazenie daného obrázku, spolu s prioritou, v akom poradí sa má daný obrázok zobraziť relatívne k ostatným (to čo sa zobrazí neskôr bude akokeby navrchu)
- tieto veci teda utriedim podľa priority a zobrazím

*zobrazovac.py* - aby som dokázal zoomovať a posúvať skladaciu plochu, mám objekt Zobrazovač, ktorý je v podstate alternatívna obrazovka
- mám nejaký offset a zoom o ktorý je táto obrazovka posunutá, priblížená od normálnej obrazovky
- vždy keď niečo chcem zobraziť, prepočítam toho pozíciu tak, aby sa zobrazila správne
- niekedy potrebujem aj opačnú operáciu - teda podľa pozície na obrazovke zistiť reálnu pozíciu v posunutom/priblíženom svete, preto mám aj inverznú funkciu k tej predošlej
    - používam to napríklad na vypočítanie pozície, kde sa má zjaviť dielik potiahnutý zo zásoby dielikov do skladacej plochy

*konstanty.py* obsahuje konštanty

Problémy

tým, že dieliky sa zvečšujú a zmenšujú, tak niekedy potom k sebe už nedoliehajú presne, kvôli tomu, že funkcia na zvečšovanie/zmenšovanie obrázkov niekedy susedné dieliky zvečší/zmenší nie úplne presne, že tam vzniká malá medzera