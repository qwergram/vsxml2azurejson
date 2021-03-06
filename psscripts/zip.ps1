# Simple script that zips whatever directory is passed in
# Really just a helper script for Python Script
param(
 [Parameter(Mandatory=$True)]
 [string]
 $zipfilename,

 [Parameter(Mandatory=$True)]
 [string]
 $sourcedir
)


Compress-Archive -Path $sourcedir\* -DestinationPath $zipfilename -Force
