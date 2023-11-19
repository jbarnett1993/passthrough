'''[                    
with PdfPages('output.pdf') as pdf:
    for df in updated_dfs[:10]:  # Process first 10 DataFrames
        plt.figure(figsize=(8, 6))
        plt.title(df['ISSUER'].iloc[0])  # Title from the 'ISSUER' column

        # Plot table
        plt.table(cellText=df.values, colLabels=df.columns, loc='center')
        plt.axis('off')  # Hide axes

        # Save page
        pdf.savefig()
        plt.close()

print("PDF generated.")








DATE CURRENCY  PX_LAST()
 ID                                          
 BM966163 Corp 2023-11-19     None  100.63350
 ZR632585 Corp 2023-11-19     None  101.18700
 BK912979 Corp 2023-11-19     None  102.93030
 BK256707 Corp 2023-11-19     None  114.07690
 BK912977 Corp 2023-11-19     None  102.53510
 BK256706 Corp 2023-11-19     None  107.78170
 ZR631768 Corp 2023-11-19     None  101.52190
 BK912976 Corp 2023-11-19     None  100.03150
 AZ988250 Corp 2023-11-19     None   97.68068
 ZR630930 Corp 2023-11-19     None   99.59774
 BM966162 Corp 2023-11-19     None   99.27781
 ZR632575 Corp 2023-11-19     None   98.18829
 ZR631722 Corp 2023-11-19     None  104.77440
 ZR631760 Corp 2023-11-19     None  108.15180
 ZR631832 Corp 2023-11-19     None   56.37306
 AZ988252 Corp 2023-11-19     None   87.35365
 ZR631707 Corp 2023-11-19     None  103.57520
 ZR631951 Corp 2023-11-19     None  111.11690
 ZR631767 Corp 2023-11-19     None  109.77420
 JK596826 Corp 2023-11-19     None   75.84887
 JK596825 Corp 2023-11-19     None   94.30695
 ZR630910 Corp 2023-11-19     None  100.71490
 AL094037 Corp 2023-11-19     None   66.44766
 EK988422 Corp 2023-11-19     None   73.60909
 AL094029 Corp 2023-11-19     None   90.82990
 AZ988253 Corp 2023-11-19     None   74.32272
 AZ988251 Corp 2023-11-19     None   92.85217
 AZ988254 Corp 2023-11-19     None   69.62200
 DD117028 Corp 2023-11-19     None  104.42390
 EC100175 Corp 2023-11-19     None  109.25040
 ZR631703 Corp 2023-11-19     None  103.24160
 ZR630947 Corp 2023-11-19     None  104.33680
 AR534233 Corp 2023-11-19     None   72.82563
 ZR632600 Corp 2023-11-19     None  105.58420
 ZR632578 Corp 2023-11-19     None   73.65400
 ZR631756 Corp 2023-11-19     None  106.67190
 EK988416 Corp 2023-11-19     None   96.17446
 ZR631557 Corp 2023-11-19     None  103.66380
 ZR630883 Corp 2023-11-19     None   97.65202
 ZR631719 Corp 2023-11-19     None  100.72220
 ZR632597 Corp 2023-11-19     None  105.27550,
                     DATE CURRENCY  PX_LAST()
 ID                                          
 ZH446011 Corp 2023-11-19     None  100.68730
 BN085798 Corp 2023-11-19     None   93.56502
 BU453315 Corp 2023-11-19     None   91.91698
 ZQ863015 Corp 2023-11-19     None   95.82129
 BU453308 Corp 2023-11-19     None   96.13868
 BK564477 Corp 2023-11-19     None  111.37550
 BS497002 Corp 2023-11-19     None   80.12500
 BU453113 Corp 2023-11-19     None   83.36562
 ZM553141 Corp 2023-11-19     None  102.42660
 BJ330279 Corp 2023-11-19     None  122.96720
 ZJ729144 Corp 2023-11-19     None  105.35640,
                     DATE CURRENCY  PX_LAST()
 ID                                          
 LW952937 Corp 2023-11-19     None   79.41013
 LW952924 Corp 2023-11-19     None   94.43080
 BN157466 Corp 2023-11-19     None   95.40620
 BN156991 Corp 2023-11-19     None   85.38146
 BN158615 Corp 2023-11-19     None   92.38911
 EJ477914 Corp 2023-11-19     None  103.95300
 EJ477939 Corp 2023-11-19     None   88.41922
 BN154741 Corp 2023-11-19     None   90.94359
 BN161676 Corp 2023-11-19     None   93.32838
 EJ477889 Corp 2023-11-19     None  107.24880
 LW952929 Corp 2023-11-19     None   94.06137
 AS940638 Corp 2023-11-19     None   96.76319
 EH914679 Corp 2023-11-19     None  108.13960
 EC007233 Corp 2023-11-19     None  104.17020
 LW952932 Corp 2023-11-19     None   89.24451
 EC915098 Corp 2023-11-19     None  106.98110
 BN156776 Corp 2023-11-19     None   86.05167
 EJ220693 Corp 2023-11-19     None   88.33118
 ZR580923 Corp 2023-11-19     None   85.39307
 BJ280347 Corp 2023-11-19     None   92.37930
 LW079953 Corp 2023-11-19     None   79.67057
 EK995917 Corp 2023-11-19     None   89.19147
 LW079947 Corp 2023-11-19     None   94.43546
 BJ264115 Corp 2023-11-19     None   95.34811
 ZR580911 Corp 2023-11-19     None   90.92092
 ZR580918 Corp 2023-11-19     None   85.86444,
                     DATE CURRENCY  PX_LAST()
 ID                                          
 BG537498 Corp 2023-11-19     None     95.226
 BN333331 Corp 2023-11-19     None     55.392
 EK790227 Corp 2023-11-19     None     92.522
 JK396661 Corp 2023-11-19     None     94.482
 BV073615 Corp 2023-11-19     None     87.327
 JK396654 Corp 2023-11-19     None     99.119
 BV073617 Corp 2023-11-19     None     83.575
 EK788113 Corp 2023-11-19     None     78.640,
                     DATE CURRENCY  PX_LAST()
 ID                                          
 ZL513928 Corp 2023-11-19     None  103.75800
 BN397412 Corp 2023-11-19     None   83.84124
 BP927746 Corp 2023-11-19     None   93.12600
 ZQ584370 Corp 2023-11-19     None   94.24108
 ZO479959 Corp 2023-11-19     None   92.92959,
                     DATE CURRENCY  PX_LAST()
 ID                                          
 EG417602 Corp 2023-11-19     None   79.54027
 ZL475108 Corp 2023-11-19     None   99.93105
 BU931916 Corp 2023-11-19     None   80.87653
 BR850334 Corp 2023-11-19     None   95.71048
 QZ179765 Corp 2023-11-19     None   92.84791
 EG892908 Corp 2023-11-19     None   99.36151
 AM671336 Corp 2023-11-19     None   87.80669
 AS505134 Corp 2023-11-19     None   94.50834
 BH537386 Corp 2023-11-19     None   90.70834
 ZR553139 Corp 2023-11-19     None   82.05784
 EK095417 Corp 2023-11-19     None   88.83194
 EH677232 Corp 2023-11-19     None  111.95720
 BR850343 Corp 2023-11-19     None   79.16682
 EI265198 Corp 2023-11-19     None   97.82784
 AU936149 Corp 2023-11-19     None   85.56915
 EK915836 Corp 2023-11-19     None   93.53600
 JV801803 Corp 2023-11-19     None   98.25002
 AS506470 Corp 2023-11-19     None   85.14915
 ZL475109 Corp 2023-11-19     None  100.23230
 ED389496 Corp 2023-11-19     None   95.46857
 EF329277 Corp 2023-11-19     None   96.75507
 AS506574 Corp 2023-11-19     None   82.65804
 EJ865815 Corp 2023-11-19     None   85.11806
 EH502118 Corp 2023-11-19     None  108.63160
 MM131914 Corp 2023-11-19     None  102.09750
 EC147169 Corp 2023-11-19     None  108.89080
 MM119837 Corp 2023-11-19     None  101.28460,
                     DATE CURRENCY  PX_LAST()
 ID                                          
 AN420284 Corp 2023-11-19     None   95.30232
 AS664644 Corp 2023-11-19     None   98.85560
 AS664834 Corp 2023-11-19     None   90.84615
 EG588738 Corp 2023-11-19     None  109.80980
 BK183051 Corp 2023-11-19     None   83.97102
 AN499923 Corp 2023-11-19     None   81.73003
 ZQ348297 Corp 2023-11-19     None   86.99641
 ZQ348321 Corp 2023-11-19     None   70.44221
 BK183061 Corp 2023-11-19     None   66.39671
 AZ595170 Corp 2023-11-19     None   75.72911
 AZ595154 Corp 2023-11-19     None   90.73734
 EJ406082 Corp 2023-11-19     None   83.42415
 AV123660 Corp 2023-11-19     None   92.03835
 AV123656 Corp 2023-11-19     None   98.59682,
                     DATE CURRENCY  PX_LAST()
 ID                                          
 ZK558882 Corp 2023-11-19     None     99.827
 ZK558887 Corp 2023-11-19     None    100.580
 AM965706 Corp 2023-11-19     None     96.297
 ZO293332 Corp 2023-11-19     None     86.260
 BP573970 Corp 2023-11-19     None     83.052
 BR693149 Corp 2023-11-19     None     79.287
 BP573966 Corp 2023-11-19     None     89.104
 BR693147 Corp 2023-11-19     None     88.684
 AS666342 Corp 2023-11-19     None     94.753
 ZO293345 Corp 2023-11-19     None     76.971
 BP573971 Corp 2023-11-19     None     75.735,


 


 resp = LocalTerminal.get_reference_data(ids,["NXT_CALL_DT","NXT_CALL_PX","PX_LAST",
                                             "YAS_ISPREAD_TO_GOVT","ISSUER" ],ignore_field_error=1)
'''