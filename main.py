from tia.bbg import LocalTerminal
import pandas as pd
import numpy as np
import tia.bbg.datamgr as dm
from dateutil.relativedelta import relativedelta
from datetime import datetime


sids = 'EURUSD Curncy'
start = datetime.now() - relativedelta(minutes=5)
end = start + relativedelta(minutes=1)

f = LocalTerminal.get_intraday_tick(sids, "TRADE", start, end,).as_frame()

mgr = dm.BbgDataManager()

events = ['DNCPIMOM Index', 'DNCPIYOY Index', 'DNCPEECM Index', 'DNCPEECY Index', 'SZMSSDDB Index', 'SZMSTSDF Index', 'BNCCINDX Index', 'NYCNM1IR Index', 'FDDSSD Index', 'WMCCCON% Index', 'WMCCCONS Index', 'JNWSDYOY Index', 'JNWSDOM Index', 'MXSATOTL Index', 'CNDIACRY Index', 'MXNSNOML Index', 'NABSCONF Index', 'NABSCOND Index', 'NZIFRBY2 Index', 'SWAUAMS Index', 'JNMTOY Index', 'FRUEREUO Index', 'FRUEREU Index', 'UKUEILOR Index', 'UKLFEMCH Index', 'UKUER Index', 'UKUEMOM Index', 'UKPYPEMC Index', 'UKAWMWHO Index', 'UKAWXTOM Index', 'SZCPIYOY Index', 'SZCPIMOM Index', 'SZHMMOM Index', 'SZHMYOY Index', 'SZEXIYOY Index', 'GRZEWI Index', 'GRZECURR Index', 'GRZEEUEX Index', 'SBOITOTL Index', 'CPI CHNG Index', 'CPUPXCHG Index', 'CPI YOY Index', 'CPI XYOY Index', 'CPURNSA Index', 'CPUPAXFE Index', 'REALYRAE Index', 'REALYRAW Index', 'MXIRINUS Index', 'NZHSTOTY Index', 'NZCSSM Index', 'NZCSRSM Index', 'NZFPCHGE Index', 'GRCAEU Index', 'NOGDCOSQ Index', 'NOGDMQQ Index', 'NOGDMM Index', 'NOGDMMM Index', 'UKRPCJMR Index', 'UKRPCJYR Index', 'UKHCA9IQ Index', 'UKHPSERY Index', 'UKHCCPIY Index', 'UKRPI Index', 'UKRPMOM Index', 'UKRPYOY Index', 'UKRPXYOY Index', 'UKPPB7SM Index', 'UKPPB7SY Index', 'UKPPHIPM Index', 'UKPPHIPY Index', 'UKLHUKY Index', 'EUGNEMUQ Index', 'EUGNEMUY Index', 'EMEMULQQ Index', 'EMEMULYY Index', 'EUITEMUM Index', 'EUIPEMUY Index', 'MBAVCHNG Index', 'ECONCREA Index', 'NZMILTS Index', 'JGDPQGDP Index', 'JGDPAGDP Index', 'JGDOQOQ Index', 'JGDFDEFY Index', 'JGDPPCQ Index', 'JGDPCIQ Index', 'JGDPCPIN Index', 'JGDPCNEX Index', 'MECCTRIM Index', 'AULFEMPC Index', 'AULFUNEM Index', 'AULFPART Index', 'AULFEMFC Index', 'AULFEMCP Index', 'AUCHSYOY Index', 'AUCHSMOM Index', 'JNIPMOM Index', 'JNIPYOY Index', 'JNCAPMOM Index', 'UKGDM3M Index', 'UKIPIMOM Index', 'UKIPIYOY Index', 'UKMPIMOM Index', 'UKMPIYOY Index', 'UKISCTMM Index', 'UKISCT3M Index', 'UKCNALSM Index', 'UKCNALSY Index', 'UKTBALEE Index', 'UKTBTTBA Index', 'UKTBGTEM Index', 'UKTBTTEM Index', 'UKGRABIQ Index', 'UKGRABIY Index', 'UKGEABRQ Index', 'UKGENMYQ Index', 'UKGENPTQ Index', 'UKGEIKKQ Index', 'UKGEIKLQ Index', 'UKBINPEQ Index', 'UKBINPEY Index', 'UKPRLZVD Index', 'DKKPMOM Index', 'DKKPYOY Index', 'NOTBTOT Index', 'SZPMIYOY Index', 'SZPMIMOM Index', 'SPIPCMOM Index', 'SPIPCYOY Index', 'SPCPEUMM Index', 'SPCPEUYY Index', 'SPIPCCYY Index', 'SPIPCCMM Index', 'SZCCIS Index', 'ITTRALEE Index', 'ITTRALEX Index', 'ITGGTOTE Index', 'XTSBEZ Index', 'XTTBEZ Index', 'CAHSTOTL Index', 'CAMFCHNG Index', 'EMPRGBCI Index', 'RSTAMOM Index', 'RSTAXMOM Index', 'RSTAXAG% Index', 'RSTAXAGM Index', 'OUTFGAF Index', 'IMP1CHNG Index', 'IMP1XPM% Index', 'IMP1YOY% Index', 'EXP1CMOM Index', 'EXP1CYOY Index', 'INJCJC Index', 'INJCSP Index', 'IP CHNG Index', 'CPTICHNG Index', 'IPMGCHNG Index', 'MTIBCHNG Index', 'USHBMIDX Index', 'BZTWBALW Index', 'FRNTTNET Index', 'FRNTTOTL Index', 'NZPMISA Index', 'JSIHSTCK Index', 'JSIABOND Index', 'JSIHBOND Index', 'JSIASTCK Index', 'BZJCTOTS Index', 'JNTIAMOM Index', 'GRWPYOYI Index', 'GRWPMOMI Index', 'SWUERATN Index', 'SWUESATN Index', 'SWUESANE Index', 'UKRVINFM Index', 'UKRVINFY Index', 'UKRVAMOM Index', 'UKRVAYOY Index', 'SZIPIYOY Index', 'SZIP2NDY Index', 'FRCPEECM Index', 'FRCPEECY Index', 'FRCPIMOM Index', 'FRCPIYOY Index', 'FRCPXTOB Index', 'BZW CPI Index', 'IBREGP1M Index', 'BZW IPCS Index', 'CAWTMOM Index', 'NHSPSTOT Index', 'NHCHSTCH Index', 'NHSPATOT Index', 'NHCHATCH Index', 'NYBLCNBA Index', 'CAITFICS Index', 'FDIDFDMO Index', 'FDIDSGMO Index', 'FDIDSGUM Index', 'FDIUFDYO Index', 'FDIUSGYO Index', 'FDIUSGUY Index', 'CONSSENT Index', 'CONSCURR Index', 'CONSEXP Index', 'CONSPXMD Index', 'CONSP5MD Index', 'CHLLM1YR Index', 'CHLLM1YV Index', 'NZPSI Index', 'JNMOCHNG Index', 'JNMOYOY Index', 'CHCUCAB Index', 'UKRMNAPM Index', 'UKRMNAPY Index', 'NZSHGB Index', 'SWCPMOM Index', 'SWCPYOY Index', 'SWCPUIFM Index', 'SWCPUIFY Index', 'SWCPIFM Index', 'SWCPIFY Index', 'SWCPI Index', 'SPTBEUBL Index', 'BZEAMOM% Index', 'BZEAYOY% Index', 'CAIPMOM Index', 'CARAMOM Index', 'CHLRLPR5 Index', 'CHLRLPR1 Index', 'JNC SALE Index', 'WCAR25 Y Index', 'SZTBEXMM Index', 'SZTBIMMM Index', 'SZTBWAY Index', 'DEGDPNQQ Index', 'DEGDPNYY Index', 'SWCUCAPU Index', 'SZMSM3Y Index', 'EUSATOTN Index', 'ITCAEUR Index', 'EUCPTSAM Index', 'EUCPTWDY Index', 'CACPTYOY Index', 'PNMARADI Index', 'CACPICHG Index', 'CACPIYOY Index', 'CACPI Index', 'CACPMYOY Index', 'LEI CHNG Index', 'NZPPOUTQ Index', 'NZPPINQ Index', 'AULILGM% Index', 'JNTBAL Index', 'JNTBALA Index', 'JNTBEXPY Index', 'JNTBIMPY Index', 'BSRFTOFD Index', 'AUWCYSA Index', 'AUWCQSA Index', 'UKPSBR Index', 'UKPSM98R Index', 'UKPSNB Index', 'UKPSJ5II Index', 'MTEF1C Index', 'MTEF4C Index', 'MXWRTRYO Index', 'MXWRTREM Index', 'EUCCEMU Index', 'FEDMMINU Index', 'NZMTEXP Index', 'NZMTBAL Index', 'NZMTBYTD Index', 'NZMTIMP Index', 'MPMIAUCA Index', 'MPMIAUMA Index', 'MPMIAUSA Index', 'BDFRTOTY Index', 'MPMIJPCA Index', 'MPMIJPMA Index', 'MPMIJPSA Index', 'SWFTCNY Index', 'JNDSTYOY Index', 'JNDSNYOY Index', 'DECCI Index', 'INSECOMP Index', 'INSESYNT Index', 'INSEPROD Index', 'INSESURV Index', 'SPHTHYOY Index', 'SPMTCYOY Index', 'SPMTHIYY Index', 'MPMIFRMA Index', 'MPMIFRSA Index', 'MPMIFRCA Index', 'MPMIDEMA Index', 'MPMIDESA Index', 'MPMIDECA Index', 'MPMIEZMA Index', 'MPMIEZSA Index', 'MPMIEZCA Index', 'ITCPEY Index', 'ITCPI Index', 'MPMIGBMA Index', 'MPMIGBSA Index', 'MPMIGBCA Index', 'ECCPEMUY Index', 'ECCPEMUM Index', 'CPEXEMUY Index', 'MXAGDPCH Index', 'MXGRGDPY Index', 'IGAEMOM Index', 'IGAEYOY Index', 'MXGPQTR Index', 'MXGCTOT Index', 'MXBWYOY Index', 'MXBWMOM Index', 'MXBWCORY Index', 'MXBWCORE Index', 'CFNAI Index', 'CARSCHNG Index', 'CARSXASC Index', 'MPMIUSMA Index', 'MPMIUSSA Index', 'MPMIUSCA Index', 'ETSLTOTL Index', 'ETSLMOM Index', 'NZRREXIN Index', 'UKCCI Index', 'CHHEAVGM Index', 'SWENAEMY Index', 'NOCR12MT Index', 'GRGDPPGQ Index', 'GDPB95YY Index', 'GRGDPPGY Index', 'GRGDPCQ Index', 'GRGDGCQ Index', 'GRGDGCIQ Index', 'GRIFPBUS Index', 'GRIFPCA Index', 'GRIFPEX Index', 'ECIENDEA Index', 'ECIETDEA Index', 'BZFGCCSA Index', 'MXCACUAC Index', 'CNFZNCC Index', 'GRIMP95M Index', 'GRIMP95Y Index', 'JNPIY Index', 'NOLBUTRD Index', 'SPROCHNG Index', 'SPROYOY Index', 'IBRENCMM Index', 'DTSDD1RB Index', 'DTSRR1RB Index', 'NHSLTOT Index', 'NHSLCHNG Index', 'DFEDGBA Index', 'JNCPIYOY Index', 'JNCPIXFF Index', 'JCPNEFFE Index', 'BZBGPRIM Index', 'BRLDDEBT Index', 'BRCPALLY Index', 'NOCONF Index', 'ECO1GFKC Index', 'SWLEMFIY Index', 'FRCCO Index', 'ECMAM3YY Index', 'BZCACURR Index', 'BZFDTMON Index', 'MXTBBAL Index', 'MXTBBIMP Index', 'MXTBBEXP Index', 'BZPIIPMO Index', 'BZPIIPYO Index', 'DGNOCHNG Index', 'DGNOXTCH Index', 'CGNOXAI% Index', 'CGSHXAI% Index', 'HPI PURQ Index', 'HPIMMOM% Index', 'SPCS20SM Index', 'SPCS20Y% Index', 'SPCSUSAY Index', 'RCHSINDX Index', 'CONCCONF Index', 'CONCPSIT Index', 'CONCEXP Index', 'RCSSCLBC Index', 'DSERGBCC Index', 'GRFRIAMM Index', 'GRFRINYY Index', 'UKNBAAMM Index', 'UKNBANYY Index', 'AUCNQTOT Index', 'ACPMYOY Index', 'NZOCR Index', 'JNCICLEI Index', 'JNCICCOI Index', 'DERSHMOM Index', 'DERSHYOY Index', 'SWPPIMOM Index', 'SWPPIYOY Index', 'SWWGNMIY Index', 'SWTBAL Index', 'NORSXVNM Index', 'SWETSURV Index', 'SWETCI Index', 'SWETCIM Index', 'ITPSSA Index', 'ITBCI Index', 'ITESECSE Index', 'CCFASZE Index', 'EUSCEMU Index', 'EUICEMU Index', 'EUESEMU Index', 'IBREGPMY Index', 'IBREGPMM Index', 'BZLNTOTA Index', 'BRCDDEFT Index', 'BZLNTMOM Index', 'CAEWNETC Index', 'CACURENT Index', 'GDP CQOQ Index', 'GDPCTOT% Index', 'GDP PIQQ Index', 'GDPCPCEC Index', 'USTGTTCB Index', 'RSRSTMOM Index', 'MWINCHNG Index', 'JNNETYOY Index', 'JNRETMOM Index', 'JNRSYOY Index', 'NZBCBA Index', 'NZBCI Index', 'LTSBBSBX Index', 'LTSBBPEX Index', 'AURSTSA Index', 'AUCECHG Index', 'OZCACRM% Index', 'OZCACRY% Index', 'CPMINDX Index', 'CPMINMAN Index', 'JNHSYOY Index', 'JNHSAN Index', 'FRPRPRIQ Index', 'DEUE Index', 'DEUEGRAT Index', 'SWGDPAQQ Index', 'SWGDPWYY Index', 'SWRSAMM Index', 'SWRSIYOY Index', 'FRGEGDPQ Index', 'FRGEGDPY Index', 'FRPIMOM Index', 'FRPIYOY Index', 'FRSNTTLM Index', 'FRSNTTLY Index', 'SZLILEI Index', 'SZGDPCQQ Index', 'SZGRGDPY Index', 'GRUECHNG Index', 'GRUEPR Index', 'GRCP2HEM Index', 'GRCP2HEY Index', 'GRCP2BVM Index', 'GRCP2BVY Index', 'GRCP2BRM Index', 'GRCP2BRY Index', 'GRCP2SAM Index', 'GRCP2SAY Index', 'GRCP2BWM Index', 'GRCP2BWY Index', 'GRCP2NRM Index', 'GRCP2NRY Index', 'ITISTOTY Index', 'ITISTSAM Index', 'NOBRFXPR Index', 'SPCAEURO Index', 'UKMSB3PS Index', 'UKMSB4TC Index', 'UKMSVTVJ Index', 'UKMSVTVX Index', 'UKMSM41M Index', 'UKMSM41Y Index', 'UKMS4QG Index', 'NZHHTLY Index', 'BZPBPRDM Index', 'BZPBNODM Index', 'BZDPNDT% Index', 'CFIBCANA Index', 'MXUERATE Index', 'BRLFUNRT Index', 'GRCP20YY Index', 'GRCP20MM Index', 'GRCP2HMM Index', 'GRCP2HYY Index', 'RPAUMED Index', 'CGE9ANN Index', 'CAGDPMOM Index', 'CAGDPYOY Index', 'PITLCHNG Index', 'PCE CRCH Index', 'PCE CHNC Index', 'PCE DEFM Index', 'PCE DEFY Index', 'PCE CMOM Index', 'PCE CYOY Index', 'CHPMINDX Index', 'MXBLPERF Index', 'USPHTMOM Index', 'USPHTYOY Index', 'KCLSSACI Index', 'NZANCCTM Index', 'NZANCCT Index', 'NZBAUNIM Index', 'JNUE Index', 'JBTARATE Index', 'CPMICOMP Index', 'MPMICNMA Index', 'JCOMSHCF Index', 'PMISSURV Index', 'SZRSRYOY Index', 'MPMIESMA Index', 'SZPUI Index', 'SZPUSERV Index', 'MPMIITMA Index', 'ITMUURS Index', 'NOPMISA Index', 'NOUE Index', 'NOUESA Index', 'ECCPEST Index', 'UMRTEMU Index', 'ITCPEM Index', 'ITCPNICY Index', 'ITCPNICM Index', 'ITPIRAYY Index', 'BZGDYOY% Index', 'BZGDGDP4 Index', 'BZGDQOQ% Index', 'MPMIBRMA Index', 'MPMICAMA Index', 'MPMIMXMA Index', 'MXRETOT$ Index', 'CNSTTMOM Index', 'NAPMPMI Index', 'NAPMPRIC Index', 'NAPMNEWO Index', 'NAPMEMPL Index', 'KCSSMCOM Index', 'ITVHYOY Index', 'IMEFNMIN Index', 'IMEFMAIN Index', 'ITBDNETE Index', 'SAARTOTL Index', 'MXDSBALA Index', 'NORNOC Index', 'NORNON Index', 'BZASSUBT Index', 'NZPCTOT% Index', 'JNVNYOYS Index', 'JNVNIYOY Index', 'JNCRPYOY Index', 'JNSASYOY Index', 'JNMBYOY Index', 'JNMBMOBE Index', 'TDMIYOY Index', 'TDMIMOM Index', 'INAUQOQ Index', 'AUPGOP Index', 'AULFANTC Index', 'AUBARSM Index', 'AUBAC Index', 'FRBDEURO Index', 'SPUECHNG Index', 'BZCPI Index', 'SNTEEUGX Index', 'MINVTMOM Index', 'MINVTYOY Index', 'MXVHTOTL Index', 'MXCLMLEA Index', 'MDPCAVTO Index', 'DECRMCHG Index', 'DECRESRV Index', 'JNCPT Index', 'JNCPTXFF Index', 'JCPTEFFE Index', 'ANZCWMOM Index', 'KPRSLFLS Index', 'AUCANXP Index', 'AUCABAL Index', 'MPMICNCA Index', 'MPMICNSA Index', 'PMSSSURS Index', 'PMISCMPS Index', 'FPIPMOM Index', 'FPIPYOY Index', 'FRMPMOM Index', 'FRMPYOY Index', 'MPMIESSA Index', 'MPMIESCA Index', 'MPMIITCA Index', 'MPMIITSA Index', 'ITPIRLYS Index', 'ITPIRLQS Index', 'UKVHRYY Index', 'UKCR Index', 'EUPPEMUM Index', 'EUPPEMUY Index', 'MPMIBRCA Index', 'MPMIBRSA Index', 'MPMICACA Index', 'MPMICASA Index', 'TMNOCHNG Index', 'TMNOXTM% Index', 'NAPMNMI Index', 'NAPMNPRC Index', 'NAPMNEMP Index', 'NAPMNNO Index', 'NZBDVQ Index', 'MXWITMOL Index', 'AUNAGDPC Index', 'AUNAGDPY Index', 'GRBTBALE Index', 'GRBTEXMM Index', 'GRBTIMMM Index', 'NOBPLVL Index', 'MPMIDEXA Index', 'MPMIGBXA Index', 'RSSAEMUM Index', 'RSWAEMUY Index', 'MXCDCOSA Index', 'BZIPTL% Index', 'BZIPYOY% Index', 'MXVETOTL Index', 'MXVPTOTL Index', 'ADP CHNG Index', 'CALPPROD Index', 'CABROVER Index', 'IVEYSA Index', 'MWSLCHNG Index', 'JOLTTOTL Index', 'BZTBIMPM Index', 'BZTBEXPM Index', 'BZTBBALM Index', 'NZMACHGE Index', 'NZMAVOQ Index', 'SWCA Index', 'BZVXEXTL Index', 'BZVPTLVH Index', 'BZVLTLVH Index', 'AUITGSB Index', 'AUITEXG% Index', 'AUITIMG% Index', 'AULJHOVM Index', 'AULJHTVM Index', 'AULJHIVM Index', 'MIKIMT07 Index', 'AUFRA Index', 'SZUE Index', 'SZUEUEA Index', 'DEMFIPSM Index', 'SWBUL Index', 'GRIORTMM Index', 'GEIOYY Index', 'NOIPSAMM Index', 'NOIPOYOY Index', 'NOIPISAM Index', 'NOIPIYOY Index', 'SZRAFCRC Index', 'SPIOYOY Index', 'SPIOWSAY Index', 'SPIOWSAM Index', 'SPNPTHQ Index', 'SPNPTHY Index', 'UKDDEPAV Index', 'UKDDCPI1 Index', 'IBREGPDM Index', 'IBREGPDY Index', 'MXCPYOY Index', 'MXCPCHNG Index', 'MXCCYOY Index', 'MXCCCHNG Index', 'CHALYOY% Index', 'EURR002W Index', 'EUORMARG Index', 'EUORDEPO Index', 'CAHOMOM Index', 'USTBTOT Index', 'CATBTOTB Index', 'PRODNFR% Index', 'COSTNFR% Index', 'NWORCHNG Index', 'CICRTOT Index', 'JHHSLERY Index', 'JNBPTRD Index', 'JNBPABA Index', 'JNBPAB Index', 'JNBLENDA Index', 'JNBLBYOY Index', 'CNTSECCY Index', 'CNFRCEXY Index', 'CNTSICCY Index', 'CNTSTCNC Index', 'CNFRCIMY Index', 'CNFRCBAL Index', 'CNGFOREX Index', 'JWEXOVSA Index', 'JWCOOVSA Index', 'GRIPIMOM Index', 'GEINYY Index', 'GRPFIMOM Index', 'GRPFIYOY Index', 'SWGDPIMM Index', 'SWGDPIYM Index', 'SWHOSAMO Index', 'SWHOWDAY Index', 'SEIBPVPM Index', 'SEIBPVPY Index', 'SEIBPVMY Index', 'SEIBPVSY Index', 'SWNOIMOM Index', 'SWNONSYY Index', 'FRTEBAL Index', 'FFCAB12S Index', 'ITPNIMOM Index', 'ITPNIYOY Index', 'NGVTEMUQ Index', 'FCFNEMUQ Index', 'EUHNEMUQ Index', 'CANLPTNC Index', 'CANLNETJ Index', 'CANLFLNC Index', 'CANLXEMR Index', 'ECONGECC Index', 'NFP TCH Index', 'NFP PCH Index', 'CAHEPERM Index', 'USMMMNCH Index', 'CANLPRTR Index', 'USURTOT Index', 'CACAPUTL Index', 'AHE MOM% Index', 'AHE YOY% Index', 'AWH TOTL Index', 'PRUSTOT Index', 'USUDMAER Index', 'CHEFTYOY Index', 'CNCPIYOY Index', 'CNLNNEW Index', 'CNMS2YOY Index', 'CNMS1YOY Index', 'CNLNASF Index', 'CNMS0YOY Index', 'JMNSM2Y Index', 'JMNSM3Y Index', 'DECASA Index', 'DETBHAL Index', 'NOCPIMOM Index', 'NOCPIYOY Index', 'NOCPULMM Index', 'NOCPULYY Index', 'NOPPIMOM Index', 'NOPPIYOY Index', 'SPRSWDSY Index', 'SPRSRGIY Index', 'JBSIBCLA Index', 'JBSIBCLM Index', 'BZPIIPCY Index', 'BZPIIPCM Index', 'MXIPTYOY Index', 'MXIPFYOY Index', 'MXPSTMOM Index', 'UKGDM3 Index', 'ITEMUNES Index', 'UKRXPBAL Index', 'BZRTAMPY Index', 'BZRTRYOY Index', 'BZRTAMPM Index', 'BZRTRETM Index', 'SPLCTYY Index', 'UKBFFTIN Index', 'ITNSSTN Index', 'ITNSTY Index', 'BRSRTTVM Index', 'BRSRTTYV Index', 'NZCC Index', 'CNRSACMY Index', 'CHRXCINY Index', 'CNFAYOY Index', 'CNUESRU Index', 'CHVAICY Index', 'CHRXSARY Index', 'RBATCTR Index', 'LNTNEMUY Index', 'MXSDSUYO Index', 'NZGRP Index', 'NZBPCA Index', 'BOJDPBAL Index', 'BOJDPRLT Index', 'ITPRSANM Index', 'ITPRWAY Index', 'ITPRNIY Index', 'FDTR Index', 'FDTRFTRL Index', 'IRRBIOER Index', 'BZSTSETA Index', 'NZNTGDPY Index', 'NZNTGDPC Index', 'SZLTDEP Index', 'NOBRDEPA Index', 'UKBRBASE Index', 'USCABAL Index', 'MXONBR Index', 'FRWAMOQ Index', 'SPNAGDPQ Index', 'SPNAGDPY Index', 'CNPRTTLY Index', 'CNPRETLY Index', 'SWRRATEI Index', 'AUEMCHGE Index', 'UKCA Index', 'SNBFXTR Index', 'JNTENMFG Index', 'JTFIFILA Index', 'JNTSMFG Index', 'JNTEMFG Index', 'JPTFSNMF Index', 'JPTFLNMF Index', 'JPTFLMFG Index', 'JPTFSMFG Index', 'JNTSNMFG Index', 'BCBSFUTR Index', 'BCBSPC1 Index', 'ITDDGQ Index', 'SZRES Index', 'NOHITOSM Index', 'CNFRBAL$ Index', 'CNFREXPY Index', 'CNFRIMPY Index', 'CNTSECNY Index', 'CNTSICNY Index', 'CNTSTCN Index', 'CNGDPC$Y Index', 'CNGDPQOQ Index', 'CHVAIOY Index', 'CNGDPYOY Index', 'CNRSCYOY Index', 'NZCPICHG Index', 'NZCPIYOY Index', 'NZCPTRAQ Index', 'NZCPNTRQ Index', 'NABQCODO Index', 'NOBUTOT Index', 'ITSR1B Index', 'EUDBEURO Index', 'RBCPWM%Y Index', 'RBCPWM%Q Index', 'RBCPTRIQ Index', 'AUCPICHG Index', 'RBCPTRIY Index', 'AUCPIYOY Index', 'FRJSTQ Index', 'AUPPFYOY Index', 'AUPPFMOM Index', 'AUWMQQIA Index', 'AUWMQQIB Index', 'SPUNEMPR Index', 'JFYFGDPC Index', 'JFYFGDP1 Index', 'JFYFGDP2 Index', 'JFYFCPIC Index', 'JFYFCPI1 Index', 'JFYFCPI2 Index', 'SWGDPIQQ Index', 'SWGDPIYY Index', 'ITNHYOY Index', 'ITNHMOM Index', 'ECI SA% Index', 'NZLCOWPQ Index', 'NZLFYOY Index', 'NZLCPQ Index', 'NZLFUNER Index', 'NZAHQOQ% Index', 'NZLFQOQ Index', 'NZLFPART Index', 'NOWBTOTY Index', 'FRQBMOP3 Index', ]


currencies = {'Mexico':'USDMXN Curncy', 'United Kingdom': 'GBPUSD Curncy', 'Japan':'USDJPY Curncy', 'Australia':'AUDUSD Curncy', 'Switzerland':'USDCHF Curncy', 'Germany':'EURUSD Curncy','Denmark':'USDDKK Curncy', 'Sweden':'USDSEK Curncy', 'Norway':'USDNOK Curncy', 'France':'EURUSD Curncy', 'Spain':'EURUSD Curncy', 'Canada':'USDCAD Curncy','United States of America':'EURUSD Curncy', 'Brazil':'USDBRL Curncy', 'Italy':'EURUSD Curncy', 'China':'USDCNH Curncy','UNITED STATES':'TWI USSP Index','United States of America':'TWI USSP Index',"New Zealand":"NZDUSD Curncy","Eurozone":"EURUSD Curncy"}

today = datetime.today()
max_date = (datetime.today() + relativedelta(days=7))

def get_data(event_list):
    eligibles = LocalTerminal.get_reference_data(event_list,['ECO_RELEASE_DT'])
    eligibles_ = eligibles.as_frame()
    eligibles_ = eligibles_[eligibles_['ECO_RELEASE_DT']< max_date]
    sids = eligibles_.index.to_list()

    resp = LocalTerminal.get_reference_data(sids,['COUNTRY','REGION_OR_COUNTRY','LONG_COMP_NAME','RELEVANCE_VALUE','ECO_FUTURE_RELEASE_DATE','ECO_RELEASE_DT','RT_BN_SURVEY_AVERAGE','PREVIOUS_TRADING_DATE','INDX_FREQ'], ignore_field_error=1)

    df = resp.as_frame()


    df['ECO_RELEASE_DT'] = pd.to_datetime(df['ECO_RELEASE_DT'])

    # df = df[df['ECO_RELEASE_DT'] < max_date]
    df = df[df['RELEVANCE_VALUE'] > 80]
    df = df[df['ECO_FUTURE_RELEASE_DATE'].str.contains(':')]
    df['ECO_FUTURE_RELEASE_DATE'] = pd.to_datetime(df['ECO_FUTURE_RELEASE_DATE'])
    df['PREVIOUS_TRADING_DATE'] = pd.to_datetime(df['PREVIOUS_TRADING_DATE'])
    df = df[~(df['COUNTRY']=="RU")]
    df = df[~(df['REGION_OR_COUNTRY']=="UNITED STATES")]
    df = df[~(df['REGION_OR_COUNTRY']=="BRITAIN")]


    df['currency'] = df['REGION_OR_COUNTRY'].map(currencies)
    df = df.sort_values(by='ECO_FUTURE_RELEASE_DATE')
    return df

tick_data = []

def get_tick_data(dataframe):
    for index, row in dataframe.iterrows():
    # Extract currency symbol and eco future release date
        sid = row['currency']  
        next_release = row['ECO_FUTURE_RELEASE_DATE']
        prior_release = row['PREVIOUS_TRADING_DATE']
        # Set the start time to the release time and end time to one hour later
        start = datetime.combine(prior_release.date(), next_release.time())
        end = start + relativedelta(minutes=1)
        f = LocalTerminal.get_intraday_tick(sid, "TRADE", start, end).as_frame()
        if not f.empty:
            initial_price = f.iloc[0]['value']
            end_price = f.iloc[-1]['value']
            pct_change_bps = ((initial_price - end_price)/initial_price ) * 10000
        else:
            pct_change_bps = np.nan
        tick_data.append(pct_change_bps)
