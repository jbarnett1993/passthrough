# GS Quant documentation available at:
# https://developer.gs.com/docs/gsquant/getting-started/

import datetime

from gs_quant.data import Dataset
from gs_quant.session import GsSession, Environment

GsSession.use(Environment.PROD, '5856b7c9c08140d69313b1b723108c25', 'ff46deb0a3ca4ce3ecd4af97b083072e10be41eb48441921984130a0ad93a7c8', ('read_product_data',))

ds = Dataset('GSDEER_GSFEER')
data = ds.get_data(datetime.date(2005, 7, 15), assetId=["MAJTN2XJVF97SYJK", "MA5NJGMGTZ1MJJEN", "MAKRJX8YT2GETP3S"], limit=50)
print(data.head())  # peek at first few rows of data




'''
Our institutional APIs implement the OAuth 2.0 standard for secure authentication and authorization. In order to make a request to any of the APIs defined in the API Directory, you will need to provide an authentication token.

To retrieve an authentication token, you will need to POST to the authentication service located at https://idfs.gs.com/as/token.oauth2 with the following parameters:

Parameter	Description
grant_type	The only currently supported grant type is client_credentials
client_id	The unique client id of your application as provided on the My Apps page
client_secret	The secret provided when you first registered the application. This should always be stored securely and regenerated if compromised
scope (optional)	Space delimited list of scopes for which you need to obtain access. Your application must have been approved for any scopes you request


'''