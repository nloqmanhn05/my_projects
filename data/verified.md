# Reka — Verification Report

Generated from `data/results.json` by `pipeline/verify.py`. Read alongside the raw attachments before claiming results.

## Summary

| Outcome | Count |
| --- | --- |
| OK | 454 |
| MISMATCH | 51 |
| NEEDS_REVIEW | 15 |
| _Total_ | 520 |

## Candidate false positives (MISMATCH field whose SI/BL raw text is identical)

_None — every flagged MISMATCH field has distinct source text on the two docs._

## Per-email audit (BL_COMPARISON)

### email_001 — OK

- Docs: email_001_SI.txt, email_001_BL.txt
- All 7 fields match SI vs BL.
### email_004 — MISMATCH

- Docs: email_004_SI.txt, email_004_BL.txt

| Field | SI | BL |
| --- | --- | --- |
|    shipper | APRIL FAR EAST (M) SDN BHD / TOWER 2, AVENUE 5, LEVEL 6; BANGSAR SOUTH CITY, NO. | APRIL FAR EAST (M) SDN BHD / TOWER 2, AVENUE 5, LEVEL 6; BANGSAR SOUTH CITY, NO. |
| ❌ consignee | EAST BRIGHT FZ-LLC / RAKEZ AMENITY CENTER; AL HAMRA INDUSTRIAL ZONE, RAK, UAE | UAB NOVAKOPA / RAKEZ AMENITY CENTER; AL HAMRA INDUSTRIAL ZONE, RAK, UAE |
| ❌ notify_party | EAST BRIGHT FZ-LLC | UAB NOVAKOPA |
|    port_of_loading | NANTONG, CHINA (CNNTG) | NANTONG, CHINA (CNNTG) |
|    port_of_discharge | KARACHI, PAKISTAN (PKKHI) | KARACHI, PAKISTAN (PKKHI) |
|    container_count | 6 | 6 |
|    gross_weight_kg | 131058.0 | 131058.0 |

### email_005 — OK

- Docs: email_005_SI.xlsx, email_005_BL.xlsx
- All 7 fields match SI vs BL.
### email_009 — OK

- Docs: email_009_SI.txt, email_009_BL.txt
- All 7 fields match SI vs BL.
### email_013 — MISMATCH

- Docs: email_013_SI.txt, email_013_BL.txt

| Field | SI | BL |
| --- | --- | --- |
|    shipper | ASIA PACIFIC PAPERBOARD TRADING PTE LTD / 80 RAFFLES PLACE, #50-01 UOB PLAZA 1;  | ASIA PACIFIC PAPERBOARD TRADING PTE LTD / 80 RAFFLES PLACE, #50-01 UOB PLAZA 1;  |
|    consignee | ROXCEL TRADING GMBH / OPERNRING 3-5; 1010 VIENNA, AUSTRIA | ROXCEL TRADING GMBH / OPERNRING 3-5; 1010 VIENNA, AUSTRIA |
|    notify_party | ROXCEL TRADING GMBH | ROXCEL TRADING GMBH |
|    port_of_loading | SINGAPORE (SGSIN) | SINGAPORE (SGSIN) |
| ❌ port_of_discharge | MOMBASA, KENYA (KEMBA) | TUTICORIN, INDIA (KEMBA) |
|    container_count | 3 | 3 |
|    gross_weight_kg | 67311.0 | 67311.0 |

### email_025 — MISMATCH

- Docs: email_025_SI.txt, email_025_BL.txt

| Field | SI | BL |
| --- | --- | --- |
|    shipper | APRIL FAR EAST (M) SDN BHD / TOWER 2, AVENUE 5, LEVEL 6; BANGSAR SOUTH CITY, NO. | APRIL FAR EAST (M) SDN BHD / TOWER 2, AVENUE 5, LEVEL 6; BANGSAR SOUTH CITY, NO. |
|    consignee | CERIEX / ZONE INDUSTRIELLE; CONAKRY, GUINEA | CERIEX / ZONE INDUSTRIELLE; CONAKRY, GUINEA |
|    notify_party | ROXCEL TRADING GMBH | ROXCEL TRADING GMBH |
|    port_of_loading | PORT KLANG (WESTPORT), MALAYSIA (MYPKG) | PORT KLANG (WESTPORT), MALAYSIA (MYPKG) |
| ❌ port_of_discharge | FREMANTLE, AUSTRALIA (AUFRE) | BUSAN, SOUTH KOREA (AUFRE) |
| ❌ container_count | 6 | 5 |
|    gross_weight_kg | 135126.0 | 135126.0 |

### email_031 — MISMATCH

- Docs: email_031_SI.txt, email_031_BL.txt

| Field | SI | BL |
| --- | --- | --- |
|    shipper | APRIL FINE PAPER TRADING (MIDDLE EAST) FZE / #813, 4 EA, DUBAI AIRPORT FREE ZONE | APRIL FINE PAPER TRADING (MIDDLE EAST) FZE / #813, 4 EA, DUBAI AIRPORT FREE ZONE |
|    consignee | VITAL SOLUTIONS PTE. LTD. / 77 ROBINSON ROAD; #21-01 ROBINSON 77; SINGAPORE 0688 | VITAL SOLUTIONS PTE. LTD. / 77 ROBINSON ROAD; #21-01 ROBINSON 77; SINGAPORE 0688 |
|    notify_party | VITAL SOLUTIONS PTE. LTD. | VITAL SOLUTIONS PTE. LTD. |
|    port_of_loading | NHAVA SHEVA, INDIA (INNSA) | NHAVA SHEVA, INDIA (INNSA) |
|    port_of_discharge | MOMBASA, KENYA (KEMBA) | MOMBASA, KENYA (KEMBA) |
| ❌ container_count | 1 | 3 |
| ❌ gross_weight_kg | 21114.0 | 23114.0 |

### email_032 — OK

- Docs: email_032_SI.txt, email_032_BL.txt
- All 7 fields match SI vs BL.
### email_034 — OK

- Docs: email_034_SI.txt, email_034_BL.txt
- All 7 fields match SI vs BL.
### email_040 — OK

- Docs: email_040_SI.txt, email_040_BL.txt
- All 7 fields match SI vs BL.
### email_043 — MISMATCH

- Docs: email_043_SI.txt, email_043_BL.txt

| Field | SI | BL |
| --- | --- | --- |
|    shipper | ASIA PACIFIC PAPERBOARD TRADING PTE LTD / 80 RAFFLES PLACE, #50-01 UOB PLAZA 1;  | ASIA PACIFIC PAPERBOARD TRADING PTE LTD / 80 RAFFLES PLACE, #50-01 UOB PLAZA 1;  |
|    consignee | PACIFIC OFFICE (M) SDN BHD / LOT 6, JALAN P/7; SECTION 13, 43650 BANDAR BARU BAN | PACIFIC OFFICE (M) SDN BHD / LOT 6, JALAN P/7; SECTION 13, 43650 BANDAR BARU BAN |
|    notify_party | PACIFIC OFFICE (M) SDN BHD | PACIFIC OFFICE (M) SDN BHD |
|    port_of_loading | NHAVA SHEVA, INDIA (INNSA) | NHAVA SHEVA, INDIA (INNSA) |
|    port_of_discharge | KLAIPEDA, LITHUANIA (LTKLJ) | KLAIPEDA, LITHUANIA (LTKLJ) |
| ❌ container_count | 3 | 5 |
|    gross_weight_kg | 68649.0 | 68649.0 |

### email_044 — OK

- Docs: email_044_SI.txt, email_044_BL.txt
- All 7 fields match SI vs BL.
### email_046 — MISMATCH

- Docs: email_046_SI.txt, email_046_BL.txt

| Field | SI | BL |
| --- | --- | --- |
|    shipper | APRIL FINE PAPER TRADING (MIDDLE EAST) FZE / #813, 4 EA, DUBAI AIRPORT FREE ZONE | APRIL FINE PAPER TRADING (MIDDLE EAST) FZE / #813, 4 EA, DUBAI AIRPORT FREE ZONE |
|    consignee | SAFQA LIMITED / P.O. BOX 99423-80100; TONONOKA ROAD; MOMBASA, KENYA; PIN NO.: P0 | SAFQA LIMITED / P.O. BOX 99423-80100; TONONOKA ROAD; MOMBASA, KENYA; PIN NO.: P0 |
| ❌ notify_party | TOPKOPY MIDDLE EAST FZE | MOORIM SP CO., LTD |
|    port_of_loading | PORT KLANG (WESTPORT), MALAYSIA (MYPKG) | PORT KLANG (WESTPORT), MALAYSIA (MYPKG) |
|    port_of_discharge | SAVANNAH, US (USSAV) | SAVANNAH, US (USSAV) |
|    container_count | 12 | 12 |
|    gross_weight_kg | 257340.0 | 257340.0 |

### email_051 — OK

- Docs: email_051_SI.txt, email_051_BL.txt
- All 7 fields match SI vs BL.
### email_052 — OK

- Docs: email_052_SI.txt, email_052_BL.txt
- All 7 fields match SI vs BL.
### email_055 — OK

- Docs: email_055_SI.xlsx, email_055_BL.docx
- All 7 fields match SI vs BL.
### email_056 — OK

- Docs: email_056_SI.txt, email_056_BL.txt
- All 7 fields match SI vs BL.
### email_058 — OK

- Docs: email_058_SI.txt, email_058_BL.txt
- All 7 fields match SI vs BL.
### email_059 — OK

- Docs: email_059_SI.pdf, email_059_BL.pdf
- All 7 fields match SI vs BL.
### email_064 — OK

- Docs: email_064_SI.txt, email_064_BL.txt
- All 7 fields match SI vs BL.
### email_065 — MISMATCH

- Docs: email_065_SI.txt, email_065_BL.txt

| Field | SI | BL |
| --- | --- | --- |
|    shipper | APRIL FINE PAPER TRADING (MIDDLE EAST) FZE / #813, 4 EA, DUBAI AIRPORT FREE ZONE | APRIL FINE PAPER TRADING (MIDDLE EAST) FZE / #813, 4 EA, DUBAI AIRPORT FREE ZONE |
|    consignee | INTERNATIONAL FOREST PRODUCTS LLC / 6 HOLLIS STREET; SUITE 100; FRAMINGHAM, MA 0 | INTERNATIONAL FOREST PRODUCTS LLC / 6 HOLLIS STREET; SUITE 100; FRAMINGHAM, MA 0 |
| ❌ notify_party | INTERNATIONAL FOREST PRODUCTS LLC | HABRAS INTERNATIONAL LIMITED |
|    port_of_loading | PORT KLANG (WESTPORT), MALAYSIA (MYPKG) | PORT KLANG (WESTPORT), MALAYSIA (MYPKG) |
| ❌ port_of_discharge | HOCHIMINH CITY, VIETNAM (VNSGN) | BUSAN, SOUTH KOREA (VNSGN) |
|    container_count | 1 | 1 |
|    gross_weight_kg | 21479.0 | 21479.0 |

### email_068 — OK

- Docs: email_068_SI.txt, email_068_BL.txt
- All 7 fields match SI vs BL.
### email_071 — MISMATCH

- Docs: email_071_SI.txt, email_071_BL.txt

| Field | SI | BL |
| --- | --- | --- |
|    shipper | APRIL FAR EAST (M) SDN BHD / TOWER 2, AVENUE 5, LEVEL 6; BANGSAR SOUTH CITY, NO. | APRIL FAR EAST (M) SDN BHD / TOWER 2, AVENUE 5, LEVEL 6; BANGSAR SOUTH CITY, NO. |
|    consignee | HABRAS INTERNATIONAL LIMITED / OFFICE 1204, THE BURLINGTON TOWER; BUSINESS BAY,  | HABRAS INTERNATIONAL LIMITED / OFFICE 1204, THE BURLINGTON TOWER; BUSINESS BAY,  |
|    notify_party | HABRAS INTERNATIONAL LIMITED | HABRAS INTERNATIONAL LIMITED |
|    port_of_loading | PORT KLANG (WESTPORT), MALAYSIA (MYPKG) | PORT KLANG (WESTPORT), MALAYSIA (MYPKG) |
| ❌ port_of_discharge | YANGON, MYANMAR (MMRGN) | CEBU, PHILIPPINES (MMRGN) |
| ❌ container_count | 6 | 8 |
|    gross_weight_kg | 132006.0 | 132006.0 |

### email_082 — OK

- Docs: email_082_SI.txt, email_082_BL.txt
- All 7 fields match SI vs BL.
### email_090 — OK

- Docs: email_090_SI.txt, email_090_BL.txt
- All 7 fields match SI vs BL.
### email_091 — MISMATCH

- Docs: email_091_SI.txt, email_091_BL.txt

| Field | SI | BL |
| --- | --- | --- |
|    shipper | APRIL FINE PAPER TRADING / ON BEHALF OF VITAL SOLUTIONS PTE LTD; 77 ROBINSON ROA | APRIL FINE PAPER TRADING / ON BEHALF OF VITAL SOLUTIONS PTE LTD; 77 ROBINSON ROA |
|    consignee | ORIENT LINKS CO (LLC) / P.O. BOX 61041; JEBEL ALI, DUBAI, UAE | ORIENT LINKS CO (LLC) / P.O. BOX 61041; JEBEL ALI, DUBAI, UAE |
|    notify_party | VITAL SOLUTIONS PTE. LTD. | VITAL SOLUTIONS PTE. LTD. |
|    port_of_loading | NHAVA SHEVA, INDIA (INNSA) | NHAVA SHEVA, INDIA (INNSA) |
|    port_of_discharge | CALLAO, PERU (PECLL) | CALLAO, PERU (PECLL) |
| ❌ container_count | 3 | 2 |
|    gross_weight_kg | 67953.0 | 67953.0 |

### email_096 — OK

- Docs: email_096_SI.txt, email_096_BL.txt
- All 7 fields match SI vs BL.
### email_097 — MISMATCH

- Docs: email_097_SI.xlsx, email_097_BL.docx

| Field | SI | BL |
| --- | --- | --- |
|    shipper | APRIL FINE PAPER TRADING (MIDDLE EAST) FZE | #813, 4 EA, DUBAI AIRPORT FREE ZONE | APRIL FINE PAPER TRADING (MIDDLE EAST) FZE / #813, 4 EA, DUBAI AIRPORT FREE ZONE |
|    consignee | ROXCEL TRADING GMBH | OPERNRING 3-5; 1010 VIENNA, AUSTRIA | ROXCEL TRADING GMBH / OPERNRING 3-5 / 1010 VIENNA, AUSTRIA |
|    notify_party | NAGAPPA EXPORTS | NEW NO : 23, L-BLOCK, 17TH STREET; ANNA NAGAR EAST; CHENNAI, T | NAGAPPA EXPORTS / NEW NO : 23, L-BLOCK, 17TH STREET / ANNA NAGAR EAST / CHENNAI, |
|    port_of_loading | SINGAPORE | SINGAPORE |
|    port_of_discharge | BRISBANE, AUSTRALIA | BRISBANE, AUSTRALIA |
| ❌ container_count | 10 | 11 |
| ❌ gross_weight_kg | 216950.0 | 215950.0 |

### email_107 — MISMATCH

- Docs: email_107_SI.xlsx, email_107_BL.docx

| Field | SI | BL |
| --- | --- | --- |
|    shipper | APRIL FINE PAPER TRADING (MIDDLE EAST) FZE | #813, 4 EA, DUBAI AIRPORT FREE ZONE | APRIL FINE PAPER TRADING (MIDDLE EAST) FZE / #813, 4 EA, DUBAI AIRPORT FREE ZONE |
| ❌ consignee | KTP CO., LTD | KTP BLDG., 36 SANGWON-GIL; SEOUNGDONG-GU, SEOUL, SOUTH KOREA; TEL | VITAL SOLUTIONS PTE. LTD. / KTP BLDG., 36 SANGWON-GIL / SEOUNGDONG-GU, SEOUL, SO |
|    notify_party | KTP CO., LTD | KTP BLDG., 36 SANGWON-GIL; SEOUNGDONG-GU, SEOUL, SOUTH KOREA; TEL | KTP CO., LTD / KTP BLDG., 36 SANGWON-GIL / SEOUNGDONG-GU, SEOUL, SOUTH KOREA / T |
|    port_of_loading | PORT KLANG (WESTPORT), MALAYSIA | PORT KLANG (WESTPORT), MALAYSIA |
|    port_of_discharge | MOMBASA, KENYA | MOMBASA, KENYA |
| ❌ container_count | 2 | 3 |
|    gross_weight_kg | 41124.0 | 41124.0 |

### email_111 — MISMATCH

- Docs: email_111_SI.txt, email_111_BL.txt

| Field | SI | BL |
| --- | --- | --- |
|    shipper | APRIL FAR EAST (M) SDN BHD / TOWER 2, AVENUE 5, LEVEL 6; BANGSAR SOUTH CITY, NO. | APRIL FAR EAST (M) SDN BHD / TOWER 2, AVENUE 5, LEVEL 6; BANGSAR SOUTH CITY, NO. |
|    consignee | CLIFFORD PAPER INC / 70 EAST STREET; RIDGEFIELD, NJ 07657, USA | CLIFFORD PAPER INC / 70 EAST STREET; RIDGEFIELD, NJ 07657, USA |
|    notify_party | CLIFFORD PAPER INC | CLIFFORD PAPER INC |
|    port_of_loading | RUGAO/NANTONG/SHANGHAI, CHINA (CNSHA) | RUGAO/NANTONG/SHANGHAI, CHINA (CNSHA) |
|    port_of_discharge | APAPA, NIGERIA (NGAPP) | APAPA, NIGERIA (NGAPP) |
| ❌ container_count | 4 | 3 |
|    gross_weight_kg | 91524.0 | 91524.0 |

### email_113 — OK

- Docs: email_113_SI.txt, email_113_BL.txt
- All 7 fields match SI vs BL.
### email_118 — OK

- Docs: email_118_SI.txt, email_118_BL.txt
- All 7 fields match SI vs BL.
### email_119 — MISMATCH

- Docs: email_119_SI.txt, email_119_BL.txt

| Field | SI | BL |
| --- | --- | --- |
|    shipper | APRIL FINE PAPER TRADING / ON BEHALF OF VITAL SOLUTIONS PTE LTD; 77 ROBINSON ROA | APRIL FINE PAPER TRADING / ON BEHALF OF VITAL SOLUTIONS PTE LTD; 77 ROBINSON ROA |
|    consignee | CLIFFORD PAPER INC / 70 EAST STREET; RIDGEFIELD, NJ 07657, USA | CLIFFORD PAPER INC / 70 EAST STREET; RIDGEFIELD, NJ 07657, USA |
|    notify_party | CLIFFORD PAPER INC | CLIFFORD PAPER INC |
| ❌ port_of_loading | PORT KLANG (WESTPORT), MALAYSIA (MYPKG) | SINGAPORE, SINGAPORE (MYPKG) |
|    port_of_discharge | SAVANNAH, US (USSAV) | SAVANNAH, US (USSAV) |
|    container_count | 15 | 15 |
|    gross_weight_kg | 322590.0 | 322590.0 |

### email_121 — MISMATCH

- Docs: email_121_SI.txt, email_121_BL.txt

| Field | SI | BL |
| --- | --- | --- |
|    shipper | APRIL FINE PAPER TRADING (MIDDLE EAST) FZE / #813, 4 EA, DUBAI AIRPORT FREE ZONE | APRIL FINE PAPER TRADING (MIDDLE EAST) FZE / #813, 4 EA, DUBAI AIRPORT FREE ZONE |
|    consignee | CLIFFORD PAPER INC / 70 EAST STREET; RIDGEFIELD, NJ 07657, USA | CLIFFORD PAPER INC / 70 EAST STREET; RIDGEFIELD, NJ 07657, USA |
|    notify_party | CLIFFORD PAPER INC | CLIFFORD PAPER INC |
|    port_of_loading | NANTONG, CHINA (CNNTG) | NANTONG, CHINA (CNNTG) |
|    port_of_discharge | BRISBANE, AUSTRALIA (AUBNE) | BRISBANE, AUSTRALIA (AUBNE) |
|    container_count | 1 | 1 |
| ❌ gross_weight_kg | 20842.0 | 21342.0 |

### email_128 — MISMATCH

- Docs: email_128_SI.txt, email_128_BL.txt

| Field | SI | BL |
| --- | --- | --- |
|    shipper | APRIL FINE PAPER TRADING / ON BEHALF OF VITAL SOLUTIONS PTE LTD; 77 ROBINSON ROA | APRIL FINE PAPER TRADING / ON BEHALF OF VITAL SOLUTIONS PTE LTD; 77 ROBINSON ROA |
|    consignee | BALL & DOGGETT AUSTRALIA PTY LTD / 43-45 METROPOLITAN ROAD; ENFIELD NSW 2136, AU | BALL & DOGGETT AUSTRALIA PTY LTD / 43-45 METROPOLITAN ROAD; ENFIELD NSW 2136, AU |
|    notify_party | BALL & DOGGETT AUSTRALIA PTY LTD | BALL & DOGGETT AUSTRALIA PTY LTD |
| ❌ port_of_loading | NHAVA SHEVA, INDIA (INNSA) | BUATAN, INDONESIA (INNSA) |
|    port_of_discharge | NEW YORK, US (USNYC) | NEW YORK, US (USNYC) |
|    container_count | 15 | 15 |
| ❌ gross_weight_kg | 323250.0 | 322250.0 |

### email_129 — MISMATCH

- Docs: email_129_SI.txt, email_129_BL.txt

| Field | SI | BL |
| --- | --- | --- |
|    shipper | APRIL FINE PAPER TRADING / ON BEHALF OF VITAL SOLUTIONS PTE LTD; 77 ROBINSON ROA | APRIL FINE PAPER TRADING / ON BEHALF OF VITAL SOLUTIONS PTE LTD; 77 ROBINSON ROA |
|    consignee | SAFQA LIMITED / P.O. BOX 99423-80100; TONONOKA ROAD; MOMBASA, KENYA; PIN NO.: P0 | SAFQA LIMITED / P.O. BOX 99423-80100; TONONOKA ROAD; MOMBASA, KENYA; PIN NO.: P0 |
|    notify_party | SAFQA LIMITED | SAFQA LIMITED |
| ❌ port_of_loading | NHAVA SHEVA, INDIA (INNSA) | BUATAN, INDONESIA (INNSA) |
| ❌ port_of_discharge | ASHDOD, ISRAEL (ILASH) | TUTICORIN, INDIA (ILASH) |
|    container_count | 6 | 6 |
|    gross_weight_kg | 124188.0 | 124188.0 |

### email_132 — OK

- Docs: email_132_SI.txt, email_132_BL.txt
- All 7 fields match SI vs BL.
### email_133 — MISMATCH

- Docs: email_133_SI.txt, email_133_BL.txt

| Field | SI | BL |
| --- | --- | --- |
|    shipper | APRIL FINE PAPER TRADING / ON BEHALF OF VITAL SOLUTIONS PTE LTD; 77 ROBINSON ROA | APRIL FINE PAPER TRADING / ON BEHALF OF VITAL SOLUTIONS PTE LTD; 77 ROBINSON ROA |
|    consignee | MOORIM SP CO., LTD / 656, GANGNAM-DAERO, GANGNAM-GU; SEOUL, SOUTH KOREA; T. 82-2 | MOORIM SP CO., LTD / 656, GANGNAM-DAERO, GANGNAM-GU; SEOUL, SOUTH KOREA; T. 82-2 |
|    notify_party | BALL & DOGGETT AUSTRALIA PTY LTD | BALL & DOGGETT AUSTRALIA PTY LTD |
|    port_of_loading | NANTONG, CHINA (CNNTG) | NANTONG, CHINA (CNNTG) |
|    port_of_discharge | CALLAO, PERU (PECLL) | CALLAO, PERU (PECLL) |
|    container_count | 6 | 6 |
| ❌ gross_weight_kg | 142848.0 | 144848.0 |

### email_143 — OK

- Docs: email_143_SI.txt, email_143_BL.txt
- All 7 fields match SI vs BL.
### email_144 — MISMATCH

- Docs: email_144_SI.txt, email_144_BL.txt

| Field | SI | BL |
| --- | --- | --- |
|    shipper | APRIL FINE PAPER TRADING / ON BEHALF OF VITAL SOLUTIONS PTE LTD; 77 ROBINSON ROA | APRIL FINE PAPER TRADING / ON BEHALF OF VITAL SOLUTIONS PTE LTD; 77 ROBINSON ROA |
| ❌ consignee | NAGAPPA EXPORTS / NEW NO : 23, L-BLOCK, 17TH STREET; ANNA NAGAR EAST; CHENNAI, T | PACIFIC OFFICE (M) SDN BHD / NEW NO : 23, L-BLOCK, 17TH STREET; ANNA NAGAR EAST; |
|    notify_party | NAGAPPA EXPORTS | NAGAPPA EXPORTS |
|    port_of_loading | NHAVA SHEVA, INDIA (INNSA) | NHAVA SHEVA, INDIA (INNSA) |
|    port_of_discharge | MERSIN, TURKEY (TRMER) | MERSIN, TURKEY (TRMER) |
| ❌ container_count | 12 | 11 |
|    gross_weight_kg | 264180.0 | 264180.0 |

### email_145 — MISMATCH

- Docs: email_145_SI.txt, email_145_BL.txt

| Field | SI | BL |
| --- | --- | --- |
| ❌ shipper | APRIL FINE PAPER TRADING / ON BEHALF OF VITAL SOLUTIONS PTE LTD; 77 ROBINSON ROA | APRIL FINE PAPER TRADING (MIDDLE EAST) FZE / ON BEHALF OF VITAL SOLUTIONS PTE LT |
|    consignee | PACIFIC OFFICE (M) SDN BHD / LOT 6, JALAN P/7; SECTION 13, 43650 BANDAR BARU BAN | PACIFIC OFFICE (M) SDN BHD / LOT 6, JALAN P/7; SECTION 13, 43650 BANDAR BARU BAN |
|    notify_party | PACIFIC OFFICE (M) SDN BHD | PACIFIC OFFICE (M) SDN BHD |
|    port_of_loading | NANTONG, CHINA (CNNTG) | NANTONG, CHINA (CNNTG) |
|    port_of_discharge | BUSAN, SOUTH KOREA (KRPUS) | BUSAN, SOUTH KOREA (KRPUS) |
|    container_count | 15 | 15 |
|    gross_weight_kg | 313380.0 | 313380.0 |

### email_146 — OK

- Docs: email_146_SI.txt, email_146_BL.txt
- All 7 fields match SI vs BL.
### email_160 — OK

- Docs: email_160_SI.pdf, email_160_BL.pdf
- All 7 fields match SI vs BL.
### email_167 — OK

- Docs: email_167_SI.txt, email_167_BL.txt
- All 7 fields match SI vs BL.
### email_171 — OK

- Docs: email_171_SI.xlsx, email_171_BL.xlsx
- All 7 fields match SI vs BL.
### email_174 — MISMATCH

- Docs: email_174_SI.txt, email_174_BL.txt

| Field | SI | BL |
| --- | --- | --- |
|    shipper | APRIL FINE PAPER TRADING (MIDDLE EAST) FZE / #813, 4 EA, DUBAI AIRPORT FREE ZONE | APRIL FINE PAPER TRADING (MIDDLE EAST) FZE / #813, 4 EA, DUBAI AIRPORT FREE ZONE |
|    consignee | TOAN LUC PAPER JOINT STOCK COMPANY / LOT B, TAN DONG HIEP B IZ; DI AN, BINH DUON | TOAN LUC PAPER JOINT STOCK COMPANY / LOT B, TAN DONG HIEP B IZ; DI AN, BINH DUON |
| ❌ notify_party | TOAN LUC PAPER JOINT STOCK COMPANY | MOORIM SP CO., LTD |
|    port_of_loading | RUGAO/NANTONG/SHANGHAI, CHINA (CNSHA) | RUGAO/NANTONG/SHANGHAI, CHINA (CNSHA) |
| ❌ port_of_discharge | CONAKRY, GUINEA (GNCKY) | HOCHIMINH CITY, VIETNAM (GNCKY) |
|    container_count | 1 | 1 |
|    gross_weight_kg | 20532.0 | 20532.0 |

### email_175 — OK

- Docs: email_175_SI.txt, email_175_BL.txt
- All 7 fields match SI vs BL.
### email_178 — MISMATCH

- Docs: email_178_SI.txt, email_178_BL.txt

| Field | SI | BL |
| --- | --- | --- |
|    shipper | APRIL FAR EAST (M) SDN BHD / TOWER 2, AVENUE 5, LEVEL 6; BANGSAR SOUTH CITY, NO. | APRIL FAR EAST (M) SDN BHD / TOWER 2, AVENUE 5, LEVEL 6; BANGSAR SOUTH CITY, NO. |
|    consignee | ORIENT LINKS CO (LLC) / P.O. BOX 61041; JEBEL ALI, DUBAI, UAE | ORIENT LINKS CO (LLC) / P.O. BOX 61041; JEBEL ALI, DUBAI, UAE |
|    notify_party | 3S PAPER PRODUCTS SDN BHD | 3S PAPER PRODUCTS SDN BHD |
|    port_of_loading | PORT KLANG (WESTPORT), MALAYSIA (MYPKG) | PORT KLANG (WESTPORT), MALAYSIA (MYPKG) |
|    port_of_discharge | CALLAO, PERU (PECLL) | CALLAO, PERU (PECLL) |
| ❌ container_count | 6 | 7 |
|    gross_weight_kg | 132516.0 | 132516.0 |

### email_182 — MISMATCH

- Docs: email_182_SI.txt, email_182_BL.txt

| Field | SI | BL |
| --- | --- | --- |
|    shipper | APRIL FAR EAST (M) SDN BHD / TOWER 2, AVENUE 5, LEVEL 6; BANGSAR SOUTH CITY, NO. | APRIL FAR EAST (M) SDN BHD / TOWER 2, AVENUE 5, LEVEL 6; BANGSAR SOUTH CITY, NO. |
|    consignee | KTP CO., LTD / KTP BLDG., 36 SANGWON-GIL; SEOUNGDONG-GU, SEOUL, SOUTH KOREA; TEL | KTP CO., LTD / KTP BLDG., 36 SANGWON-GIL; SEOUNGDONG-GU, SEOUL, SOUTH KOREA; TEL |
|    notify_party | KTP CO., LTD | KTP CO., LTD |
|    port_of_loading | NANTONG, CHINA (CNNTG) | NANTONG, CHINA (CNNTG) |
| ❌ port_of_discharge | APAPA, NIGERIA (NGAPP) | BALTIMORE, US (NGAPP) |
| ❌ container_count | 5 | 6 |
|    gross_weight_kg | 100240.0 | 100240.0 |

### email_197 — OK

- Docs: email_197_SI.txt, email_197_BL.txt
- All 7 fields match SI vs BL.
### email_198 — OK

- Docs: email_198_SI.txt, email_198_BL.txt
- All 7 fields match SI vs BL.
### email_208 — OK

- Docs: email_208_SI.pdf, email_208_BL.pdf
- All 7 fields match SI vs BL.
### email_225 — MISMATCH

- Docs: email_225_SI.txt, email_225_BL.txt

| Field | SI | BL |
| --- | --- | --- |
|    shipper | ASIA PACIFIC PAPERBOARD TRADING PTE LTD / 80 RAFFLES PLACE, #50-01 UOB PLAZA 1;  | ASIA PACIFIC PAPERBOARD TRADING PTE LTD / 80 RAFFLES PLACE, #50-01 UOB PLAZA 1;  |
| ❌ consignee | ROXCEL TRADING GMBH / OPERNRING 3-5; 1010 VIENNA, AUSTRIA | AL GURG STATIONERY LLC / OPERNRING 3-5; 1010 VIENNA, AUSTRIA |
|    notify_party | TOAN LUC PAPER JOINT STOCK COMPANY | TOAN LUC PAPER JOINT STOCK COMPANY |
|    port_of_loading | PORT KLANG (WESTPORT), MALAYSIA (MYPKG) | PORT KLANG (WESTPORT), MALAYSIA (MYPKG) |
|    port_of_discharge | GDANSK, POLAND (PLGDN) | GDANSK, POLAND (PLGDN) |
|    container_count | 1 | 1 |
|    gross_weight_kg | 22596.0 | 22596.0 |

### email_227 — OK

- Docs: email_227_SI.txt, email_227_BL.txt
- All 7 fields match SI vs BL.
### email_235 — OK

- Docs: email_235_SI.txt, email_235_BL.txt
- All 7 fields match SI vs BL.
### email_239 — OK

- Docs: email_239_SI.txt, email_239_BL.txt
- All 7 fields match SI vs BL.
### email_243 — MISMATCH

- Docs: email_243_SI.xlsx, email_243_BL.xlsx

| Field | SI | BL |
| --- | --- | --- |
|    shipper | ASIA PACIFIC PAPERBOARD TRADING PTE LTD | 80 RAFFLES PLACE, #50-01 UOB PLAZA 1;  | ASIA PACIFIC PAPERBOARD TRADING PTE LTD | 80 RAFFLES PLACE, #50-01 UOB PLAZA 1;  |
|    consignee | SAFQA LIMITED | P.O. BOX 99423-80100; TONONOKA ROAD; MOMBASA, KENYA; PIN NO.: P0 | SAFQA LIMITED | P.O. BOX 99423-80100; TONONOKA ROAD; MOMBASA, KENYA; PIN NO.: P0 |
|    notify_party | SAFQA LIMITED | P.O. BOX 99423-80100; TONONOKA ROAD; MOMBASA, KENYA; PIN NO.: P0 | SAFQA LIMITED | P.O. BOX 99423-80100; TONONOKA ROAD; MOMBASA, KENYA; PIN NO.: P0 |
| ❌ port_of_loading | PORT KLANG (WESTPORT), MALAYSIA | RUGAO/NANTONG/SHANGHAI, CHINA |
| ❌ port_of_discharge | HOUSTON, US | MOMBASA, KENYA |
|    container_count | 5 | 5 |
|    gross_weight_kg | 100445.0 | 100445.0 |

### email_249 — OK

- Docs: email_249_SI.txt, email_249_BL.txt
- All 7 fields match SI vs BL.
### email_256 — MISMATCH

- Docs: email_256_SI.txt, email_256_BL.txt

| Field | SI | BL |
| --- | --- | --- |
| ❌ shipper | APRIL FINE PAPER TRADING / ON BEHALF OF VITAL SOLUTIONS PTE LTD; 77 ROBINSON ROA | APRIL FAR EAST (M) SDN BHD / ON BEHALF OF VITAL SOLUTIONS PTE LTD; 77 ROBINSON R |
|    consignee | SAFQA LIMITED / P.O. BOX 99423-80100; TONONOKA ROAD; MOMBASA, KENYA; PIN NO.: P0 | SAFQA LIMITED / P.O. BOX 99423-80100; TONONOKA ROAD; MOMBASA, KENYA; PIN NO.: P0 |
|    notify_party | HABRAS INTERNATIONAL LIMITED | HABRAS INTERNATIONAL LIMITED |
|    port_of_loading | PORT KLANG (WESTPORT), MALAYSIA (MYPKG) | PORT KLANG (WESTPORT), MALAYSIA (MYPKG) |
| ❌ port_of_discharge | VALPARAISO, CHILE (CLVAP) | FREMANTLE, AUSTRALIA (CLVAP) |
|    container_count | 12 | 12 |
|    gross_weight_kg | 262224.0 | 262224.0 |

### email_270 — MISMATCH

- Docs: email_270_SI.txt, email_270_BL.txt

| Field | SI | BL |
| --- | --- | --- |
|    shipper | APRIL FAR EAST (M) SDN BHD / TOWER 2, AVENUE 5, LEVEL 6; BANGSAR SOUTH CITY, NO. | APRIL FAR EAST (M) SDN BHD / TOWER 2, AVENUE 5, LEVEL 6; BANGSAR SOUTH CITY, NO. |
|    consignee | KPP-ANTALIS (SINGAPORE) PTE. LTD. / 8 TEMASEK BOULEVARD; #42-01 SUNTEC TOWER 3;  | KPP-ANTALIS (SINGAPORE) PTE. LTD. / 8 TEMASEK BOULEVARD; #42-01 SUNTEC TOWER 3;  |
|    notify_party | 3S PAPER PRODUCTS SDN BHD | 3S PAPER PRODUCTS SDN BHD |
|    port_of_loading | SINGAPORE (SGSIN) | SINGAPORE (SGSIN) |
| ❌ port_of_discharge | MERSIN, TURKEY (TRMER) | LONG BEACH, US (TRMER) |
|    container_count | 6 | 6 |
|    gross_weight_kg | 139536.0 | 139536.0 |

### email_273 — OK

- Docs: email_273_SI.pdf, email_273_BL.pdf
- All 7 fields match SI vs BL.
### email_275 — OK

- Docs: email_275_SI.txt, email_275_BL.txt
- All 7 fields match SI vs BL.
### email_291 — MISMATCH

- Docs: email_291_SI.xlsx, email_291_BL.docx

| Field | SI | BL |
| --- | --- | --- |
|    shipper | APRIL FINE PAPER TRADING (MIDDLE EAST) FZE | #813, 4 EA, DUBAI AIRPORT FREE ZONE | APRIL FINE PAPER TRADING (MIDDLE EAST) FZE / #813, 4 EA, DUBAI AIRPORT FREE ZONE |
| ❌ consignee | INTERNATIONAL FOREST PRODUCTS LLC | 6 HOLLIS STREET; SUITE 100; FRAMINGHAM, MA 0 | TOPKOPY MIDDLE EAST FZE / 6 HOLLIS STREET / SUITE 100 / FRAMINGHAM, MA 01702, US |
|    notify_party | INTERNATIONAL FOREST PRODUCTS LLC | 6 HOLLIS STREET; SUITE 100; FRAMINGHAM, MA 0 | INTERNATIONAL FOREST PRODUCTS LLC / 6 HOLLIS STREET / SUITE 100 / FRAMINGHAM, MA |
|    port_of_loading | NANTONG, CHINA | NANTONG, CHINA |
|    port_of_discharge | SAVANNAH, US | SAVANNAH, US |
| ❌ container_count | 1 | 3 |
|    gross_weight_kg | 21745.0 | 21745.0 |

### email_296 — OK

- Docs: email_296_SI.txt, email_296_BL.txt
- All 7 fields match SI vs BL.
### email_300 — MISMATCH

- Docs: email_300_SI.xlsx, email_300_BL.xlsx

| Field | SI | BL |
| --- | --- | --- |
| ❌ shipper | APRIL FAR EAST (M) SDN BHD | TOWER 2, AVENUE 5, LEVEL 6; BANGSAR SOUTH CITY, NO. | APRIL FINE PAPER TRADING (MIDDLE EAST) FZE | TOWER 2, AVENUE 5, LEVEL 6; BANGSAR |
|    consignee | SAFQA LIMITED | P.O. BOX 99423-80100; TONONOKA ROAD; MOMBASA, KENYA; PIN NO.: P0 | SAFQA LIMITED | P.O. BOX 99423-80100; TONONOKA ROAD; MOMBASA, KENYA; PIN NO.: P0 |
| ❌ notify_party | UAB NOVAKOPA | SAVANORIU PR. 187; LT-02300 VILNIUS, LITHUANIA | NAGAPPA EXPORTS | SAVANORIU PR. 187; LT-02300 VILNIUS, LITHUANIA |
|    port_of_loading | NANTONG, CHINA | NANTONG, CHINA |
|    port_of_discharge | VALPARAISO, CHILE | VALPARAISO, CHILE |
|    container_count | 12 | 12 |
|    gross_weight_kg | 243168.0 | 243168.0 |

### email_302 — MISMATCH

- Docs: email_302_SI.xlsx, email_302_BL.docx

| Field | SI | BL |
| --- | --- | --- |
|    shipper | APRIL FINE PAPER TRADING (MIDDLE EAST) FZE | #813, 4 EA, DUBAI AIRPORT FREE ZONE | APRIL FINE PAPER TRADING (MIDDLE EAST) FZE / #813, 4 EA, DUBAI AIRPORT FREE ZONE |
|    consignee | INTERNATIONAL FOREST PRODUCTS LLC | 6 HOLLIS STREET; SUITE 100; FRAMINGHAM, MA 0 | INTERNATIONAL FOREST PRODUCTS LLC / 6 HOLLIS STREET / SUITE 100 / FRAMINGHAM, MA |
|    notify_party | KTP CO., LTD | KTP BLDG., 36 SANGWON-GIL; SEOUNGDONG-GU, SEOUL, SOUTH KOREA; TEL | KTP CO., LTD / KTP BLDG., 36 SANGWON-GIL / SEOUNGDONG-GU, SEOUL, SOUTH KOREA / T |
|    port_of_loading | RUGAO/NANTONG/SHANGHAI, CHINA | RUGAO/NANTONG/SHANGHAI, CHINA |
|    port_of_discharge | BRISBANE, AUSTRALIA | BRISBANE, AUSTRALIA |
| ❌ container_count | 2 | 4 |
|    gross_weight_kg | 40176.0 | 40176.0 |

### email_307 — OK

- Docs: email_307_SI.txt, email_307_BL.txt
- All 7 fields match SI vs BL.
### email_312 — MISMATCH

- Docs: email_312_SI.txt, email_312_BL.txt

| Field | SI | BL |
| --- | --- | --- |
| ❌ shipper | APRIL FINE PAPER TRADING (MIDDLE EAST) FZE / #813, 4 EA, DUBAI AIRPORT FREE ZONE | APRIL FAR EAST (M) SDN BHD / #813, 4 EA, DUBAI AIRPORT FREE ZONE; P.O. BOX: 2937 |
|    consignee | 3S PAPER PRODUCTS SDN BHD / NO 12, JALAN INDUSTRI 3/6; RAWANG INTEGRATED INDUSTR | 3S PAPER PRODUCTS SDN BHD / NO 12, JALAN INDUSTRI 3/6; RAWANG INTEGRATED INDUSTR |
| ❌ notify_party | 3S PAPER PRODUCTS SDN BHD | KPP-ANTALIS (SINGAPORE) PTE. LTD. |
|    port_of_loading | NANTONG, CHINA (CNNTG) | NANTONG, CHINA (CNNTG) |
|    port_of_discharge | BRISBANE, AUSTRALIA (AUBNE) | BRISBANE, AUSTRALIA (AUBNE) |
|    container_count | 10 | 10 |
|    gross_weight_kg | 237010.0 | 237010.0 |

### email_313 — MISMATCH

- Docs: email_313_SI.pdf, email_313_BL.pdf

| Field | SI | BL |
| --- | --- | --- |
|    shipper | APRIL FINE PAPER TRADING / ON BEHALF OF VITAL SOLUTIONS PTE LTD / 77 ROBINSON RO | APRIL FINE PAPER TRADING / ON BEHALF OF VITAL SOLUTIONS PTE LTD / 77 ROBINSON RO |
|    consignee | KPP-ANTALIS (SINGAPORE) PTE. LTD. / 8 TEMASEK BOULEVARD / #42-01 SUNTEC TOWER 3  | KPP-ANTALIS (SINGAPORE) PTE. LTD. / 8 TEMASEK BOULEVARD / #42-01 SUNTEC TOWER 3  |
|    notify_party | KPP-ANTALIS (SINGAPORE) PTE. LTD. / 8 TEMASEK BOULEVARD / #42-01 SUNTEC TOWER 3  | KPP-ANTALIS (SINGAPORE) PTE. LTD. / 8 TEMASEK BOULEVARD / #42-01 SUNTEC TOWER 3  |
|    port_of_loading | RUGAO/NANTONG/SHANGHAI, CHINA | RUGAO/NANTONG/SHANGHAI, CHINA |
|    port_of_discharge | HOCHIMINH CITY, VIETNAM | HOCHIMINH CITY, VIETNAM |
| ❌ container_count | 5 | 4 |
| ❌ gross_weight_kg | 118270.0 | 117770.0 |

### email_324 — MISMATCH

- Docs: email_324_SI.txt, email_324_BL.txt

| Field | SI | BL |
| --- | --- | --- |
| ❌ shipper | ASIA PACIFIC PAPERBOARD TRADING PTE LTD / 80 RAFFLES PLACE, #50-01 UOB PLAZA 1;  | APRIL FAR EAST (M) SDN BHD / 80 RAFFLES PLACE, #50-01 UOB PLAZA 1; SINGAPORE 048 |
|    consignee | CLIFFORD PAPER INC / 70 EAST STREET; RIDGEFIELD, NJ 07657, USA | CLIFFORD PAPER INC / 70 EAST STREET; RIDGEFIELD, NJ 07657, USA |
|    notify_party | CLIFFORD PAPER INC | CLIFFORD PAPER INC |
|    port_of_loading | BUATAN, INDONESIA (IDBUA) | BUATAN, INDONESIA (IDBUA) |
|    port_of_discharge | NEW YORK, US (USNYC) | NEW YORK, US (USNYC) |
| ❌ container_count | 3 | 4 |
|    gross_weight_kg | 60258.0 | 60258.0 |

### email_334 — MISMATCH

- Docs: email_334_SI.txt, email_334_BL.txt

| Field | SI | BL |
| --- | --- | --- |
| ❌ shipper | ASIA PACIFIC PAPERBOARD TRADING PTE LTD / 80 RAFFLES PLACE, #50-01 UOB PLAZA 1;  | APRIL FINE PAPER TRADING / 80 RAFFLES PLACE, #50-01 UOB PLAZA 1; SINGAPORE 04862 |
| ❌ consignee | EAST BRIGHT FZ-LLC / RAKEZ AMENITY CENTER; AL HAMRA INDUSTRIAL ZONE, RAK, UAE | INTERNATIONAL FOREST PRODUCTS LLC / RAKEZ AMENITY CENTER; AL HAMRA INDUSTRIAL ZO |
|    notify_party | EAST BRIGHT FZ-LLC | EAST BRIGHT FZ-LLC |
|    port_of_loading | SINGAPORE (SGSIN) | SINGAPORE (SGSIN) |
|    port_of_discharge | YANGON, MYANMAR (MMRGN) | YANGON, MYANMAR (MMRGN) |
|    container_count | 6 | 6 |
|    gross_weight_kg | 127692.0 | 127692.0 |

### email_335 — OK

- Docs: email_335_SI.txt, email_335_BL.txt
- All 7 fields match SI vs BL.
### email_342 — MISMATCH

- Docs: email_342_SI.txt, email_342_BL.txt

| Field | SI | BL |
| --- | --- | --- |
|    shipper | APRIL FINE PAPER TRADING / ON BEHALF OF VITAL SOLUTIONS PTE LTD; 77 ROBINSON ROA | APRIL FINE PAPER TRADING / ON BEHALF OF VITAL SOLUTIONS PTE LTD; 77 ROBINSON ROA |
|    consignee | MOORIM SP CO., LTD / 656, GANGNAM-DAERO, GANGNAM-GU; SEOUL, SOUTH KOREA; T. 82-2 | MOORIM SP CO., LTD / 656, GANGNAM-DAERO, GANGNAM-GU; SEOUL, SOUTH KOREA; T. 82-2 |
| ❌ notify_party | HABRAS INTERNATIONAL LIMITED | SAFQA LIMITED |
|    port_of_loading | NHAVA SHEVA, INDIA (INNSA) | NHAVA SHEVA, INDIA (INNSA) |
|    port_of_discharge | AQABA, JORDAN (JOAQB) | AQABA, JORDAN (JOAQB) |
| ❌ container_count | 1 | 2 |
|    gross_weight_kg | 23794.0 | 23794.0 |

### email_348 — OK

- Docs: email_348_SI.txt, email_348_BL.txt
- All 7 fields match SI vs BL.
### email_349 — OK

- Docs: email_349_SI.txt, email_349_BL.txt
- All 7 fields match SI vs BL.
### email_351 — MISMATCH

- Docs: email_351_SI.pdf, email_351_BL.pdf

| Field | SI | BL |
| --- | --- | --- |
|    shipper | APRIL FINE PAPER TRADING (MIDDLE EAST) FZE / #813, 4 EA, DUBAI AIRPORT FREE ZONE | APRIL FINE PAPER TRADING (MIDDLE EAST) FZE / #813, 4 EA, DUBAI AIRPORT FREE ZONE |
|    consignee | KTP CO., LTD / KTP BLDG., 36 SANGWON-GIL / SEOUNGDONG-GU, SEOUL, SOUTH KOREA / T | KTP CO., LTD / KTP BLDG., 36 SANGWON-GIL / SEOUNGDONG-GU, SEOUL, SOUTH KOREA / T |
|    notify_party | KTP CO., LTD / KTP BLDG., 36 SANGWON-GIL / SEOUNGDONG-GU, SEOUL, SOUTH KOREA / T | KTP CO., LTD / KTP BLDG., 36 SANGWON-GIL / SEOUNGDONG-GU, SEOUL, SOUTH KOREA / T |
|    port_of_loading | PORT KLANG (WESTPORT), MALAYSIA | PORT KLANG (WESTPORT), MALAYSIA |
|    port_of_discharge | ASHDOD, ISRAEL | ASHDOD, ISRAEL |
| ❌ container_count | 15 | 16 |
| ❌ gross_weight_kg | 359415.0 | 360415.0 |

### email_354 — MISMATCH

- Docs: email_354_SI.xlsx, email_354_BL.docx

| Field | SI | BL |
| --- | --- | --- |
|    shipper | APRIL FINE PAPER TRADING | ON BEHALF OF VITAL SOLUTIONS PTE LTD; 77 ROBINSON ROA | APRIL FINE PAPER TRADING / ON BEHALF OF VITAL SOLUTIONS PTE LTD / 77 ROBINSON RO |
|    consignee | HABRAS INTERNATIONAL LIMITED | OFFICE 1204, THE BURLINGTON TOWER; BUSINESS BAY,  | HABRAS INTERNATIONAL LIMITED / OFFICE 1204, THE BURLINGTON TOWER / BUSINESS BAY, |
| ❌ notify_party | HABRAS INTERNATIONAL LIMITED | OFFICE 1204, THE BURLINGTON TOWER; BUSINESS BAY,  | NAGAPPA EXPORTS / OFFICE 1204, THE BURLINGTON TOWER / BUSINESS BAY, DUBAI, UAE |
|    port_of_loading | RUGAO/NANTONG/SHANGHAI, CHINA | RUGAO/NANTONG/SHANGHAI, CHINA |
|    port_of_discharge | VALPARAISO, CHILE | VALPARAISO, CHILE |
|    container_count | 1 | 1 |
| ❌ gross_weight_kg | 20603.0 | 22603.0 |

### email_361 — MISMATCH

- Docs: email_361_SI.txt, email_361_BL.txt

| Field | SI | BL |
| --- | --- | --- |
|    shipper | APRIL FINE PAPER TRADING (MIDDLE EAST) FZE / #813, 4 EA, DUBAI AIRPORT FREE ZONE | APRIL FINE PAPER TRADING (MIDDLE EAST) FZE / #813, 4 EA, DUBAI AIRPORT FREE ZONE |
|    consignee | PACIFIC OFFICE (M) SDN BHD / LOT 6, JALAN P/7; SECTION 13, 43650 BANDAR BARU BAN | PACIFIC OFFICE (M) SDN BHD / LOT 6, JALAN P/7; SECTION 13, 43650 BANDAR BARU BAN |
|    notify_party | ROXCEL TRADING GMBH | ROXCEL TRADING GMBH |
|    port_of_loading | PORT KLANG (WESTPORT), MALAYSIA (MYPKG) | PORT KLANG (WESTPORT), MALAYSIA (MYPKG) |
| ❌ port_of_discharge | BRISBANE, AUSTRALIA (AUBNE) | MOMBASA, KENYA (AUBNE) |
|    container_count | 10 | 10 |
| ❌ gross_weight_kg | 239590.0 | 238590.0 |

### email_364 — OK

- Docs: email_364_SI.txt, email_364_BL.txt
- All 7 fields match SI vs BL.
### email_367 — OK

- Docs: email_367_SI.txt, email_367_BL.txt
- All 7 fields match SI vs BL.
### email_377 — OK

- Docs: email_377_SI.txt, email_377_BL.txt
- All 7 fields match SI vs BL.
### email_378 — OK

- Docs: email_378_SI.txt, email_378_BL.txt
- All 7 fields match SI vs BL.
### email_379 — MISMATCH

- Docs: email_379_SI.txt, email_379_BL.txt

| Field | SI | BL |
| --- | --- | --- |
| ❌ shipper | APRIL FAR EAST (M) SDN BHD / TOWER 2, AVENUE 5, LEVEL 6; BANGSAR SOUTH CITY, NO. | APRIL FINE PAPER TRADING / TOWER 2, AVENUE 5, LEVEL 6; BANGSAR SOUTH CITY, NO. 8 |
|    consignee | ROXCEL TRADING GMBH / OPERNRING 3-5; 1010 VIENNA, AUSTRIA | ROXCEL TRADING GMBH / OPERNRING 3-5; 1010 VIENNA, AUSTRIA |
|    notify_party | ROXCEL TRADING GMBH | ROXCEL TRADING GMBH |
|    port_of_loading | NANTONG, CHINA (CNNTG) | NANTONG, CHINA (CNNTG) |
|    port_of_discharge | HOUSTON, US (USHOU) | HOUSTON, US (USHOU) |
|    container_count | 12 | 12 |
|    gross_weight_kg | 272232.0 | 272232.0 |

### email_383 — OK

- Docs: email_383_SI.txt, email_383_BL.txt
- All 7 fields match SI vs BL.
### email_391 — OK

- Docs: email_391_SI.txt, email_391_BL.txt
- All 7 fields match SI vs BL.
### email_398 — OK

- Docs: email_398_SI.xlsx, email_398_BL.xlsx
- All 7 fields match SI vs BL.
### email_405 — OK

- Docs: email_405_SI.txt, email_405_BL.txt
- All 7 fields match SI vs BL.
### email_407 — OK

- Docs: email_407_SI.pdf, email_407_BL.pdf
- All 7 fields match SI vs BL.
### email_408 — OK

- Docs: email_408_SI.txt, email_408_BL.txt
- All 7 fields match SI vs BL.
### email_409 — OK

- Docs: email_409_SI.txt, email_409_BL.txt
- All 7 fields match SI vs BL.
### email_410 — MISMATCH

- Docs: email_410_SI.txt, email_410_BL.txt

| Field | SI | BL |
| --- | --- | --- |
|    shipper | APRIL FINE PAPER TRADING (MIDDLE EAST) FZE / #813, 4 EA, DUBAI AIRPORT FREE ZONE | APRIL FINE PAPER TRADING (MIDDLE EAST) FZE / #813, 4 EA, DUBAI AIRPORT FREE ZONE |
|    consignee | PACIFIC OFFICE (M) SDN BHD / LOT 6, JALAN P/7; SECTION 13, 43650 BANDAR BARU BAN | PACIFIC OFFICE (M) SDN BHD / LOT 6, JALAN P/7; SECTION 13, 43650 BANDAR BARU BAN |
|    notify_party | PACIFIC OFFICE (M) SDN BHD | PACIFIC OFFICE (M) SDN BHD |
| ❌ port_of_loading | SINGAPORE (SGSIN) | PORT KLANG (WESTPORT), MALAYSIA (SGSIN) |
|    port_of_discharge | ASHDOD, ISRAEL (ILASH) | ASHDOD, ISRAEL (ILASH) |
|    container_count | 15 | 15 |
|    gross_weight_kg | 324210.0 | 324210.0 |

### email_411 — OK

- Docs: email_411_SI.pdf, email_411_BL.pdf
- All 7 fields match SI vs BL.
### email_416 — MISMATCH

- Docs: email_416_SI.txt, email_416_BL.txt

| Field | SI | BL |
| --- | --- | --- |
|    shipper | ASIA PACIFIC PAPERBOARD TRADING PTE LTD / 80 RAFFLES PLACE, #50-01 UOB PLAZA 1;  | ASIA PACIFIC PAPERBOARD TRADING PTE LTD / 80 RAFFLES PLACE, #50-01 UOB PLAZA 1;  |
|    consignee | VITAL SOLUTIONS PTE. LTD. / 77 ROBINSON ROAD; #21-01 ROBINSON 77; SINGAPORE 0688 | VITAL SOLUTIONS PTE. LTD. / 77 ROBINSON ROAD; #21-01 ROBINSON 77; SINGAPORE 0688 |
|    notify_party | VITAL SOLUTIONS PTE. LTD. | VITAL SOLUTIONS PTE. LTD. |
|    port_of_loading | PORT KLANG (WESTPORT), MALAYSIA (MYPKG) | PORT KLANG (WESTPORT), MALAYSIA (MYPKG) |
|    port_of_discharge | LONG BEACH, US (USLGB) | LONG BEACH, US (USLGB) |
|    container_count | 5 | 5 |
| ❌ gross_weight_kg | 105625.0 | 106625.0 |

### email_426 — MISMATCH

- Docs: email_426_SI.txt, email_426_BL.txt

| Field | SI | BL |
| --- | --- | --- |
|    shipper | APRIL FINE PAPER TRADING / ON BEHALF OF VITAL SOLUTIONS PTE LTD; 77 ROBINSON ROA | APRIL FINE PAPER TRADING / ON BEHALF OF VITAL SOLUTIONS PTE LTD; 77 ROBINSON ROA |
|    consignee | KTP CO., LTD / KTP BLDG., 36 SANGWON-GIL; SEOUNGDONG-GU, SEOUL, SOUTH KOREA; TEL | KTP CO., LTD / KTP BLDG., 36 SANGWON-GIL; SEOUNGDONG-GU, SEOUL, SOUTH KOREA; TEL |
|    notify_party | PACIFIC OFFICE (M) SDN BHD | PACIFIC OFFICE (M) SDN BHD |
|    port_of_loading | BUATAN, INDONESIA (IDBUA) | BUATAN, INDONESIA (IDBUA) |
| ❌ port_of_discharge | NEW YORK, US (USNYC) | KLAIPEDA, LITHUANIA (USNYC) |
| ❌ container_count | 10 | 11 |
|    gross_weight_kg | 219740.0 | 219740.0 |

### email_428 — OK

- Docs: email_428_SI.txt, email_428_BL.txt
- All 7 fields match SI vs BL.
### email_434 — MISMATCH

- Docs: email_434_SI.pdf, email_434_BL.pdf

| Field | SI | BL |
| --- | --- | --- |
|    shipper | APRIL FINE PAPER TRADING (MIDDLE EAST) FZE / #813, 4 EA, DUBAI AIRPORT FREE ZONE | APRIL FINE PAPER TRADING (MIDDLE EAST) FZE / #813, 4 EA, DUBAI AIRPORT FREE ZONE |
|    consignee | TOPKOPY MIDDLE EAST FZE / P.O. BOX 17436 / JEBEL ALI FREE ZONE, DUBAI, UAE | TOPKOPY MIDDLE EAST FZE / P.O. BOX 17436 / JEBEL ALI FREE ZONE, DUBAI, UAE |
|    notify_party | TOPKOPY MIDDLE EAST FZE / P.O. BOX 17436 / JEBEL ALI FREE ZONE, DUBAI, UAE | TOPKOPY MIDDLE EAST FZE / P.O. BOX 17436 / JEBEL ALI FREE ZONE, DUBAI, UAE |
|    port_of_loading | NHAVA SHEVA, INDIA | NHAVA SHEVA, INDIA |
| ❌ port_of_discharge | BUSAN, SOUTH KOREA | CEBU, PHILIPPINES |
|    container_count | 12 | 12 |
|    gross_weight_kg | 261480.0 | 261480.0 |

### email_435 — MISMATCH

- Docs: email_435_SI.xlsx, email_435_BL.docx

| Field | SI | BL |
| --- | --- | --- |
|    shipper | APRIL FINE PAPER TRADING (MIDDLE EAST) FZE | #813, 4 EA, DUBAI AIRPORT FREE ZONE | APRIL FINE PAPER TRADING (MIDDLE EAST) FZE / #813, 4 EA, DUBAI AIRPORT FREE ZONE |
|    consignee | AL GURG STATIONERY LLC | P.O. BOX 5069; DUBAI, UNITED ARAB EMIRATES | AL GURG STATIONERY LLC / P.O. BOX 5069 / DUBAI, UNITED ARAB EMIRATES |
|    notify_party | AL GURG STATIONERY LLC | P.O. BOX 5069; DUBAI, UNITED ARAB EMIRATES | AL GURG STATIONERY LLC / P.O. BOX 5069 / DUBAI, UNITED ARAB EMIRATES |
|    port_of_loading | SINGAPORE | SINGAPORE |
|    port_of_discharge | AQABA, JORDAN | AQABA, JORDAN |
|    container_count | 10 | 10 |
| ❌ gross_weight_kg | 214270.0 | 214770.0 |

### email_453 — OK

- Docs: email_453_SI.txt, email_453_BL.txt
- All 7 fields match SI vs BL.
### email_462 — OK

- Docs: email_462_SI.xlsx, email_462_BL.docx
- All 7 fields match SI vs BL.
### email_468 — MISMATCH

- Docs: email_468_SI.txt, email_468_BL.txt

| Field | SI | BL |
| --- | --- | --- |
|    shipper | ASIA PACIFIC PAPERBOARD TRADING PTE LTD / 80 RAFFLES PLACE, #50-01 UOB PLAZA 1;  | ASIA PACIFIC PAPERBOARD TRADING PTE LTD / 80 RAFFLES PLACE, #50-01 UOB PLAZA 1;  |
|    consignee | ROXCEL TRADING GMBH / OPERNRING 3-5; 1010 VIENNA, AUSTRIA | ROXCEL TRADING GMBH / OPERNRING 3-5; 1010 VIENNA, AUSTRIA |
|    notify_party | ROXCEL TRADING GMBH | ROXCEL TRADING GMBH |
| ❌ port_of_loading | SINGAPORE (SGSIN) | RUGAO/NANTONG/SHANGHAI, CHINA (SGSIN) |
|    port_of_discharge | ASHDOD, ISRAEL (ILASH) | ASHDOD, ISRAEL (ILASH) |
| ❌ container_count | 1 | 3 |
|    gross_weight_kg | 20456.0 | 20456.0 |

### email_474 — OK

- Docs: email_474_SI.txt, email_474_BL.txt
- All 7 fields match SI vs BL.
### email_479 — OK

- Docs: email_479_SI.txt, email_479_BL.txt
- All 7 fields match SI vs BL.
### email_481 — MISMATCH

- Docs: email_481_SI.xlsx, email_481_BL.xlsx

| Field | SI | BL |
| --- | --- | --- |
|    shipper | APRIL FAR EAST (M) SDN BHD | TOWER 2, AVENUE 5, LEVEL 6; BANGSAR SOUTH CITY, NO. | APRIL FAR EAST (M) SDN BHD | TOWER 2, AVENUE 5, LEVEL 6; BANGSAR SOUTH CITY, NO. |
| ❌ consignee | AL GURG STATIONERY LLC | P.O. BOX 5069; DUBAI, UNITED ARAB EMIRATES | 3S PAPER PRODUCTS SDN BHD | P.O. BOX 5069; DUBAI, UNITED ARAB EMIRATES |
|    notify_party | SAFQA LIMITED | P.O. BOX 99423-80100; TONONOKA ROAD; MOMBASA, KENYA; PIN NO.: P0 | SAFQA LIMITED | P.O. BOX 99423-80100; TONONOKA ROAD; MOMBASA, KENYA; PIN NO.: P0 |
|    port_of_loading | RUGAO/NANTONG/SHANGHAI, CHINA | RUGAO/NANTONG/SHANGHAI, CHINA |
|    port_of_discharge | VALPARAISO, CHILE | VALPARAISO, CHILE |
|    container_count | 4 | 4 |
|    gross_weight_kg | 91436.0 | 91436.0 |

### email_483 — OK

- Docs: email_483_SI.txt, email_483_BL.txt
- All 7 fields match SI vs BL.
### email_491 — OK

- Docs: email_491_SI.txt, email_491_BL.txt
- All 7 fields match SI vs BL.
### email_494 — OK

- Docs: email_494_SI.txt, email_494_BL.txt
- All 7 fields match SI vs BL.
### email_496 — OK

- Docs: email_496_SI.xlsx, email_496_BL.xlsx
- All 7 fields match SI vs BL.
### email_498 — OK

- Docs: email_498_SI.txt, email_498_BL.txt
- All 7 fields match SI vs BL.
### email_499 — MISMATCH

- Docs: email_499_SI.pdf, email_499_BL.pdf

| Field | SI | BL |
| --- | --- | --- |
|    shipper | APRIL FINE PAPER TRADING (MIDDLE EAST) FZE / #813, 4 EA, DUBAI AIRPORT FREE ZONE | APRIL FINE PAPER TRADING (MIDDLE EAST) FZE / #813, 4 EA, DUBAI AIRPORT FREE ZONE |
|    consignee | TOPKOPY MIDDLE EAST FZE / P.O. BOX 17436 / JEBEL ALI FREE ZONE, DUBAI, UAE | TOPKOPY MIDDLE EAST FZE / P.O. BOX 17436 / JEBEL ALI FREE ZONE, DUBAI, UAE |
|    notify_party | TOPKOPY MIDDLE EAST FZE / P.O. BOX 17436 / JEBEL ALI FREE ZONE, DUBAI, UAE | TOPKOPY MIDDLE EAST FZE / P.O. BOX 17436 / JEBEL ALI FREE ZONE, DUBAI, UAE |
|    port_of_loading | PORT KLANG (WESTPORT), MALAYSIA | PORT KLANG (WESTPORT), MALAYSIA |
|    port_of_discharge | HOCHIMINH CITY, VIETNAM | HOCHIMINH CITY, VIETNAM |
|    container_count | 2 | 2 |
| ❌ gross_weight_kg | 40326.0 | 41326.0 |

### email_501 — NEEDS_REVIEW — wrong_doc_type

- Docs: email_501_SI.txt, email_501_BL.txt

| Field | SI | BL |
| --- | --- | --- |
|    shipper | — | — |
|    consignee | — | — |
|    notify_party | — | — |
|    port_of_loading | — | — |
|    port_of_discharge | — | — |
|    container_count | — | — |
|    gross_weight_kg | — | — |

### email_502 — NEEDS_REVIEW — wrong_doc_type

- Docs: email_502_SI.txt, email_502_BL.txt

| Field | SI | BL |
| --- | --- | --- |
|    shipper | — | — |
|    consignee | — | — |
|    notify_party | — | — |
|    port_of_loading | — | — |
|    port_of_discharge | — | — |
|    container_count | — | — |
|    gross_weight_kg | — | — |

### email_503 — NEEDS_REVIEW — wrong_doc_type

- Docs: email_503_SI.txt, email_503_BL.txt

| Field | SI | BL |
| --- | --- | --- |
|    shipper | — | — |
|    consignee | — | — |
|    notify_party | — | — |
|    port_of_loading | — | — |
|    port_of_discharge | — | — |
|    container_count | — | — |
|    gross_weight_kg | — | — |

### email_504 — NEEDS_REVIEW — wrong_doc_type

- Docs: email_504_SI.txt, email_504_BL.txt

| Field | SI | BL |
| --- | --- | --- |
|    shipper | — | — |
|    consignee | — | — |
|    notify_party | — | — |
|    port_of_loading | — | — |
|    port_of_discharge | — | — |
|    container_count | — | — |
|    gross_weight_kg | — | — |

### email_505 — NEEDS_REVIEW — wrong_doc_type

- Docs: email_505_SI.txt, email_505_BL.txt

| Field | SI | BL |
| --- | --- | --- |
|    shipper | — | — |
|    consignee | — | — |
|    notify_party | — | — |
|    port_of_loading | — | — |
|    port_of_discharge | — | — |
|    container_count | — | — |
|    gross_weight_kg | — | — |

### email_506 — NEEDS_REVIEW — missing_attachment

- Docs: 

| Field | SI | BL |
| --- | --- | --- |
|    shipper | — | — |
|    consignee | — | — |
|    notify_party | — | — |
|    port_of_loading | — | — |
|    port_of_discharge | — | — |
|    container_count | — | — |
|    gross_weight_kg | — | — |

### email_507 — NEEDS_REVIEW — missing_attachment

- Docs: 

| Field | SI | BL |
| --- | --- | --- |
|    shipper | — | — |
|    consignee | — | — |
|    notify_party | — | — |
|    port_of_loading | — | — |
|    port_of_discharge | — | — |
|    container_count | — | — |
|    gross_weight_kg | — | — |

### email_508 — NEEDS_REVIEW — missing_attachment

- Docs: 

| Field | SI | BL |
| --- | --- | --- |
|    shipper | — | — |
|    consignee | — | — |
|    notify_party | — | — |
|    port_of_loading | — | — |
|    port_of_discharge | — | — |
|    container_count | — | — |
|    gross_weight_kg | — | — |

### email_509 — NEEDS_REVIEW — missing_attachment

- Docs: 

| Field | SI | BL |
| --- | --- | --- |
|    shipper | — | — |
|    consignee | — | — |
|    notify_party | — | — |
|    port_of_loading | — | — |
|    port_of_discharge | — | — |
|    container_count | — | — |
|    gross_weight_kg | — | — |

### email_510 — NEEDS_REVIEW — missing_attachment

- Docs: 

| Field | SI | BL |
| --- | --- | --- |
|    shipper | — | — |
|    consignee | — | — |
|    notify_party | — | — |
|    port_of_loading | — | — |
|    port_of_discharge | — | — |
|    container_count | — | — |
|    gross_weight_kg | — | — |

### email_511 — NEEDS_REVIEW — unreadable

- Docs: email_511_SI.txt, email_511_BL.pdf

| Field | SI | BL |
| --- | --- | --- |
|    shipper | — | — |
|    consignee | — | — |
|    notify_party | — | — |
|    port_of_loading | — | — |
|    port_of_discharge | — | — |
|    container_count | — | — |
|    gross_weight_kg | — | — |

### email_512 — NEEDS_REVIEW — unreadable

- Docs: email_512_SI.pdf, email_512_BL.pdf

| Field | SI | BL |
| --- | --- | --- |
|    shipper | — | — |
|    consignee | — | — |
|    notify_party | — | — |
|    port_of_loading | — | — |
|    port_of_discharge | — | — |
|    container_count | — | — |
|    gross_weight_kg | — | — |

### email_513 — NEEDS_REVIEW — unreadable

- Docs: email_513_SI.pdf, email_513_BL.pdf

| Field | SI | BL |
| --- | --- | --- |
|    shipper | — | — |
|    consignee | — | — |
|    notify_party | — | — |
|    port_of_loading | — | — |
|    port_of_discharge | — | — |
|    container_count | — | — |
|    gross_weight_kg | — | — |

### email_514 — NEEDS_REVIEW — unreadable

- Docs: email_514_SI.pdf, email_514_BL.pdf

| Field | SI | BL |
| --- | --- | --- |
|    shipper | — | — |
|    consignee | — | — |
|    notify_party | — | — |
|    port_of_loading | — | — |
|    port_of_discharge | — | — |
|    container_count | — | — |
|    gross_weight_kg | — | — |

### email_515 — NEEDS_REVIEW — unreadable

- Docs: email_515_SI.txt, email_515_BL.pdf

| Field | SI | BL |
| --- | --- | --- |
|    shipper | — | — |
|    consignee | — | — |
|    notify_party | — | — |
|    port_of_loading | — | — |
|    port_of_discharge | — | — |
|    container_count | — | — |
|    gross_weight_kg | — | — |

### email_516 — MISMATCH

- Docs: email_516_SI.txt, email_516_BL.txt

| Field | SI | BL |
| --- | --- | --- |
| ❌ shipper | APRIL FINE PAPER TRADING | APRIL FINE PAPER TRADING / ON BEHALF OF VITAL SOLUTIONS PTE LTD; 77 ROBINSON ROA |
| ❌ consignee | KPP-ANTALIS (SINGAPORE) PTE. LTD. | KPP-ANTALIS (SINGAPORE) PTE. LTD. / 8 TEMASEK BOULEVARD; #42-01 SUNTEC TOWER 3;  |
|    notify_party | KPP-ANTALIS (SINGAPORE) PTE. LTD. | KPP-ANTALIS (SINGAPORE) PTE. LTD. |
|    port_of_loading | NHAVA SHEVA, INDIA | NHAVA SHEVA, INDIA (INNSA) |
|    port_of_discharge | CONAKRY, GUINEA | CONAKRY, GUINEA (GNCKY) |
|    container_count | 10 | 10 |
|    gross_weight_kg | — | 235550.0 |

### email_517 — MISMATCH

- Docs: email_517_SI.txt, email_517_BL.txt

| Field | SI | BL |
| --- | --- | --- |
| ❌ shipper | APRIL FAR EAST (M) SDN BHD | APRIL FAR EAST (M) SDN BHD / TOWER 2, AVENUE 5, LEVEL 6; BANGSAR SOUTH CITY, NO. |
| ❌ consignee | BALL & DOGGETT AUSTRALIA PTY LTD | BALL & DOGGETT AUSTRALIA PTY LTD / 43-45 METROPOLITAN ROAD; ENFIELD NSW 2136, AU |
|    notify_party | BALL & DOGGETT AUSTRALIA PTY LTD | BALL & DOGGETT AUSTRALIA PTY LTD |
| ❌ port_of_loading | MT | SINGAPORE (SGSIN) |
| ❌ port_of_discharge | TBA | CALLAO, PERU (PECLL) |
|    container_count | 15 | 15 |
|    gross_weight_kg | 340770.0 | 340770.0 |

### email_518 — MISMATCH

- Docs: email_518_SI.txt, email_518_BL.txt

| Field | SI | BL |
| --- | --- | --- |
| ❌ shipper | APRIL FINE PAPER TRADING | APRIL FINE PAPER TRADING / ON BEHALF OF VITAL SOLUTIONS PTE LTD; 77 ROBINSON ROA |
| ❌ consignee | MOORIM SP CO., LTD | MOORIM SP CO., LTD / 656, GANGNAM-DAERO, GANGNAM-GU; SEOUL, SOUTH KOREA; T. 82-2 |
|    notify_party | MOORIM SP CO., LTD | MOORIM SP CO., LTD |
|    port_of_loading | NANTONG, CHINA | NANTONG, CHINA (CNNTG) |
|    port_of_discharge | — | APAPA, NIGERIA (NGAPP) |
|    container_count | 6 | 6 |
|    gross_weight_kg | — | 134586.0 |

### email_519 — MISMATCH

- Docs: email_519_SI.txt, email_519_BL.txt

| Field | SI | BL |
| --- | --- | --- |
|    shipper | — | ASIA PACIFIC PAPERBOARD TRADING PTE LTD / 80 RAFFLES PLACE, #50-01 UOB PLAZA 1;  |
| ❌ consignee | UAB NOVAKOPA | UAB NOVAKOPA / SAVANORIU PR. 187; LT-02300 VILNIUS, LITHUANIA |
|    notify_party | UAB NOVAKOPA | UAB NOVAKOPA |
|    port_of_loading | BUATAN, INDONESIA | BUATAN, INDONESIA (IDBUA) |
|    port_of_discharge | BUSAN, SOUTH KOREA | BUSAN, SOUTH KOREA (KRPUS) |
|    container_count | — | 3 |
|    gross_weight_kg | 70572.0 | 70572.0 |

### email_520 — MISMATCH

- Docs: email_520_SI.txt, email_520_BL.txt

| Field | SI | BL |
| --- | --- | --- |
| ❌ shipper | APRIL FINE PAPER TRADING | APRIL FINE PAPER TRADING / ON BEHALF OF VITAL SOLUTIONS PTE LTD; 77 ROBINSON ROA |
|    consignee | — | CLIFFORD PAPER INC / 70 EAST STREET; RIDGEFIELD, NJ 07657, USA |
|    notify_party | CLIFFORD PAPER INC | CLIFFORD PAPER INC |
|    port_of_loading | SINGAPORE | SINGAPORE (SGSIN) |
|    port_of_discharge | PYEONGTAEK, SOUTH KOREA | PYEONGTAEK, SOUTH KOREA (KRPTK) |
|    container_count | 6 | 6 |
|    gross_weight_kg | 122640.0 | 122640.0 |
