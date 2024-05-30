# Define the path to your audio file
$filePath = "C:\123.m4a"

# Create a Shell.Application object
$shell = New-Object -ComObject Shell.Application

# Get the folder part of the path (removes the file name)
$folderPath = [System.IO.Path]::GetDirectoryName($filePath)

# Get the file name part of the path
$fileName = [System.IO.Path]::GetFileName($filePath)

# Get the folder object
$folder = $shell.Namespace($folderPath)

# Get the file object
$file = $folder.ParseName($fileName)

# Get the property index for "Media Created" (might vary, commonly 208)
$mediaCreatedIndex = 208

# Get the "Media Created" property value
$mediaCreated = $folder.GetDetailsOf($file, $mediaCreatedIndex)

# Output the "Media Created" date
Write-Output "Media Created: $mediaCreated"
