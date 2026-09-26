#!/usr/bin/env python3
"""Generate research/index.qmd in en, es, eu for the personal site from one data set.
Sources: 2020 full CV (cv_main.pdf), large-facility cost memo, EHU project
certificates 2013/2015/2019, 2022 abbreviated CV, 2026 CV (already on the page)."""
import pathlib, yaml, html

ROOT = pathlib.Path(__file__).resolve().parent.parent
L = ("en", "es", "eu")

# ---------------------------------------------------------------- strings
T = {
"title": ("Research", "Investigación", "Ikerketa"),
"desc": (
 "Five research lines since 1988, the experiments at European large facilities, the competitive projects and research groups, and the contracts with industry.",
 "Cinco líneas de investigación desde 1988, los experimentos en grandes instalaciones europeas, los proyectos competitivos y grupos de investigación, y los contratos con la industria.",
 "Bost ikerketa-lerro 1988tik, Europako instalazio handietako esperimentuak, proiektu lehiakorrak eta ikerketa-taldeak, eta industriarekiko kontratuak."),
"crumb": ("research", "investigación", "ikerketa"),
"sub": (
 "Five lines in thirty-eight years, from adiabatic calorimetry to infrared emissivity. They share a habit: let the data decide the symmetry, and keep the computation reproducible.",
 "Cinco líneas en treinta y ocho años, de la calorimetría adiabática a la emisividad infrarroja. Comparten una costumbre: que los datos decidan la simetría, y que el cálculo sea reproducible.",
 "Bost lerro hogeita hemezortzi urtetan, kalorimetria adiabatikotik emisibitate infragorrira. Ohitura bera dute: datuek erabaki dezatela simetria, eta konputazioa erreproduzigarri mantendu."),
"intro": (
 "My research began in 1988 in the adiabatic calorimetry laboratory of the Faculty of Science, grew into the crystallography of perovskite oxides through the Bilbao Crystallographic Server and the European neutron and synchrotron sources, and since 2018 lives in the Thermomat group, which I co-lead, around the HAIRL emissometer. What follows is the record: the lines, the experiments at large facilities, the projects and groups that paid for them, and the contracts with industry. The publications are on [their own page](../publications/index.html), generated from a registry synchronised with OpenAlex.",
 "Mi investigación empezó en 1988 en el laboratorio de calorimetría adiabática de la Facultad de Ciencias, creció hacia la cristalografía de los óxidos con estructura de perovskita a través del Bilbao Crystallographic Server y de las fuentes europeas de neutrones y sincrotrón, y desde 2018 vive en el grupo Thermomat, que codirijo, alrededor del emisómetro HAIRL. Lo que sigue es el registro: las líneas, los experimentos en grandes instalaciones, los proyectos y grupos que los pagaron, y los contratos con la industria. Las publicaciones están en [su propia página](../publications/index.html), generada a partir de un registro sincronizado con OpenAlex.",
 "Nire ikerketa 1988an hasi zen Zientzia Fakultateko kalorimetria adiabatikoko laborategian, perobskita motako oxidoen kristalografiarantz hazi zen Bilbao Crystallographic Server-aren eta Europako neutroi- eta sinkrotroi-iturrien bidez, eta 2018tik Thermomat taldean bizi da, nik ko-zuzentzen dudana, HAIRL emisometroaren inguruan. Hona hemen erregistroa: lerroak, instalazio handietako esperimentuak, horiek ordaindu zituzten proiektuak eta taldeak, eta industriarekiko kontratuak. Argitalpenak [beren orrian](../publications/index.html) daude, OpenAlexekin sinkronizatutako erregistro batetik sortuak."),

"h_calo": ("Adiabatic calorimetry and structural phase transitions (1988–1995)",
           "Calorimetría adiabática y transiciones de fase estructurales (1988–1995)",
           "Kalorimetria adiabatikoa eta egiturazko fase-trantsizioak (1988–1995)"),
"p_calo": (
 "My doctoral work, with Ángel López-Echarri and Isabel Ruiz-Larrea, was on the solid–solid phase transitions of ferroic, ferroelastic and incommensurate crystals measured by adiabatic calorimetry: [N(CH₃)₄]₂ZnBr₄ and [N(CH₃)₄]₂ZnI₄, thiourea, betaine calcium chloride dihydrate, N(CH₃)₄CdBr₃, Cs₂ZnI₄ and Cs₂CdBr₄. The instrument was an automatic adiabatic calorimeter working between 20 and 370 K, built and programmed in the laboratory. The method separated the harmonic and anharmonic lattice contributions with Raman, elastic and thermal-expansion data, so that the entropy of each transition could be assigned without ambiguity and the order–disorder or displacive character settled. Stays at the University of Bordeaux with Michel Couzi added the Raman side. The results appeared in *physica status solidi (b)*, *Thermochimica Acta*, *Solid State Communications*, *Physical Review B*, *Phase Transitions*, *Ferroelectrics* and *Journal of Physics: Condensed Matter*, and the thesis was defended in 1994.",
 "Mi trabajo doctoral, con Ángel López-Echarri e Isabel Ruiz-Larrea, versó sobre las transiciones de fase sólido–sólido de cristales ferroicos, ferroelásticos e inconmensurables medidas por calorimetría adiabática: [N(CH₃)₄]₂ZnBr₄ y [N(CH₃)₄]₂ZnI₄, tiourea, cloruro cálcico de betaína dihidratado, N(CH₃)₄CdBr₃, Cs₂ZnI₄ y Cs₂CdBr₄. El instrumento era un calorímetro adiabático automático entre 20 y 370 K, construido y programado en el laboratorio. El método separaba las contribuciones armónica y anarmónica de la red con datos Raman, elásticos y de dilatación térmica, de modo que la entropía de cada transición quedaba asignada sin ambigüedad y su carácter orden–desorden o desplazativo, resuelto. Varias estancias en la Universidad de Burdeos con Michel Couzi aportaron la parte Raman. Los resultados aparecieron en *physica status solidi (b)*, *Thermochimica Acta*, *Solid State Communications*, *Physical Review B*, *Phase Transitions*, *Ferroelectrics* y *Journal of Physics: Condensed Matter*, y la tesis se leyó en 1994.",
 "Nire doktorego-lana, Ángel López-Echarri eta Isabel Ruiz-Larrearekin, kristal ferroiko, ferroelastiko eta inkonmentsurableen solido–solido fase-trantsizioei buruzkoa izan zen, kalorimetria adiabatikoz neurtuak: [N(CH₃)₄]₂ZnBr₄ eta [N(CH₃)₄]₂ZnI₄, tiourea, betaina kaltzio kloruro dihidratatua, N(CH₃)₄CdBr₃, Cs₂ZnI₄ eta Cs₂CdBr₄. Tresna 20 eta 370 K artean lan egiten zuen kalorimetro adiabatiko automatiko bat zen, laborategian eraikia eta programatua. Metodoak sarearen ekarpen harmonikoa eta anharmonikoa bereizten zituen Raman, elastikotasun- eta dilatazio termikoko datuekin, trantsizio bakoitzaren entropia anbiguotasunik gabe esleitzeko eta bere ordena–desordena edo desplazamendu-izaera erabakitzeko. Bordeleko Unibertsitatean Michel Couzirekin egindako egonaldiek Raman aldea gehitu zuten. Emaitzak *physica status solidi (b)*, *Thermochimica Acta*, *Solid State Communications*, *Physical Review B*, *Phase Transitions*, *Ferroelectrics* eta *Journal of Physics: Condensed Matter* aldizkarietan argitaratu ziren, eta tesia 1994an defendatu zen."),

"h_pseudo": ("Pseudosymmetry and the prediction of phase transitions (1996–2001)",
             "Pseudosimetría y predicción de transiciones de fase (1996–2001)",
             "Pseudosimetria eta fase-trantsizioen iragarpena (1996–2001)"),
"p_pseudo": (
 "With Mois I. Aroyo and J. Manuel Pérez-Mato I developed a systematic procedure for finding pseudosymmetric structures in crystallographic databases: determine the minimal supergroups of a space group, apply their additional operations to the known structure, and measure how far the transformed structure lies from the original. A small distance reveals a slightly distorted phase of higher symmetry, and therefore a probable phase transition at higher temperature. Applied to the P2₁2₁2₁ and Pnma structures of the Inorganic Crystal Structure Database (*Physical Review B* 1996, *Acta Crystallographica B* 1999, *Ferroelectrics* 1997 and 2000), the method recovered the compounds with known transitions and proposed dozens of new candidates, including displacive ferroelectrics. It became the program PSEUDO on the Bilbao Crystallographic Server, and its logic is how the next line began: the Sr₂MWO₆ family was chosen because pseudosymmetry said it should transform.",
 "Con Mois I. Aroyo y J. Manuel Pérez-Mato desarrollé un procedimiento sistemático para encontrar estructuras pseudosimétricas en las bases de datos cristalográficas: determinar los supergrupos minimales de un grupo espacial, aplicar sus operaciones adicionales a la estructura conocida y medir cuánto se aleja la estructura transformada de la original. Una distancia pequeña revela una fase de simetría superior ligeramente distorsionada y, por tanto, una probable transición de fase a mayor temperatura. Aplicado a las estructuras P2₁2₁2₁ y Pnma de la Inorganic Crystal Structure Database (*Physical Review B* 1996, *Acta Crystallographica B* 1999, *Ferroelectrics* 1997 y 2000), el método recuperó los compuestos con transiciones conocidas y propuso decenas de candidatos nuevos, incluidos ferroeléctricos desplazativos. Se convirtió en el programa PSEUDO del Bilbao Crystallographic Server, y su lógica es el origen de la línea siguiente: la familia Sr₂MWO₆ se eligió porque la pseudosimetría decía que debía transformarse.",
 "Mois I. Aroyo eta J. Manuel Pérez-Matorekin egitura pseudosimetrikoak datu-base kristalografikoetan aurkitzeko prozedura sistematiko bat garatu nuen: talde espazial baten supertalde minimoak zehaztu, haien eragiketa gehigarriak egitura ezagunari aplikatu, eta egitura eraldatua jatorrizkotik zenbat urruntzen den neurtu. Distantzia txiki batek simetria handiagoko fase apur bat desitxuratu bat agerian uzten du, eta beraz, tenperatura altuagoan fase-trantsizio bat izateko probabilitatea. Inorganic Crystal Structure Database-ko P2₁2₁2₁ eta Pnma egiturei aplikatuta (*Physical Review B* 1996, *Acta Crystallographica B* 1999, *Ferroelectrics* 1997 eta 2000), metodoak trantsizio ezagunak zituzten konposatuak berreskuratu zituen eta dozenaka hautagai berri proposatu, ferroelektriko desplazatiboak barne. Bilbao Crystallographic Server-eko PSEUDO programa bihurtu zen, eta bere logika da hurrengo lerroaren abiapuntua: Sr₂MWO₆ familia aukeratu zen pseudosimetriak eraldatu behar zuela zioelako."),

"h_perov": ("Double perovskites and mode crystallography (2003–2019)",
            "Perovskitas dobles y cristalografía de modos (2003–2019)",
            "Perobskita bikoitzak eta moduen kristalografia (2003–2019)"),
"p_perov1": (
 "From 2003 the line settled on double and triple perovskite oxides, A₂BB′O₆ and their relatives, which distort from the ideal cubic structure through octahedral tilts, cation order and off-centre displacements, and whose magnetic, dielectric and transport properties depend on those distortions: the tungstates Sr₂MWO₆ and Ca₂MWO₆, the antimonates A₂MSbO₆ with M from scandium to the lanthanides, the ruthenates SrLnMRuO₆ and La₂NiRuO₆, the tellurates Sr₂MTeO₆ and their solid solutions, the triple perovskites ALn₂CuTi₂O₉, Na₀.₅K₀.₅NbO₃ and La₂CoMnO₆. For every family the questions were the same: the room-temperature structure and degree of cation order, the sequence of temperature-driven transitions, typically P2₁/n → I4/m → Fm3̄m or through R3̄ and I2/m, and the modes that drive them. The data came from laboratory X-rays, synchrotron radiation at the ESRF, neutrons at the ILL, SINQ, FRM II and the Helmholtz-Zentrum Berlin, high-temperature and high-pressure Raman spectroscopy with Bouchaib Manoun and Peter Lazor, and magnetic measurements.",
 "Desde 2003 la línea se asentó en los óxidos con estructura de perovskita doble y triple, A₂BB′O₆ y sus parientes, que se distorsionan respecto de la estructura cúbica ideal por giros de los octaedros, orden catiónico y desplazamientos fuera del centro, y cuyas propiedades magnéticas, dieléctricas y de transporte dependen de esas distorsiones: los wolframatos Sr₂MWO₆ y Ca₂MWO₆, los antimoniatos A₂MSbO₆ con M desde el escandio hasta los lantánidos, los rutenatos SrLnMRuO₆ y La₂NiRuO₆, los teluratos Sr₂MTeO₆ y sus disoluciones sólidas, las perovskitas triples ALn₂CuTi₂O₉, Na₀.₅K₀.₅NbO₃ y La₂CoMnO₆. Para cada familia las preguntas fueron las mismas: la estructura a temperatura ambiente y el grado de orden catiónico, la secuencia de transiciones inducidas por la temperatura, típicamente P2₁/n → I4/m → Fm3̄m o a través de R3̄ e I2/m, y los modos que las gobiernan. Los datos vinieron de rayos X de laboratorio, radiación sincrotrón en el ESRF, neutrones en el ILL, SINQ, FRM II y el Helmholtz-Zentrum Berlin, espectroscopia Raman a alta temperatura y alta presión con Bouchaib Manoun y Peter Lazor, y medidas magnéticas.",
 "2003tik lerroa perobskita bikoitz eta hirukoitz motako oxidoetan finkatu zen, A₂BB′O₆ eta beren senideak, egitura kubiko idealetik oktaedroen biraketen, katioi-ordenaren eta zentrotik kanpoko desplazamenduen bidez desitxuratzen direnak, eta zeinen propietate magnetiko, dielektriko eta garraiokoak distortsio horien mende dauden: Sr₂MWO₆ eta Ca₂MWO₆ wolframatoak, A₂MSbO₆ antimoniatoak M eskandiotik lantanidoetara, SrLnMRuO₆ eta La₂NiRuO₆ rutenatoak, Sr₂MTeO₆ teluratoak eta beren soluzio solidoak, ALn₂CuTi₂O₉ perobskita hirukoitzak, Na₀.₅K₀.₅NbO₃ eta La₂CoMnO₆. Familia bakoitzarentzat galderak berberak izan ziren: giro-tenperaturako egitura eta katioi-ordenaren maila, tenperaturak eragindako trantsizioen sekuentzia, normalean P2₁/n → I4/m → Fm3̄m edo R3̄ eta I2/m bidez, eta gidatzen dituzten moduak. Datuak laborategiko X izpietatik, ESRFko sinkrotroi-erradiaziotik, ILL, SINQ, FRM II eta Helmholtz-Zentrum Berlineko neutroietatik, Bouchaib Manoun eta Peter Lazorrekin egindako tenperatura eta presio altuko Raman espektroskopiatik eta neurketa magnetikoetatik etorri ziren."),
"p_perov2": (
 "The method that ties the work together is symmetry-mode analysis, or mode crystallography: describing a distorted structure not by atomic coordinates but by the amplitudes of the symmetry-adapted modes of the parent phase, as implemented in AMPLIMODES on the Bilbao Crystallographic Server. My own contribution, developed on K₀.₅Na₀.₅NbO₃ and the Sr₂MM′O₆ families with M′ = Sb, W, Mo, Ru, Te, is a parametrised refinement protocol: high-resolution data on one member of a family fix the relations among mode amplitudes, and those relations let laboratory X-ray data, which cannot resolve light elements or subtle tilts on their own, be refined to a physically meaningful solution. It reduces the need for expensive high-resolution experiments and makes preliminary data usable. This line produced four of my five doctoral theses (Gateshki 2003, Faik 2009, Iturbe-Zabalo 2012, Orayech 2015), some forty papers, and a lasting collaboration with Morocco, with Abdeslam El Bouari, Bouchaib Manoun and Abdessamad Faik, that continues today with the Sr₂(Co,Fe,Ni)TeO₆ series in *Dalton Transactions* (2022, 2023).",
 "El método que enlaza el trabajo es el análisis de modos de simetría, o cristalografía de modos: describir una estructura distorsionada no por coordenadas atómicas sino por las amplitudes de los modos adaptados a la simetría de la fase madre, como implementa AMPLIMODES en el Bilbao Crystallographic Server. Mi contribución propia, desarrollada sobre K₀.₅Na₀.₅NbO₃ y las familias Sr₂MM′O₆ con M′ = Sb, W, Mo, Ru, Te, es un protocolo de refinamiento parametrizado: los datos de alta resolución de un miembro de la familia fijan las relaciones entre las amplitudes de los modos, y esas relaciones permiten refinar los datos de rayos X de laboratorio, que por sí solos no resuelven elementos ligeros ni giros sutiles, hasta una solución con sentido físico. Reduce la necesidad de experimentos caros de alta resolución y hace utilizables los datos preliminares. Esta línea produjo cuatro de mis cinco tesis doctorales (Gateshki 2003, Faik 2009, Iturbe-Zabalo 2012, Orayech 2015), unos cuarenta artículos y una colaboración duradera con Marruecos, con Abdeslam El Bouari, Bouchaib Manoun y Abdessamad Faik, que continúa hoy con la serie Sr₂(Co,Fe,Ni)TeO₆ en *Dalton Transactions* (2022, 2023).",
 "Lana lotzen duen metodoa simetria-moduen analisia da, edo moduen kristalografia: egitura desitxuratu bat ez deskribatzea koordenatu atomikoen bidez, baizik eta fase amaren simetriara egokitutako moduen anplitudeen bidez, Bilbao Crystallographic Server-eko AMPLIMODESek inplementatzen duen moduan. Nire ekarpen propioa, K₀.₅Na₀.₅NbO₃ eta Sr₂MM′O₆ familietan garatua M′ = Sb, W, Mo, Ru, Te izanik, errefinamendu-protokolo parametrizatu bat da: familia bateko kide baten bereizmen handiko datuek modu-anplitudeen arteko erlazioak finkatzen dituzte, eta erlazio horiek laborategiko X izpien datuak, berez elementu arinak edo biraketa sotilak bereizten ez dituztenak, zentzu fisikoko soluzio bateraino errefinatzea ahalbidetzen dute. Bereizmen handiko esperimentu garestien beharra murrizten du eta aurretiazko datuak erabilgarri egiten ditu. Lerro honek nire bost doktorego-tesietatik lau eman zituen (Gateshki 2003, Faik 2009, Iturbe-Zabalo 2012, Orayech 2015), berrogei bat artikulu eta Marokorekiko lankidetza iraunkor bat, Abdeslam El Bouari, Bouchaib Manoun eta Abdessamad Faikekin, gaur egun Sr₂(Co,Fe,Ni)TeO₆ seriearekin jarraitzen duena *Dalton Transactions* aldizkarian (2022, 2023)."),
"cap_modes": (
 "Amplitude of the X₅⁺ mode and its components against the experimental tolerance factor for Sr₂MM′O₆ double perovskites, colour-coded by the B′ cation. The regularity across families is what the parametrised refinement exploits.",
 "Amplitud del modo X₅⁺ y de sus componentes frente al factor de tolerancia experimental para las perovskitas dobles Sr₂MM′O₆, con colores según el catión B′. La regularidad entre familias es lo que explota el refinamiento parametrizado.",
 "X₅⁺ moduaren eta bere osagaien anplitudea tolerantzia-faktore esperimentalarekiko Sr₂MM′O₆ perobskita bikoitzetarako, B′ katioiaren araberako koloreekin. Familien arteko erregulartasuna da errefinamendu parametrizatuak ustiatzen duena."),
"alt_modes": (
 "Scatter plot of symmetry-mode amplitudes against tolerance factor for double perovskites with Sb, W, Mo, Ru and Te on the B prime site",
 "Diagrama de dispersión de amplitudes de modos de simetría frente al factor de tolerancia para perovskitas dobles con Sb, W, Mo, Ru y Te en el sitio B prima",
 "Simetria-moduen anplitudeen sakabanatze-diagrama tolerantzia-faktorearekiko, B prima gunean Sb, W, Mo, Ru eta Te duten perobskita bikoitzetarako"),

"h_rad": ("Thermal radiative properties of materials (2018–)",
          "Propiedades radiativas térmicas de materiales (2018–)",
          "Materialen propietate erradiatibo termikoak (2018–)"),
"p_rad1": (
 "Over the last decade my activity has moved to the high-temperature thermophysical properties and the infrared radiative behaviour of materials for energy, in Thermomat, the research group on the thermophysical properties of materials at EHU, which I co-lead. The group operates HAIRL, a high-accuracy infrared radiometer built in-house: directional spectral emissivity from 0.83 to 25 μm, from room temperature to 1000 °C, in controlled atmosphere, with a full uncertainty budget. My part of the work is on the instrument and its data as much as on the samples: the upgrade of the emissometer, the model-free cascaded temperature control published in *IEEE Transactions on Control Systems Technology*, the updated measurement method and uncertainty budget in *Metrologia*, the “fer” framework for FAIR-compliant reporting of traceable experimental results in *IEEE Transactions on Instrumentation and Measurement*, and EKHI, the open database of optical and thermal radiative properties of solids described in *Scientific Data* and indexed by emissivity.org. The materials run from oxidising steels, high-entropy alloys and materials for nuclear fusion to laser-patterned surfaces and selective coatings for concentrated solar power, in close collaboration with CIC Energigune, Tecnalia, Petronor, ArcelorMittal and ESS Bilbao, and with academic partners abroad.",
 "En la última década mi actividad se ha desplazado a las propiedades termofísicas a alta temperatura y al comportamiento radiativo infrarrojo de materiales para la energía, en Thermomat, el grupo de investigación en propiedades termofísicas de materiales de la EHU, que codirijo. El grupo opera HAIRL, un radiómetro infrarrojo de alta precisión construido en casa: emisividad espectral direccional de 0,83 a 25 μm, desde temperatura ambiente hasta 1000 °C, en atmósfera controlada, con un presupuesto de incertidumbre completo. Mi parte del trabajo está tanto en el instrumento y sus datos como en las muestras: la actualización del emisómetro, el control de temperatura en cascada sin modelo publicado en *IEEE Transactions on Control Systems Technology*, el método de medida y el presupuesto de incertidumbre actualizados en *Metrologia*, el marco «fer» para el registro FAIR de resultados experimentales trazables en *IEEE Transactions on Instrumentation and Measurement*, y EKHI, la base de datos abierta de propiedades ópticas y radiativas térmicas de sólidos descrita en *Scientific Data* e indexada por emissivity.org. Los materiales van desde aceros en oxidación, aleaciones de alta entropía y materiales para fusión nuclear hasta superficies texturizadas por láser y recubrimientos selectivos para energía solar de concentración, en estrecha colaboración con CIC Energigune, Tecnalia, Petronor, ArcelorMittal y ESS Bilbao, y con socios académicos en el extranjero.",
 "Azken hamarkadan nire jarduera energiarako materialen tenperatura altuko propietate termofisikoetara eta portaera erradiatibo infragorrira mugitu da, Thermomat taldean, EHUko materialen propietate termofisikoen ikerketa-taldean, nik ko-zuzentzen dudana. Taldeak HAIRL erabiltzen du, etxean eraikitako zehaztasun handiko erradiometro infragorria: emisibitate espektral norabidezkoa 0,83tik 25 μm-ra, giro-tenperaturatik 1000 °C-ra, atmosfera kontrolatuan, ziurgabetasun-aurrekontu osoarekin. Nire lan-zatia tresnan eta bere datuetan dago laginetan bezainbeste: emisometroaren eguneratzea, *IEEE Transactions on Control Systems Technology* aldizkarian argitaratutako eredurik gabeko kaskadako tenperatura-kontrola, *Metrologia* aldizkariko neurketa-metodo eguneratua eta ziurgabetasun-aurrekontua, emaitza esperimental trazagarrien FAIR erregistrorako «fer» esparrua *IEEE Transactions on Instrumentation and Measurement* aldizkarian, eta EKHI, *Scientific Data* aldizkarian deskribatutako eta emissivity.org-ek indexatutako solidoen propietate optiko eta erradiatibo termikoen datu-base irekia. Materialak oxidatzen ari diren altzairuetatik, entropia handiko aleazioetatik eta fusio nuklearrerako materialetatik laser bidez ereduztatutako gainazaletara eta kontzentrazio bidezko eguzki-energiarako estaldura selektiboetara doaz, CIC Energigune, Tecnalia, Petronor, ArcelorMittal eta ESS Bilbaorekin eta atzerriko bazkide akademikoekin lankidetza estuan."),
"p_rad2": (
 "The same years opened a second energy strand with CIC Energigune and Abdessamad Faik: molten nitrate salt nanofluids for thermal energy storage in concentrated solar plants, their enhanced heat capacity and thermal conductivity, the stability of the dispersions and the corrosion of carbon steel in contact with them. It was the fifth doctoral thesis (Nithiyanantham 2019) and five papers in *Solar Energy*, *Solar Energy Materials and Solar Cells*, *Journal of Energy Storage* and *Applied Thermal Engineering*, with a sixth on thermochemical storage in double hydrated salts.",
 "Los mismos años abrieron una segunda vertiente energética con CIC Energigune y Abdessamad Faik: nanofluidos de sales de nitrato fundidas para el almacenamiento de energía térmica en centrales solares de concentración, la mejora de su capacidad calorífica y conductividad térmica, la estabilidad de las dispersiones y la corrosión del acero al carbono en contacto con ellas. Fue la quinta tesis doctoral (Nithiyanantham 2019) y cinco artículos en *Solar Energy*, *Solar Energy Materials and Solar Cells*, *Journal of Energy Storage* y *Applied Thermal Engineering*, con un sexto sobre almacenamiento termoquímico en sales dobles hidratadas.",
 "Urte berberek bigarren energia-adar bat ireki zuten CIC Energigune eta Abdessamad Faikekin: nitrato-gatz urtuen nanofluidoak kontzentrazio bidezko eguzki-zentraletan energia termikoa biltegiratzeko, beren bero-ahalmenaren eta eroankortasun termikoaren hobekuntza, dispertsioen egonkortasuna eta haiekin kontaktuan dagoen karbono-altzairuaren korrosioa. Bosgarren doktorego-tesia izan zen (Nithiyanantham 2019) eta bost artikulu *Solar Energy*, *Solar Energy Materials and Solar Cells*, *Journal of Energy Storage* eta *Applied Thermal Engineering* aldizkarietan, seigarren bat gatz bikoitz hidratatuetako biltegiratze termokimikoari buruz."),
"cap_hairl": (
 "Optical layout of HAIRL: the spectrometer alternates between the sample chamber and two reference blackbodies through a rotating mirror; the sample sits on a heater under vacuum or purge, on a rotation axis for directional measurements.",
 "Disposición óptica de HAIRL: el espectrómetro alterna entre la cámara de muestra y dos cuerpos negros de referencia mediante un espejo giratorio; la muestra descansa sobre un calefactor en vacío o purga, sobre un eje de rotación para medidas direccionales.",
 "HAIRLen antolaera optikoa: espektrometroak lagin-ganberaren eta bi gorputz beltz erreferentziaren artean txandakatzen du ispilu birakari baten bidez; lagina berogailu baten gainean dago hutsean edo purgan, biraketa-ardatz batean norabidezko neurketetarako."),
"alt_hairl": (
 "Optical schematic of the HAIRL emissometer: FTIR spectrometer, parabolic and rotating mirrors, two blackbodies, sample chamber with heater and vacuum",
 "Esquema óptico del emisómetro HAIRL: espectrómetro FTIR, espejos parabólicos y giratorio, dos cuerpos negros, cámara de muestra con calefactor y vacío",
 "HAIRL emisometroaren eskema optikoa: FTIR espektrometroa, ispilu parabolikoak eta birakaria, bi gorputz beltz, berogailua eta hutsa dituen lagin-ganbera"),

"h_teach": ("Computation in physics education", "Computación en la enseñanza de la física", "Konputazioa fisikaren irakaskuntzan"),
"p_teach": (
 "The fifth line began as a way of teaching thermodynamics and became research. Jupyter notebooks written in Basque are the laboratory notebook of a theoretical subject: students derive, compute and plot in the same document, and the subject keeps a daily log of what was done. MinervaLab, an interactive simulation laboratory for first-order phase transitions and the van der Waals fluid, was built as a bachelor's thesis under my direction, released under the GPL, and is the basis of the physics-education contributions I have presented at CINTE 2016, CSEDU 2017, GIREP 2018 and the 2019 biennial meeting of the Real Sociedad Española de Física, and of the teaching-innovation project on the electronic laboratory notebook I led at EHU. The same tools now answer another question: what the data say about how students perform, from the subject's own records to the physics entrance examination across the Spanish regions.",
 "La quinta línea empezó como una forma de enseñar termodinámica y se convirtió en investigación. Los cuadernos Jupyter escritos en euskera son el cuaderno de laboratorio de una asignatura teórica: los estudiantes deducen, calculan y representan en el mismo documento, y la asignatura lleva un diario de lo hecho cada día. MinervaLab, un laboratorio interactivo de simulación de transiciones de fase de primer orden y del fluido de van der Waals, se construyó como trabajo de fin de grado bajo mi dirección, se publicó bajo licencia GPL y es la base de las contribuciones de didáctica de la física que he presentado en CINTE 2016, CSEDU 2017, GIREP 2018 y la bienal de 2019 de la Real Sociedad Española de Física, y del proyecto de innovación docente sobre el cuaderno de laboratorio electrónico que dirigí en la EHU. Las mismas herramientas responden ahora a otra pregunta: qué dicen los datos sobre cómo rinden los estudiantes, desde los registros de la propia asignatura hasta el examen de acceso de física en las comunidades autónomas.",
 "Bosgarren lerroa termodinamika irakasteko modu gisa hasi zen eta ikerketa bihurtu zen. Euskaraz idatzitako Jupyter koadernoak irakasgai teoriko baten laborategi-koadernoa dira: ikasleek dokumentu berean deduzitzen, kalkulatzen eta irudikatzen dute, eta irakasgaiak egindakoaren eguneroko egunkaria darama. MinervaLab, lehen ordenako fase-trantsizioen eta van der Waals fluidoaren simulazio-laborategi interaktiboa, gradu amaierako lan gisa eraiki zen nire zuzendaritzapean, GPL lizentziapean argitaratu zen, eta CINTE 2016, CSEDU 2017, GIREP 2018 eta Real Sociedad Española de Física elkartearen 2019ko bilera bienalean aurkeztu ditudan fisikaren didaktikako ekarpenen oinarria da, baita EHUn zuzendu nuen laborategi-koaderno elektronikoari buruzko irakaskuntza-berrikuntzako proiektuarena ere. Tresna berberek beste galdera bati erantzuten diote orain: zer dioten datuek ikasleek nola errenditzen duten, irakasgaiaren beraren erregistroetatik fisikako sarbide-azterketara Espainiako erkidegoetan."),
"cap_minerva": (
 "Planning sketch for MinervaLab: the decomposition into simulation apps, each with its code, drawn before a line was written. The software lives on GitHub at jongablop/MinervaLab.",
 "Boceto de planificación de MinervaLab: la descomposición en aplicaciones de simulación, cada una con su código, dibujada antes de escribir una línea. El software está en GitHub, en jongablop/MinervaLab.",
 "MinervaLab-en plangintza-zirriborroa: simulazio-aplikazioen deskonposizioa, bakoitza bere kodearekin, lerro bat idatzi aurretik marraztua. Softwarea GitHuben dago, jongablop/MinervaLab helbidean."),
"alt_minerva": (
 "Hand-drawn planning sketch for MinervaLab with numbered timeline boxes and app codes",
 "Boceto de planificación de MinervaLab dibujado a mano, con cajas de cronograma numeradas y códigos de aplicación",
 "MinervaLab-en eskuz marraztutako plangintza-zirriborroa, zenbakitutako kronograma-koadroekin eta aplikazio-kodeekin"),

"h_fac": ("Experiments at large European facilities", "Experimentos en grandes instalaciones europeas", "Europako instalazio handietako esperimentuak"),
"p_fac": (
 "Nineteen experiments between 2007 and 2011 at the Institut Laue-Langevin in Grenoble (instruments D1B, D2B, D20 and D15), the SINQ spallation source of the Paul Scherrer Institut (HRPT), the FRM II reactor in Garching (SPODI), the Helmholtz-Zentrum Berlin (E9) and the ESRF (BM25 SpLine), sixteen of them as principal investigator. Beam time at these facilities is awarded by international peer review, with success rates near one in two at the ILL and stricter quotas for foreign groups elsewhere; valued at the facilities' own published cost per day of operation, about 12 000 €, the time awarded amounts to half a million euros. Each proposal was a study of structures and phase transitions in the double-perovskite line, and its data went into the theses and papers above.",
 "Diecinueve experimentos entre 2007 y 2011 en el Institut Laue-Langevin de Grenoble (instrumentos D1B, D2B, D20 y D15), la fuente de espalación SINQ del Paul Scherrer Institut (HRPT), el reactor FRM II de Garching (SPODI), el Helmholtz-Zentrum Berlin (E9) y el ESRF (BM25 SpLine), dieciséis de ellos como investigador principal. El tiempo de haz en estas instalaciones se concede por evaluación internacional entre pares, con tasas de éxito cercanas a una de cada dos en el ILL y cupos más estrictos para grupos extranjeros en las demás; valorado al coste por día de operación que publican las propias instalaciones, unos 12 000 €, el tiempo concedido equivale a medio millón de euros. Cada propuesta fue un estudio de estructuras y transiciones de fase de la línea de perovskitas dobles, y sus datos alimentaron las tesis y artículos anteriores.",
 "Hemeretzi esperimentu 2007 eta 2011 artean Grenobleko Institut Laue-Langevinen (D1B, D2B, D20 eta D15 tresnak), Paul Scherrer Institut-eko SINQ espalazio-iturrian (HRPT), Garchingeko FRM II erreaktorean (SPODI), Helmholtz-Zentrum Berlinen (E9) eta ESRFn (BM25 SpLine), horietatik hamasei ikertzaile nagusi gisa. Instalazio horietako izpi-denbora nazioarteko parekoen ebaluazioz esleitzen da, ILLn bitik bat inguruko arrakasta-tasekin eta atzerriko taldeentzako kupo zorrotzagoekin besteetan; instalazioek berek argitaratutako eguneko funtzionamendu-kostuan baloratuta, 12 000 € inguru, emandako denbora milioi erdi euro da. Proposamen bakoitza perobskita bikoitzen lerroko egituren eta fase-trantsizioen azterketa bat izan zen, eta bere datuak goiko tesi eta artikuluetara joan ziren."),
"th_when": ("Dates", "Fechas", "Datak"),
"th_where": ("Facility", "Instalación", "Instalazioa"),
"th_exp": ("Experiment", "Experimento", "Esperimentua"),
"th_days": ("Days", "Días", "Egunak"),
"th_role": ("Role", "Papel", "Eginkizuna"),
"pi": ("PI", "IP", "IN"),
"coi": ("co-investigator", "coinvestigador", "ikertzaile kidea"),
"p_fac_note": (
 "Role: PI, principal investigator of the proposal; co-investigator on the three proposals led by Vicente Recarte (Universidad Pública de Navarra).",
 "Papel: IP, investigador principal de la propuesta; coinvestigador en las tres propuestas lideradas por Vicente Recarte (Universidad Pública de Navarra).",
 "Eginkizuna: IN, proposamenaren ikertzaile nagusia; ikertzaile kidea Vicente Recartek (Nafarroako Unibertsitate Publikoa) zuzendutako hiru proposamenetan."),

"h_proj": ("Competitive projects and research groups", "Proyectos competitivos y grupos de investigación", "Proiektu lehiakorrak eta ikerketa-taldeak"),
"p_proj": (
 "More than forty competitive projects and recognised research groups across the career, and over sixty entries once funded actions and contracts are counted: first as a member of the structural-physics group led by J. Manuel Pérez-Mato and Gotzon Madariaga, since 2018 in Thermomat, and as principal investigator of the EHU node of the ELKARTEK storage project, of the large-facility proposals above and of the teaching-innovation project on the electronic laboratory notebook. The recognised groups are listed first, then the projects in reverse chronological order. Amounts are the sums awarded to EHU as they appear in the certificates of the Vice-Rectorate for Research.",
 "Más de cuarenta proyectos competitivos y grupos de investigación reconocidos a lo largo de la carrera, y más de sesenta entradas si se cuentan las acciones financiadas y los contratos: primero como miembro del grupo de física estructural dirigido por J. Manuel Pérez-Mato y Gotzon Madariaga, desde 2018 en Thermomat, y como investigador principal del nodo EHU del proyecto ELKARTEK de almacenamiento, de las propuestas de grandes instalaciones anteriores y del proyecto de innovación docente sobre el cuaderno de laboratorio electrónico. Se listan primero los grupos reconocidos y después los proyectos, en orden cronológico inverso. Las cantidades son las concedidas a la EHU tal como aparecen en los certificados del Vicerrectorado de Investigación.",
 "Berrogei proiektu lehiakor eta ikerketa-talde aitortu baino gehiago ibilbidean zehar, eta hirurogei sarrera baino gehiago ekintza finantzatuak eta kontratuak zenbatuz gero: lehenik J. Manuel Pérez-Matok eta Gotzon Madariagak zuzendutako egitura-fisikako taldeko kide gisa, 2018tik Thermomaten, eta ikertzaile nagusi gisa ELKARTEK biltegiratze-proiektuaren EHU nodoan, goiko instalazio handietako proposamenetan eta laborategi-koaderno elektronikoari buruzko irakaskuntza-berrikuntzako proiektuan. Lehenik talde aitortuak zerrendatzen dira, gero proiektuak, kronologia alderantzizko ordenan. Zenbatekoak EHUri emandakoak dira, Ikerketako Errektoreordetzaren ziurtagirietan agertzen diren bezala."),
"h_groups": ("Recognised research groups", "Grupos de investigación reconocidos", "Ikerketa-talde aitortuak"),
"h_projects": ("Projects and funded actions", "Proyectos y acciones financiadas", "Proiektuak eta ekintza finantzatuak"),
"th_years": ("Years", "Años", "Urteak"),
"th_title": ("Project", "Proyecto", "Proiektua"),
"th_funder": ("Funder", "Financiador", "Finantzatzailea"),
"th_pi": ("PI", "IP", "IN"),
"th_amount": ("Awarded", "Concedido", "Emandakoa"),

"h_contracts": ("Contracts with industry", "Contratos con la industria", "Industriarekiko kontratuak"),
"p_contracts": (
 "Research and consultancy contracts of the Thermomat group in which I take part, all on infrared emissivity and thermo-optical measurement.",
 "Contratos de investigación y consultoría del grupo Thermomat en los que participo, todos sobre emisividad infrarroja y medida termo-óptica.",
 "Thermomat taldearen ikerketa- eta aholkularitza-kontratuak, nik parte hartzen dudanak, guztiak emisibitate infragorriari eta neurketa termo-optikoari buruz."),
"th_contract": ("Contract", "Contrato", "Kontratua"),
"th_company": ("Company", "Empresa", "Enpresa"),

"h_comm": ("Community", "Comunidad", "Komunitatea"),
"p_comm": (
 "Around a hundred conference contributions since 1990, with invited talks at the Gordon Conference on order and disorder in solids (New London, 1994), the Kraków workshop on symmetry analysis in diffraction (1996), the Hünfeld symposium on the predictability of crystal structures (1997) and, in the emissivity years, THERMEC, EUROMAT, the MRS Spring Meeting, MMC and EOSAM. Reviewer for some twenty indexed journals in materials science, thermophysics, crystallography and instrumentation, with more than a hundred reviews completed; associate editor of *Energies*. Member of the organising committee of the two international schools of the Bilbao Crystallographic Server (2009, 2011) and a graduate of the ILL FullProf school, the Hercules course and the European School on Multiferroics. Vice-president of the local section of the Real Sociedad Española de Física.",
 "Un centenar de contribuciones a congresos desde 1990, con conferencias invitadas en la Gordon Conference sobre orden y desorden en sólidos (New London, 1994), el taller de Cracovia sobre análisis de simetría en difracción (1996), el simposio de Hünfeld sobre la predictibilidad de las estructuras cristalinas (1997) y, en los años de la emisividad, THERMEC, EUROMAT, el MRS Spring Meeting, MMC y EOSAM. Revisor de una veintena de revistas indexadas de ciencia de materiales, termofísica, cristalografía e instrumentación, con más de cien revisiones completadas; editor asociado de *Energies*. Miembro del comité organizador de las dos escuelas internacionales del Bilbao Crystallographic Server (2009, 2011) y alumno de la escuela FullProf del ILL, del curso Hercules y de la European School on Multiferroics. Vicepresidente de la sección local de la Real Sociedad Española de Física.",
 "Ehun bat kongresu-ekarpen 1990etik, gonbidatutako hitzaldiekin solidoetako ordena eta desordenari buruzko Gordon Conferencen (New London, 1994), difrakzioko simetria-analisiari buruzko Krakoviako tailerrean (1996), egitura kristalinoen iragargarritasunari buruzko Hünfeldeko sinposioan (1997) eta, emisibitatearen urteetan, THERMEC, EUROMAT, MRS Spring Meeting, MMC eta EOSAM bileretan. Materialen zientzia, termofisika, kristalografia eta instrumentazioko hogei bat aldizkari indexaturen berrikuslea, ehun berrikuspen baino gehiago osatuta; *Energies* aldizkariaren editore elkartua. Bilbao Crystallographic Server-aren bi nazioarteko eskolen antolakuntza-batzordeko kidea (2009, 2011) eta ILLko FullProf eskolako, Hercules ikastaroko eta European School on Multiferroics-eko ikaslea. Real Sociedad Española de Física elkartearen tokiko sekzioaren presidenteordea."),
"toc": ("On this page", "En esta página", "Orri honetan"),
"h_conf": ("Conference contributions listed in the dossier and the 2022 CV", "Contribuciones a congresos listadas en el dosier y en el CV de 2022", "Dosierrean eta 2022ko CVan zerrendatutako kongresu-ekarpenak"),
"conf_sum": ("{n} contributions, {i} invited talks, {o} oral, {p} posters · open the list", "{n} contribuciones, {i} invitadas, {o} orales, {p} pósteres · abrir la lista", "{n} ekarpen, {i} gonbidatuak, {o} ahozkoak, {p} posterrak · zerrenda ireki"),
"th_conf": (("Year", "Contribution", "Conference", "Place", "Type"), ("Año", "Contribución", "Congreso", "Lugar", "Tipo"), ("Urtea", "Ekarpena", "Kongresua", "Tokia", "Mota")),
"kind": ({"invited": "invited", "oral": "oral", "poster": "poster"}, {"invited": "invitada", "oral": "oral", "poster": "póster"}, {"invited": "gonbidatua", "oral": "ahozkoa", "poster": "posterra"}),
}

# ---------------------------------------------------------------- tables
# Experiments: (dates per lang, facility, title, days, role) — titles kept in English (as submitted).
ILL = "ILL, Grenoble"; SINQ = "SINQ (PSI), Villigen"; FRM = "FRM II (SPODI), Garching"; HZB = "HZB (E9), Berlin"; ESRF = "ESRF (BM25), Grenoble"
EXPS = [
 (("Dec 2007","dic 2007","2007 abe"), ILL, "Kinetics of the transformations A₂Mn²⁺WO₆ → A₂Mn³⁺WO₆ (A = Ca, Sr) and the temperature-induced phase transitions", "3", "coi"),
 (("Sep 2008","sep 2008","2008 ira"), ILL, "Temperature evolution of the phase-transition sequences in Sr₂MSbO₆ (M = Co, Fe, Cr, Sc, Ga, Sm, La)", "3", "coi"),
 (("Oct 2008","oct 2008","2008 urr"), HZB, "Temperature evolution of the symmetry modes of the phase-transition sequences in Sr₂MSbO₆ (M = Sc, La)", "8", "pi"),
 (("Jun 2010","jun 2010","2010 eka"), SINQ, "Structures and phase transitions of the triple perovskites A′A″₂CuTi₂O₉ (A′ = Ca, Ba; A″ = Pr, Nd)", "4", "pi"),
 (("Jul 2010","jul 2010","2010 uzt"), ILL, "Phase transitions in Fe-Al-Cr alloys and their relation to the mobility of dislocations and grain boundaries", "3", "coi"),
 (("Jul 2010","jul 2010","2010 uzt"), FRM, "Structures and phase transitions at low and high temperature of SrNdMRuO₆ (M = Ni, Co, Fe, Mg, Zn)", "4", "pi"),
 (("Jul 2010","jul 2010","2010 uzt"), ILL, "Thermal evolution of SrLaCoRuO₆: magnetic and nuclear structures", "4", "pi"),
 (("Dec 2010","dic 2010","2010 abe"), ILL, "Structural and magnetic characterisation of the possible multiferroic Pb₃Ni₁.₅Mn₅.₅O₁₅ (two experiments)", "4", "pi"),
 (("Dec 2010","dic 2010","2010 abe"), ILL + " (D2B)", "Structures and phase transitions at low and high temperature of the new double perovskites SrNdMRuO₆", "3", "pi"),
 (("Dec 2010","dic 2010","2010 abe"), ILL, "Symmetry of the ferroelectric phase in multiferroic BiFeO₃: neutron diffraction aided by group-theoretical tools", "2", "pi"),
 (("Apr 2011","abr 2011","2011 api"), SINQ, "Characterisation of the possible multiferroic Pb₃Ni₁.₅Mn₅.₅O₁₅", "5", "pi"),
 (("2011","2011","2011"), ESRF, "Characterisation of the possible multiferroic Pb₃Ni₁.₅Mn₅.₅O₁₅ by synchrotron powder diffraction", "—", "pi"),
 (("Jul 2011","jul 2011","2011 uzt"), ILL, "Structural and magnetic characterisation of SrPrMRuO₆ (M = Mg, Co, Ni, Zn)", "1", "pi"),
 (("Aug 2011","ago 2011","2011 abu"), SINQ, "Structural and magnetic characterisation of SrPrMRuO₆ (M = Mg, Co, Ni, Zn, Fe)", "3", "pi"),
 (("Sep 2011","sep 2011","2011 ira"), ILL, "Structural and magnetic characterisation at low and high temperature of SrPrMRuO₆", "3", "pi"),
 (("Oct 2011","oct 2011","2011 urr"), ILL, "SrNdCoRuO₆, SrNdNiRuO₆ and SrLaCoRuO₆: nuclear and magnetic structures", "1", "pi"),
 (("Nov 2011","nov 2011","2011 aza"), ILL, "Structural phase-transition sequence in the multiferroic magnetoelectric NaLaCoWO₆", "1", "pi"),
 (("Nov–Dec 2011","nov–dic 2011","2011 aza–abe"), ILL, "Rare-earth cation influence on the crystal and magnetic structures of SrLnFeRuO₆ (Ln = La, Nd, Pr)", "32", "pi"),
]

GV = ("Basque Government", "Gobierno Vasco", "Eusko Jaurlaritza")
UPV = ("EHU", "EHU", "EHU")
UPVGV = ("EHU and Basque Government", "EHU y Gobierno Vasco", "EHU eta Eusko Jaurlaritza")
MEC = ("Spanish Ministry of Education and Science", "Ministerio de Educación y Ciencia", "Espainiako Hezkuntza eta Zientzia Ministerioa")
MINECO = ("Spanish Ministry of Economy and Competitiveness", "Ministerio de Economía y Competitividad", "Espainiako Ekonomia eta Lehiakortasun Ministerioa")
MICINN = ("Spanish Ministry of Science and Innovation", "Ministerio de Ciencia e Innovación", "Espainiako Zientzia eta Berrikuntza Ministerioa")
MCYT = ("Spanish Ministry of Science and Technology", "Ministerio de Ciencia y Tecnología", "Espainiako Zientzia eta Teknologia Ministerioa")
DGES = ("DGESIC, Spanish Ministry of Education", "DGESIC, Ministerio de Educación", "DGESIC, Espainiako Hezkuntza Ministerioa")

GROUPS = [
 ("2022–2025", ("Research group on the thermophysical properties of materials (IT1714-22)", "Grupo de investigación en propiedades termofísicas de materiales (IT1714-22)", "Materialen propietate termofisikoen ikerketa-taldea (IT1714-22)"), GV, "R. Fuente", "104 400 €"),
 ("2019–2022", ("Research group on the radiative properties of materials (GIU19/019, IT1364-19)", "Grupo de investigación en propiedades radiativas de materiales (GIU19/019, IT1364-19)", "Materialen propietate erradiatiboen ikerketa-taldea (GIU19/019, IT1364-19)"), UPVGV, "R. Fuente, G. A. López", "26 271 €"),
 ("2013–2018", ("Structural and dynamical properties of solids (GIC12/146, IT779-13)", "Propiedades estructurales y dinámicas de sólidos (GIC12/146, IT779-13)", "Solidoen egitura- eta dinamika-propietateak (GIC12/146, IT779-13)"), GV, "G. Madariaga", "262 798 €"),
 ("2007–2012", ("Structural and dynamical properties of solids (GIC07/117, IT-282-07)", "Propiedades estructurales y dinámicas de sólidos (GIC07/117, IT-282-07)", "Solidoen egitura- eta dinamika-propietateak (GIC07/117, IT-282-07)"), GV, "J. M. Pérez-Mato", "563 474 €"),
 ("2001–2006", ("Development of instrumentation for X-ray and synchrotron diffraction (GIC01/43)", "Desarrollo de instrumentación para difracción de rayos X y radiación sincrotrón (GIC01/43)", "X izpien eta sinkrotroi-erradiazioaren difrakziorako instrumentazioaren garapena (GIC01/43)"), GV, "J. M. Pérez-Mato", "420 519 €"),
 ("2001–2006", ("Structural and dynamical properties of solids, consolidated high-performance group (UPV0063.310-13564/2001, with three extensions)", "Propiedades estructurales y dinámicas de sólidos, grupo consolidado de alto rendimiento (UPV0063.310-13564/2001, con tres prórrogas)", "Solidoen egitura- eta dinamika-propietateak, errendimendu handiko talde finkatua (UPV0063.310-13564/2001, hiru luzapenekin)"), UPV, "J. M. Pérez-Mato", "380 426 €"),
 ("1998–2000", ("Structural and dynamical properties of solids", "Propiedades estructurales y dinámicas de sólidos", "Solidoen egitura- eta dinamika-propietateak"), UPV, "J. M. Pérez-Mato", "228 360 €"),
]

PROJECTS = [
 ("2025–2026", ("SIMULATE: multiscale and multiphysics simulation approaches in laser microfabrication (KK-2025/00075)", "SIMULATE: aproximaciones de simulación multiescala y multifísica en microfabricación láser (KK-2025/00075)", "SIMULATE: eskala anitzeko eta fisika anitzeko simulazio-hurbilketak laser bidezko mikrofabrikazioan (KK-2025/00075)"), GV, "—", "135 284 €"),
 ("2024–2026", ("Systematic study of defects in steel production for traceability and efficiency (US24/04), with Sidenor I+D", "Estudio sistemático de defectos en la producción de aceros para trazabilidad y eficiencia (US24/04), con Sidenor I+D", "Altzairuen ekoizpeneko akatsen azterketa sistematikoa trazagarritasunerako eta eraginkortasunerako (US24/04), Sidenor I+D-rekin"), UPV, "—", "14 585 €"),
 ("2021–2023", ("Advanced characterisation of latest-generation aeronautical alloys for high temperature (PIBA_2021_1_0022)", "Caracterización avanzada de aleaciones aeronáuticas de última generación para alta temperatura (PIBA_2021_1_0022)", "Azken belaunaldiko aleazio aeronautikoen karakterizazio aurreratua tenperatura altuetarako (PIBA_2021_1_0022)"), GV, "G. A. López", "50 000 €"),
 ("2019–2021", ("Modelling for the development of correction algorithms in thermography (US19/13), with Petronor", "Modelización para el desarrollo de algoritmos de corrección en termografía (US19/13), con Petronor", "Termografiako zuzenketa-algoritmoen garapenerako modelizazioa (US19/13), Petronorrekin"), UPV, "R. Fuente, G. A. López", "63 450 €"),
 ("2019", ("Infrared camera for high temperature, infrastructure (INF19/18)", "Cámara infrarroja para alta temperatura, infraestructura (INF19/18)", "Tenperatura altuko kamera infragorria, azpiegitura (INF19/18)"), UPV, "R. Fuente", "10 792 €"),
 ("2019", ("Research aid, groups mode II (PPGA19/25)", "Ayudas a la investigación, modalidad II grupos (PPGA19/25)", "Ikerketarako laguntzak, II. modalitatea taldeak (PPGA19/25)"), UPV, "R. Fuente", "5 566 €"),
 ("2018–2019", ("Strategic fundamental research on electrochemical and thermal energy storage for hybrid storage systems (ELKARTEK KK-2018/00098), coordinated by CIC Energigune", "Investigación fundamental estratégica en almacenamiento de energía electroquímica y térmica para sistemas de almacenamiento híbridos (ELKARTEK KK-2018/00098), coordinado por CIC Energigune", "Sistema hibridoetarako energia elektrokimikoaren eta termikoaren biltegiratzeari buruzko oinarrizko ikerketa estrategikoa (ELKARTEK KK-2018/00098), CIC Energigunek koordinatua"), GV, ("G. A. López, J. M. Igartua (EHU node)", "G. A. López, J. M. Igartua (nodo EHU)", "G. A. López, J. M. Igartua (EHU nodoa)"), ("74 018 € to the group, 3.1 M€ in all", "74 018 € al grupo, 3,1 M€ en total", "74 018 € taldearentzat, 3,1 M€ guztira")),
 ("2018–2019", ("Electronic laboratory notebook: Jupyter Notebook, teaching-innovation project (PIE 61)", "Cuaderno de laboratorio electrónico: Jupyter Notebook, proyecto de innovación educativa (PIE 61)", "Laborategi-koaderno elektronikoa: Jupyter Notebook, irakaskuntza-berrikuntzako proiektua (PIE 61)"), UPV, "J. M. Igartua", "1 000 €"),
 ("2016–2018", ("New magnetic, ferroic and multiferroic materials: structure, properties and tools for their analysis (MAT2015-66441-P)", "Nuevos materiales magnéticos, ferroicos y multiferroicos: estructura, propiedades y desarrollo de herramientas para su análisis (MAT2015-66441-P)", "Material magnetiko, ferroiko eta multiferroiko berriak: egitura, propietateak eta haien analisirako tresnak (MAT2015-66441-P)"), MINECO, "G. Madariaga", "177 870 €"),
 ("2013–2015", ("Synthesis, structure and properties of new ferroic and multiferroic materials (MAT2012-34740)", "Síntesis, estructura y propiedades de nuevos materiales ferroicos y multiferroicos (MAT2012-34740)", "Material ferroiko eta multiferroiko berrien sintesia, egitura eta propietateak (MAT2012-34740)"), MINECO, "G. Madariaga", "204 750 €"),
 ("2011", ("Multipurpose diffractometer with Eulerian geometry, dual X-ray source and real-time 2D detection, infrastructure (GVINF11/48)", "Difractómetro polivalente con geometría euleriana, fuente dual de rayos X y detección bidimensional en tiempo real, infraestructura (GVINF11/48)", "Geometria eulerdarreko difraktometro polibalentea, X izpien iturri bikoitza eta denbora errealeko detekzio bidimentsionala, azpiegitura (GVINF11/48)"), GV, "J. M. Pérez-Mato", "300 000 €"),
 ("2011–2012", ("ITON 2011 satellite workshop: online edition of the International Tables for Crystallography (CGV11/51)", "ITON 2011 satellite workshop: edición en línea de las International Tables for Crystallography (CGV11/51)", "ITON 2011 satellite workshop: International Tables for Crystallography-ren lineako edizioa (CGV11/51)"), GV, "G. Madariaga", "5 866 €"),
 ("2009–2012", ("Structure and properties in ferroic and multiferroic materials: modelling and experiments (MAT2008-05839)", "Estructura y propiedades en materiales ferroicos y multiferroicos: modelización y experimentos (MAT2008-05839)", "Egitura eta propietateak material ferroiko eta multiferroikoetan: modelizazioa eta esperimentuak (MAT2008-05839)"), MICINN, "J. M. Pérez-Mato", "121 000 €"),
 ("2009–2010", ("ITON 2009 satellite workshop: international school on the Bilbao Crystallographic Server", "ITON 2009 satellite workshop: escuela internacional sobre el Bilbao Crystallographic Server", "ITON 2009 satellite workshop: Bilbao Crystallographic Server-ari buruzko nazioarteko eskola"), GV, "G. Madariaga", "5 000 €"),
 ("2009", ("Upgrade of the electronic interfaces of two X-ray diffractometers, infrastructure (INF09/16)", "Actualización de las interfaces electrónicas de dos equipos de difracción de rayos X, infraestructura (INF09/16)", "Bi X izpien difrakzio-ekipoen interfaze elektronikoen eguneratzea, azpiegitura (INF09/16)"), UPV, "G. Madariaga", "23 497 €"),
 ("2009–2012", ("Visits to the ILL, ESRF and CERN for master's students, two editions (PISAM 2009/10, 2011/12)", "Visitas al ILL, ESRF y CERN para estudiantes de máster, dos ediciones (PISAM 2009/10, 2011/12)", "ILL, ESRF eta CERNera bisitak master-ikasleentzat, bi edizio (PISAM 2009/10, 2011/12)"), UPV, "J. M. Igartua", "8 200 €"),
 ("2007", ("Physics in action, outreach conference (CSJ07/14)", "Física en acción, congresos y jornadas (CSJ07/14)", "Fisika ekinean, kongresuak eta jardunaldiak (CSJ07/14)"), UPV, "G. Madariaga", "6 000 €"),
 ("2005–2008", ("Crystal structures and properties of new functional materials under non-ambient conditions (FIS2005-07090)", "Estructuras cristalinas y propiedades de nuevos materiales funcionales en condiciones no ambientales (FIS2005-07090)", "Material funtzional berrien egitura kristalinoak eta propietateak giro-baldintzez kanpo (FIS2005-07090)"), MEC, "A. Grzechnik", "64 260 €"),
 ("2002–2005", ("Superspace description and phase transitions in layered compounds with perovskite-derived structures (BFM2002-00057)", "Descripción superespacial y transiciones de fase en compuestos de capas con estructuras derivadas de la perovskita (BFM2002-00057)", "Superespazio-deskribapena eta fase-trantsizioak perobskitatik eratorritako egiturak dituzten geruza-konposatuetan (BFM2002-00057)"), MCYT, "F. J. Zúñiga", "80 918 €"),
 ("1999–2002", ("Phase transitions in solids: mechanisms and structure (PB98-0244)", "Transiciones de fase en sólidos: mecanismos y estructura (PB98-0244)", "Fase-trantsizioak solidoetan: mekanismoak eta egitura (PB98-0244)"), DGES, "J. M. Pérez-Mato", "48 000 €"),
 ("1998–1999", ("Basic mechanisms in structural phase transitions", "Mecanismos básicos en transiciones de fase estructurales", "Oinarrizko mekanismoak egiturazko fase-trantsizioetan"), MEC, "J. M. Pérez-Mato", "7 200 €"),
 ("1995–1998", ("Structure and stability of insulating materials and quasicrystals", "Estructura y estabilidad de materiales aislantes y cuasicristales", "Material isolatzaileen eta kuasikristalen egitura eta egonkortasuna"), MEC, "J. M. Pérez-Mato", "42 000 €"),
 ("1995", ("Phase-diagram studies in the ABX₃ family", "Estudios de diagramas de fase en la familia ABX₃", "Fase-diagramen azterketak ABX₃ familian"), UPV, "A. López-Echarri", "10 800 €"),
 ("1993", ("Phase transitions in ferroelectric crystals", "Transiciones de fase en cristales ferroeléctricos", "Fase-trantsizioak kristal ferroelektrikoetan"), UPV, "A. López-Echarri", "—"),
 ("1992", ("Spectroscopic study of A₂BX₄ crystals with incommensurate phases", "Estudio espectroscópico de cristales A₂BX₄ con fases inconmensurables", "Fase inkonmentsurableak dituzten A₂BX₄ kristalen azterketa espektroskopikoa"), UPV, "A. López-Echarri", "—"),
 ("1989–1991", ("Calorimetric study of ferroelectric and incommensurate crystals", "Estudio calorimétrico de cristales ferroeléctricos e inconmensurables", "Kristal ferroelektriko eta inkonmentsurableen azterketa kalorimetrikoa"), UPV, "A. López-Echarri", "2 362 €"),
]

CONTRACTS = [
 ("2025", ("Thermo-optical properties of materials", "Propiedades termo-ópticas de materiales", "Materialen propietate termo-optikoak"), "ITP Aero", "—"),
 ("2019–2021", ("Thermo-optical techniques for measuring tube-skin temperature in Petronor furnaces", "Técnicas termo-ópticas para la medida de temperatura de piel de tubo en hornos de Petronor", "Hodi-azalaren tenperatura neurtzeko teknika termo-optikoak Petronorren labeetan"), "Petronor Innovación", "89 241 €"),
 ("2017", ("Infrared emissivity of 316L steel with different surface finishes", "Emisividad infrarroja del acero 316L con distintos acabados superficiales", "316L altzairuaren emisibitate infragorria gainazal-akabera desberdinekin"), "ESS Bilbao", "31 764 €"),
 ("2017", ("Infrared emissivity of alumina and boron nitride samples for the contrast of an industrial device", "Emisividad infrarroja de muestras de alúmina y nitruro de boro para el contraste de un dispositivo industrial", "Alumina eta boro nitruro laginen emisibitate infragorria gailu industrial baten kontrasterako"), "ArcelorMittal Sestao", "3 594 €"),
 ("2017–2018", ("Normal and directional infrared emissivity of a paint sample", "Emisividad infrarroja normal y direccional de una muestra de pintura", "Pintura-lagin baten emisibitate infragorri normala eta norabidezkoa"), "SENER Ingeniería y Sistemas", "3 010 €"),
]

SCRIPT = '''<script>
(function () {
  var main = document.querySelector(".article-grid > .page-article");
  var list = document.getElementById("docs-toc-list");
  if (!main || !list) return;
  var heads = main.querySelectorAll("h2, h3");
  heads.forEach(function (h) {
    if (!h.id) return;
    var li = document.createElement("li"); li.className = h.tagName === "H3" ? "l3" : "l2";
    var a = document.createElement("a"); a.href = "#" + h.id; a.textContent = h.textContent;
    li.appendChild(a); list.appendChild(li);
  });
  if (!list.children.length) { list.parentNode.hidden = true; return; }
  var links = list.querySelectorAll("a");
  var mark = function () {
    var y = window.scrollY + 80, cur = null;
    heads.forEach(function (h) { if (h.id && h.getBoundingClientRect().top + window.scrollY <= y) cur = h.id; });
    links.forEach(function (a) { a.classList.toggle("current", cur !== null && a.getAttribute("href") === "#" + cur); });
  };
  window.addEventListener("scroll", mark, { passive: true }); mark();
})();
</script>'''

def pick(v, i):
    return v[i] if isinstance(v, tuple) else v

def table(headers, rows):
    out = ['<div class="table-wrap"><table>', "<thead><tr>" + "".join(f"<th>{h}</th>" for h in headers) + "</tr></thead>", "<tbody>"]
    for r in rows:
        out.append("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>")
    out.append("</tbody></table></div>")
    return "\n".join(out)

def conf_details(i):
    items = yaml.safe_load((ROOT / "_data" / "conferences.yml").read_text())["items"]
    t = lambda k: T[k][i]
    c = {k: sum(1 for x in items if x["kind"] == k) for k in ("invited", "oral", "poster")}
    rows = [(x["year"], html.escape(x["title"]), html.escape(x["conference"]), html.escape(x["place"]), t("kind")[x["kind"]]) for x in sorted(items, key=lambda x: (-x["year"], -(x["month"] or 0)))]
    return (f'<details class="list-details"><summary>{t("conf_sum").format(n=len(items), i=c["invited"], o=c["oral"], p=c["poster"])}</summary>'
            + table(list(t("th_conf")), rows) + "</details>")

def build(i):
    t = lambda k: T[k][i]
    img = "../../assets/images/" if i else "../assets/images/"
    exp_rows = [(pick(d, i), fac, ttl, days, t(role)) for d, fac, ttl, days, role in EXPS]
    grp_rows = [(y, pick(ttl, i), pick(f, i), pick(p, i), pick(a, i)) for y, ttl, f, p, a in GROUPS]
    prj_rows = [(y, pick(ttl, i), pick(f, i), pick(p, i), pick(a, i)) for y, ttl, f, p, a in PROJECTS]
    con_rows = [(y, pick(ttl, i), c, a) for y, ttl, c, a in CONTRACTS]
    fig = lambda src, alt, cap: f'```{{=html}}\n<figure class="thesis-figure"><img src="{img}{src}" alt="{alt}"><figcaption>{cap}</figcaption></figure>\n```'
    parts = [
f"""---
title: "{t('title')}"
description: "{t('desc')}"
title-block-style: none
page-layout: full
toc: false
---

```{{=html}}
<div class="crumbs"><a href="../index.html">igartua</a> / {t('crumb')}</div>
<div class="article-grid">
<article class="page-article">
<h1>{t('title')}</h1>
<p class="sub">{t('sub')}</p>
```

{t('intro')}

## {t('h_calo')} {{#calorimetry}}

{t('p_calo')}

## {t('h_pseudo')} {{#pseudosymmetry}}

{t('p_pseudo')}

## {t('h_perov')} {{#structure}}

{t('p_perov1')}

{t('p_perov2')}

{fig('mode-amplitudes-tolerance.png', t('alt_modes'), t('cap_modes'))}

## {t('h_rad')} {{#radiation}}

{t('p_rad1')}

{t('p_rad2')}

{fig('hairl-schematic.png', t('alt_hairl'), t('cap_hairl'))}

## {t('h_teach')} {{#teaching}}

{t('p_teach')}

{fig('minervalab-sketch.png', t('alt_minerva'), t('cap_minerva'))}

## {t('h_fac')} {{#facilities}}

{t('p_fac')}

```{{=html}}
{table([t('th_when'), t('th_where'), t('th_exp'), t('th_days'), t('th_role')], exp_rows)}
<p class="table-note">{t('p_fac_note')}</p>
```

## {t('h_proj')} {{#projects}}

{t('p_proj')}

### {t('h_groups')} {{#groups}}

```{{=html}}
{table([t('th_years'), t('th_title'), t('th_funder'), t('th_pi'), t('th_amount')], grp_rows)}
```

### {t('h_projects')} {{#funded}}

```{{=html}}
{table([t('th_years'), t('th_title'), t('th_funder'), t('th_pi'), t('th_amount')], prj_rows)}
```

## {t('h_contracts')} {{#contracts}}

{t('p_contracts')}

```{{=html}}
{table([t('th_years'), t('th_contract'), t('th_company'), t('th_amount')], con_rows)}
```

## {t('h_comm')} {{#community}}

{t('p_comm')}

```{{=html}}
<h3 id="conferences">{t('h_conf')}</h3>
{conf_details(i)}
</article>
<aside class="docs-toc" aria-label="{t('toc')}"><div class="t">{t('toc')}</div><ol id="docs-toc-list"></ol></aside>
</div>
{SCRIPT}
```
"""]
    return "".join(parts)

for i, lang in enumerate(L):
    p = ROOT / ("research/index.qmd" if lang == "en" else f"{lang}/research/index.qmd")
    p.write_text(build(i))
    print("wrote", p, len(p.read_text()))
