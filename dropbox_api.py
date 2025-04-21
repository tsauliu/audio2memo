#%%
import dropbox
from env import access_token_dropbox

TOKEN = access_token_dropbox

dbx = dropbox.Dropbox(TOKEN)
print(dbx.users_get_current_account())