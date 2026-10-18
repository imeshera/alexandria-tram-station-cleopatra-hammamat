# Sources

No third-party image is included in this repository. The reference images (owner's photos, video frames,
satellite crops, web thumbnails) were used for personal modelling reference only; the CSV manifests in
[`manifests/`](manifests/) list every file with its source, author and licence so they can be re-fetched.

## Owner's photos
Six iPhone 14 Pro Max photos (Ibrahim Eshera, 12 March 2026, around midnight), taken from the trackbed about 8.6 m
north-east of the SW colonnade, looking SSW along the platform. Used for the v0 photogrammetry (rail-gauge ground
plane, EXIF intrinsics) and the module count. Kept local; not published. Manifest without GPS/time:
[`manifests/owner-photos.csv`](manifests/owner-photos.csv).

## YouTube (frames grabbed for reference; videos cited by ID, not embedded)
| Channel | Video ID | Date | What it gave |
|---|---|---|---|
| Amr Veto | `01YNkcHynps` (t13m17–t13m25) | 2024-06 | Route-1 car passing the NE colonnade: canopy count (7), frame count (8), drum position, side-on dome silhouettes |
| Amr Veto | `hBRSKXDcvPw` (t21m02–t21m09) | 2024-06 | Opposite direction, SW colonnade: same layout, balustrade and benches, standing passengers for scale |
| ahmed salah (@ahmedsalah1145) | `3nKi0T8XbfM` | 2024-07 | "Cleopatra Grand Hammamet Tram Station 2024": Raml cars at the platform (car 175, DD 218), platform paving, column plinths |
| Tram El Raml (ترام الرمل) | `5VrK_jv34yY` | 2025-07 | From the upper deck of a double-deck car: dome tops and the two-tier unit |
| Am El Sayed El Masry (عم السيد المصري) | `hYF1ttlnHgU` | 2022-10 | Capital, bench and balustrade close-up |
| Tram El Raml (ترام الرمل) | `6IYrhhEwTqE` | 2026-05 | Along-platform views under the colonnade: transverse frames, column spacing |
| Hekayat Moug El Bahr (حكايات موج البحر) | `7QD9XvKRADc`, `dTKsyEO6TQo` | 2026-04/05 | Weed-grown track, capitals, soffits, platform paving |
| Hekayat Moug El Bahr (حكايات موج البحر) | `uDaakU1MMQ8`, `U0pAlyOq3yQ` | 2026-09 | Rails lifted; demolition in progress |
| Hekayat Moug El Bahr (حكايات موج البحر) | `LjFTTQorR9o` (t05m54–t07m32) | 2026-09 | Best daylight detail: cartouche text, drum plaque "كليوباترا", frames from below, arcade of canopies |
| Yasser Hayrouh Fein (ياسر هيروح فين) | `Wi4t1OngdrE` (t03m36) | 2026-09 | Broken canopy: RC shell thickness and rebar cage, balustrade piers |
| Shawarea Masr ma3 Mina (شوارع مصر مع مينا) | `9-zDQpju3g8` | 2026-10 | Abandoned loop; a colonnade still standing in early October |

Full frame list with timestamps: [`manifests/youtube-frames.csv`](manifests/youtube-frames.csv).

## Maps, imagery and documents
- **Esri World Imagery** (Maxar, Earthstar Geographics), zoom 19 around 31.22130 N, 29.93789 E: the two colonnades,
  their lengths and the street layout. © Esri and its data providers; personal reference only.
- **OpenStreetMap** (© OpenStreetMap contributors, ODbL): stop node 4748507684 "Cleopatra El Kobra Station",
  level-crossing nodes on Sidi Gaber Street.
- **Raml Tram ESIA** (NAT / EcoConServ, Rev.0, 2022; EIB register document 159793226), §5.2.4.2 "Removal of Sidi
  Gaber Loop": the northern branch with this station is eliminated.
- **aaha.ch** "trams-ramleh-cleopatra" page (Swiss Alexandria heritage site), five thumbnails of the colonnade,
  pre-2024: [`manifests/web-images.csv`](manifests/web-images.csv).
- Research dossier for this station (identification, history, status, v0 photogrammetry), kept with the reference
  images; the parts used here are summarised in [`notes/dimensions.md`](notes/dimensions.md).

## Related models (same author)
Raml cars used for scale: `alexandria-tram-raml-221-223` (single-deck car dimensions) and
`alexandria-tram-raml-dd-224` (double-deck height 4.80 m).
