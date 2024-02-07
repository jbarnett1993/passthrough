import pandas as pd
import numpy as np
import tia.bbg.datamgr as dm

mgr = dm.BbgDataManager()

events = ['JNCICLEI Index', 'SZUE Index', 'SZUEUEA Index', 'GRIPIMOM Index', 'GEINYY Index', 'SWBUL Index', 'NOIPSAMM Index', 'NOIPOYOY Index', 'NOIPISAM Index', 'NOIPIYOY Index', 'FRTEBAL Index', 'SZRAFCRC Index', 'ITNSSTN Index', 'ITNSTY Index', 'LMEXCA Index', 'LMEXZS Index', 'LMEXAH Index', 'LMEXNI Index', 'BZPBPRDM Index', 'BZDPNDT% Index', 'MBAVCHNG Index', 'BZRTRYOY Index', 'BZRTRETM Index', 'MXVETOTL Index', 'MXVPTOTL Index', 'RUFGGFML Index', 'CATBTOTB Index', 'USTBTOT Index', 'MXIRINUS Index', 'DOEASCRD Index', 'DOEASCUS Index', 'DOEASMGS Index', 'DOEASDIS Index', 'DOEAUTIL Index', 'DOIDCRUD Index', 'DOIDMOGA Index', 'DOESFETH Index', 'DOETFETH Index', 'RUWCWOW Index', 'RUWCYTD Index', 'RURSRYOY Index', 'RUUER Index', 'RUMEREAL Index', 'BZTBBALM Index', 'CICRTOT Index', 'JSIHSTCK Index', 'JSIABOND Index', 'JSIHBOND Index', 'JSIASTCK Index', 'JNBPAB Index', 'JNBPTRD Index', 'UNIBAS Index', 'UNIBBS Index', 'UNIBHS Index', 'UKRXPBAL Index', 'BZW IPCS Index', 'BZPIIPCM Index', 'BZPIIPCY Index', 'BZCTSP Index', 'BZCTSA Index', 'BZCTSY Index', 'BZCTCP Index', 'BZCTCA Index', 'BZCTCY Index', 'MXCPYOY Index', 'MXCPCHNG Index', 'MXCCCHNG Index', 'MXBWYOY Index', 'MXBWMOM Index', 'MXBWCORE Index', 'RUREFEG Index', 'W3CAST Index', 'W1CAST Index', 'SALECNUM Index', 'SALECORN Index', 'C5CAST Index', 'SALESYBN Index', 'BYCAST Index', 'SALESOYB Index', 'SALEWEAL Index', 'SALEWHET Index', 'SALECNUA Index', 'SALECOTT Index', 'SALESCML Index', 'SALESYOL Index', 'INJCJC Index', 'INJCSP Index', 'MWINCHNG Index', 'DOENUSCH Index', 'DOENIFTL Index', 'CUSEENDS Index', 'CUSEYIEL Index', 'CUSEPROD Index', 'CUSEEXPO Index', 'SUSEENDS Index', 'SUSEYIEL Index', 'SUSEPROD Index', 'SUSEEXPT Index', 'WUSETWES Index', 'WUSETWPR Index', 'WUSETWEX Index', 'TUSEENDS Index', 'TUSEPROD Index', 'TUSEEXPO Index', 'LUSEPACE Index', 'LUSEPASP Index', 'LUSEPBSP Index', 'MXONBR Index', 'JMNSM2Y Index', 'JMNSM3Y Index', 'NOCPIMOM Index', 'NOCPIYOY Index', 'NOCPULMM Index', 'NOCPULYY Index', 'NOPPIMOM Index', 'NOPPIYOY Index', 'GRCP20YY Index', 'GRCP20MM Index', 'GRCP2HMM Index', 'GRCP2HYY Index', 'SWNOIMOM Index', 'SWNONSYY Index', 'BZW CPI Index', 'ITPRSANM Index', 'ITPRWAY Index', 'ITPRNIY Index', 'MXPSTMOM Index', 'MXIPTYOY Index', 'CANLNETJ Index', 'CANLXEMR Index', 'BAKETOT Index', 'SZMSTSDF Index', 'RUTBAL Index', 'GRINCORN Index', 'GRINSOYB Index', 'GRINWHET Index', 'FDDSSD Index', 'JNWSDYOY Index', 'JNWSDOM Index', 'MXSATOTL Index', 'SWAUAMS Index', 'JNMTOY Index', 'FRUEREUO Index', 'UKUEILOR Index', 'UKUER Index', 'UKUEMOM Index', 'UKAWMWHO Index', 'SZCPIYOY Index', 'SZCPIMOM Index', 'GRZEWI Index', 'GRZECURR Index', 'GRZEEUEX Index', 'SBOITOTL Index', 'CPI CHNG Index', 'CPUPXCHG Index', 'CPI YOY Index', 'CPI XYOY Index', 'CPURNSA Index', 'CPUPAXFE Index', 'GRCAEU Index', 'NOGDCOSQ Index', 'NOGDMQQ Index', 'UKRPCJMR Index', 'UKRPCJYR Index', 'UKHCA9IQ Index', 'UKRPI Index', 'UKRPMOM Index', 'UKRPYOY Index', 'UKRPXYOY Index', 'EUGNEMUQ Index', 'EUGNEMUY Index', 'EMEMULYY Index', 'EUITEMUM Index', 'EUIPEMUY Index', 'RUCPBI Index', 'RUCPIMOM Index', 'RUCPIYOY Index', 'ARNCYINX Index', 'ARNCNINX Index', 'ARC6INDM Index', 'JGDPQGDP Index', 'JGDPAGDP Index', 'JGDOQOQ Index', 'JGDFDEFY Index', 'JNIPMOM Index', 'JNIPYOY Index', 'JNCAPMOM Index', 'UKIPIMOM Index', 'UKIPIYOY Index', 'UKMPIMOM Index', 'UKMPIYOY Index', 'UKISCT3M Index', 'UKTBALEE Index', 'UKTBTTBA Index', 'UKGRABIQ Index', 'UKGRABIY Index', 'UKGEABRQ Index', 'UKGENMYQ Index', 'UKGEIKKQ Index', 'UKGEIKLQ Index', 'UKBINPEQ Index', 'UKBINPEY Index', 'SZPMIYOY Index', 'SZPMIMOM Index', 'BZEAMOM% Index', 'BZEAYOY% Index', 'CAHSTOTL Index', 'CAMFCHNG Index', 'EMPRGBCI Index', 'RSTAMOM Index', 'RSTAXMOM Index', 'RSTAXAG% Index', 'OUTFGAF Index', 'IMP1CHNG Index', 'IP CHNG Index', 'CPTICHNG Index', 'USHBMIDX Index', 'BZTWBALW Index', 'FRNTTNET Index', 'FRNTTOTL Index', 'JNTIAMOM Index', 'UKRVINFM Index', 'UKRVINFY Index', 'UKRVAMOM Index', 'UKRVAYOY Index', 'SZIPIYOY Index', 'FRCPEECM Index', 'FRCPEECY Index', 'FRCPIMOM Index', 'FRCPIYOY Index', 'FRCPXTOB Index', 'RREFKANN Index', 'IBREGP1M Index', 'CAWTMOM Index', 'NHSPATOT Index', 'NHSPSTOT Index', 'CAITFICS Index', 'FDIDFDMO Index', 'FDIDSGMO Index', 'FDIUFDYO Index', 'FDIUSGYO Index', 'CONSSENT Index', 'JNDSNYOY Index', 'JNMOCHNG Index', 'JNMOYOY Index', 'UKRMNAPM Index', 'UKRMNAPY Index', 'SWCPMOM Index', 'SWCPYOY Index', 'SWCPUIFM Index', 'SWCPUIFY Index', 'SWCPI Index', 'CAIPMOM Index', 'CARAMOM Index', 'JNC SALE Index', 'SZTBEXMM Index', 'SZTBIMMM Index', 'SWCUCAPU Index', 'SZMSM3Y Index', 'CACPICHG Index', 'CACPIYOY Index', 'LEI CHNG Index', 'ARBABAL Index', 'JNTBAL Index', 'JNTBALA Index', 'JNTBEXPY Index', 'JNTBIMPY Index', 'ARDMSUMM Index', 'BSRFTOFD Index', 'UKPSBR Index', 'UKPSNB Index', 'UKPSJ5II Index', 'MXWRTRYO Index', 'MXMMCOPR Index', 'EUCCEMU Index', 'RUPPNEWM Index', 'RUPPNEWY Index', 'FEDMMINU Index', 'COWSTOTT Index', 'MPMIJPCA Index', 'MPMIJPMA Index', 'MPMIJPSA Index', 'INSESYNT Index', 'MPMIFRMA Index', 'MPMIFRSA Index', 'MPMIFRCA Index', 'MPMIDEMA Index', 'MPMIDESA Index', 'MPMIDECA Index', 'MPMIEZMA Index', 'MPMIEZSA Index', 'MPMIEZCA Index', 'ITCPEY Index', 'MPMIGBMA Index', 'MPMIGBSA Index', 'MPMIGBCA Index', 'ECCPEMUY Index', 'ECCPEMUM Index', 'CPEXEMUY Index', 'MXGRGDPY Index', 'IGAEYOY Index', 'MXGPQTR Index', 'MXGCTOT Index', 'CFNAI Index', 'CARSCHNG Index', 'CARSXASC Index', 'MPMIUSMA Index', 'MPMIUSSA Index', 'MPMIUSCA Index', 'ETSLTOTL Index', 'ETSLMOM Index', 'AREMORMO Index', 'AREMDEMO Index', 'LIVERMLY Index', 'UKCCI Index', 'SWENAEMY Index', 'NOCR12MT Index', 'GRGDPPGQ Index', 'GDPB95YY Index', 'GRGDPPGY Index', 'GRIFPBUS Index', 'GRIFPCA Index', 'GRIFPEX Index', 'MXCACUAC Index', 'COLDPORK Index', 'CATTLE7P Index', 'CATTLEPP Index', 'CATTLEMP Index', 'JNPIY Index', 'NHSLTOT Index', 'NHSLCHNG Index', 'DFEDGBA Index', 'JNCPIYOY Index', 'JNCPIXFF Index', 'BZBGPRIM Index', 'NOCONF Index', 'ECO1GFKC Index', 'SWLEMFIY Index', 'FRCCO Index', 'ECMAM3YY Index', 'BZCACURR Index', 'BZFDTMON Index', 'MXTBBAL Index', 'BZPIIPMO Index', 'BZPIIPYO Index', 'DGNOCHNG Index', 'DGNOXTCH Index', 'CGNOXAI% Index', 'CGSHXAI% Index', 'HPIMMOM% Index', 'SPCS20Y% Index', 'RCHSINDX Index', 'CONCCONF Index', 'GRFRIAMM Index', 'GRFRINYY Index', 'UKNBAAMM Index', 'UKNBANYY Index', 'SWPPIMOM Index', 'SWPPIYOY Index', 'SWWGNMIY Index', 'SWTBAL Index', 'SWETSURV Index', 'ITPSSA Index', 'ITBCI Index', 'ITESECSE Index', 'EUESEMU Index', 'IBREGPMY Index', 'IBREGPMM Index', 'BZLNTOTA Index', 'CACURENT Index', 'GDP CQOQ Index', 'GDPCTOT% Index', 'GDP PIQQ Index', 'GDPCPCEC Index', 'RUIPRNYY Index', 'JNNETYOY Index', 'JNRETMOM Index', 'JNRSYOY Index', 'JNHSYOY Index', 'JNHSAN Index', 'SWGDPAQQ Index', 'SWGDPWYY Index', 'SWRSAMM Index', 'SWRSIYOY Index', 'FRGEGDPQ Index', 'FRGEGDPY Index', 'FRPIMOM Index', 'FRPIYOY Index', 'SZGDPCQQ Index', 'SZGRGDPY Index', 'GRUECHNG Index', 'GRUEPR Index', 'GRCP2SAM Index', 'GRCP2NRM Index', 'GRCP2NRY Index', 'NOBRFXPR Index', 'UKMSVTVJ Index', 'UKMSVTVX Index', 'UKMSM41M Index', 'UKMSM41Y Index', 'MXUERATE Index', 'BRLFUNRT Index', 'CGE9ANN Index', 'CAGDPMOM Index', 'CAGDPYOY Index', 'PITLCHNG Index', 'PCE CRCH Index', 'PCE DEFY Index', 'PCE CMOM Index', 'PCE CYOY Index', 'CHPMINDX Index', 'USPHTMOM Index', 'AGRPYOY% Index', 'JNUE Index', 'JBTARATE Index', 'ARCCIND Index', 'MPMIRUMA Index', 'PMISSURV Index', 'SZRSRYOY Index', 'SZPUI Index', 'MPMIITMA Index', 'ITMUURS Index', 'NOPMISA Index', 'NOUE Index', 'ECCPEST Index', 'UMRTEMU Index', 'ITCPEM Index', 'ITCPNICY Index', 'ITCPNICM Index', 'BZGDYOY% Index', 'BZGDQOQ% Index', 'MPMIBRMA Index', 'MPMICAMA Index', 'MPMIMXMA Index', 'MXRETOT$ Index', 'CNSTTMOM Index', 'NAPMPMI Index', 'NAPMPRIC Index', 'SAARTOTL Index', 'ARTXTOTL Index', 'JNVNYOYS Index', 'JNMBYOY Index', 'MINVTYOY Index', 'MXVHTOTL Index', 'JNCPT Index', 'JNCPTXFF Index', 'MPMIRUCA Index', 'MPMIRUSA Index', 'PMSSSURS Index', 'FPIPMOM Index', 'FPIPYOY Index', 'FRMPMOM Index', 'FRMPYOY Index', 'MPMIITCA Index', 'MPMIITSA Index', 'ITPIRLYS Index', 'ITPIRLQS Index', 'UKVHRYY Index', 'UKCR Index', 'EUPPEMUM Index', 'EUPPEMUY Index', 'MPMIBRCA Index', 'MPMIBRSA Index', 'TMNOCHNG Index', 'NAPMNMI Index', 'ARVSARTL Index', 'GRBTEXMM Index', 'MPMIDEXA Index', 'MPMIGBXA Index', 'RSSAEMUM Index', 'RSWAEMUY Index', 'BZIPTL% Index', 'BZIPYOY% Index', 'ADP CHNG Index', 'CABROVER Index', 'JOLTTOTL Index', 'ARCOYOY Index', 'SWCA Index', 'GRIORTMM Index', 'GEIOYY Index', 'IBREGPDM Index', 'EURR002W Index', 'EUORMARG Index', 'EUORDEPO Index', 'CAHOMOM Index', 'PRODNFR% Index', 'JHHSLERY Index', 'GRPFIMOM Index', 'GRPFIYOY Index', 'ITPNIMOM Index', 'ITPNIYOY Index', 'EUHNEMUQ Index', 'NFP TCH Index', 'USMMMNCH Index', 'USURTOT Index', 'CACAPUTL Index', 'C5CAAR Index', 'W1CAAR Index', 'ITEMUNES Index', 'MXSDSUYO Index', 'BOJDPBAL Index', 'BOJDPRLT Index', 'FDTR Index', 'FDTRFTRL Index', 'ARGQPYOX Index', 'ARUERATE Index', 'ARADTOTQ Index', 'BZSTSETA Index', 'SZLTDEP Index', 'NOBRDEPA Index', 'UKBRBASE Index', 'USCABAL Index', 'ARBPCURR Index', 'SWRRATEI Index', 'UKCA Index', 'PPLNALLW Index', 'PPLNBARL Index', 'PPLNCANO Index', 'PPLNCORN Index', 'PPLNCOTN Index', 'PPLNDURW Index', 'PPLNOATS Index', 'PPLNREDS Index', 'PPLNRICE Index', 'PPLNSORG Index', 'PPLNSOYB Index', 'PPLNSUNF Index', 'PPLNWINW Index', 'UGRSCNTO Index', 'UGRSSBTO Index', 'UGRSAWTO Index', 'UGRSBATO Index', 'UGRSOATO Index', 'UGRSSOTO Index', 'SUEYALLS Index', 'RUCACAL Index', 'JTFIFILA Index', 'JNTSMFG Index', 'JPTFLNMF Index', 'JPTFLMFG Index', 'JNTSNMFG Index', 'BCBSFUTR Index', 'PLNTCORN Index', 'PLNTCOTN Index', 'PLNTSOYB Index', 'CONDWWHT Index', 'RUDPRYOY Index', 'BZCTSAT Index', 'ECI SA% Index', 'CONDCORN Index', 'CONDCOTT Index', 'CONDSOYB Index', 'ACRECRNP Index', 'ACRESOYP Index', 'ACREWHTP Index', ]


df = pd.DataFrame()
df.index = events

for event in df.index:
    df['country'] = mgr[event].COUNTRY

print(df)