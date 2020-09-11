### Mottak-arkiv-service

### Databaseskjema
Koden under kan brukes på: https://dbdiagram.io/
```
//// -- LEVEL 1
//// -- Tables and References

// Creating tables
Table arkivuttrekk as a {
    id int [pk, increment] // auto-increment
    objId uuid
    status enum
    arkivtype enum
    tittel varchar
    metadataFil int
    avgiverNavn varchar
    avgiverEpost varchar
    avgiverOrganisasjon varchar
    koordinator varchar
    opprettetDato timestamp
    endretDato timestamp
  }

Table metadata_fil {
    id int [pk]
    type varchar
    filnavn varchar
    data text
    opplastetDato timestamp
 }

 Table invitasjon {
    id int
    arkivId int
    status varchar
 }

 Table tester {
    id int
    arkivId int
    epost varchar
 }

 Table arkiv_overforingspakke {
    id int
    arkivuttrekkId int
    navn varchar
    storrelse int
    status enum
 }


 Table lokasjon {
   id int
   arkivuttrekkId int
   kontainer varchar
   generasjon int
 }


// Creating references
// You can also define relaionship separately
// > many-to-one; < one-to-many; - one-to-one
Ref: a.metadataFil - metadata_fil.id
Ref: a.id - invitasjon.arkivId
Ref: a.id - tester.arkivId
Ref: arkivuttrekk.id - arkiv_overforingspakke.arkivuttrekkId
Ref: arkivuttrekk.id - lokasjon.arkivuttrekkId
//----------------------------------------------//
```
