# SF2DPH
Generator DPH a KH z dat SuperFaktury

Pozadavky:
- platny ucet na SuperFaktura
- vygenerovany API klic
- schopnost upravovat Python script

Zprovozneni:
Otevrete soubor get_data_from_sf.py a doplnte:
- API klic a email na zacatku scriptu
- sve udaje do tzv. vet XML souboru. Hledejte slovo DOPLNIT. Jsou to udaje dle formatu, jako je adresa, jmeno, cislo pracoviste atd.

Pokud bylo vse spravne doplneno, staci spustit script a ten na konzoli vypise aktualni stav pro posledni mesic a vygeneruje vhodna XML k odeslani do datove schranky

Kredit:
knihovna z 99% pouziva kod pysuperfaktura, aktualne udrzovany na https://github.com/milano-slesarik/pysuperfaktura
