4 losse queries omdat Oracle SQL een max van 1000 items heeft voor WHERE code IN (...)

```sql
select stuk.id, bovenliggende_beschrijving.id as boven_id, toegang_beschrijving.id as top_id, stuk.guid, concat(concat(concat(concat(top.nummer,top.code),'.'),stuk.nummer),stuk.code) as inv, aet.code,
    stuk_beschrijving.beschrijving as stuk_beschrijving,
    bovenliggende_beschrijving.beschrijving as bovenliggende_beschrijving,
    toegang_beschrijving.beschrijving as toegang_beschrijving
from archiefeenheden stuk
join archiefeenheden top on stuk.ahd_id_top=top.id
join archief_beschrijvingen stuk_beschrijving on stuk_beschrijving.id=stuk.id
join archief_beschrijvingen bovenliggende_beschrijving on bovenliggende_beschrijving.id=stuk.ahd_id
join archief_beschrijvingen toegang_beschrijving on toegang_beschrijving.id=stuk.ahd_id_top
join archiefeenheidsoorten aet on aet.id=stuk.aet_id
where stuk.aet_id!=186 
and concat(concat(concat(concat(top.nummer,top.code),'.'),stuk.nummer),stuk.code)
    in ('1136.273' ), --ZIE nummers in deze map
```