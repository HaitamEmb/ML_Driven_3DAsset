param (
    [string]$randomValue
)
hython -c "
import sys
hou.hipFile.load('C:/users/Haitam/backup/HairCards_recovered_bak22.hip')
hou.session.my_random_number = '$randomValue'
exec(hou.session.maincode)
"

