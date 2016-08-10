# https://blogs.technet.microsoft.com/uktechnet/2016/02/12/create-a-custom-script-extension-for-an-azure-resource-manager-vm-using-powershell/
# Ensure PS remoting is enabled, although this is enabled by default for Azure VMs
Enable-PSRemoting -Force

# Create rule in Windows Firewall
Try {
    Get-NetFirewallRule -Name "WinRM HTTPS" -ErrorAction Stop
} Catch {
    New-NetFirewallRule -Name "WinRM HTTPS" -DisplayName "WinRM HTTPS" -Enabled True -Profile Any -Action Allow -Direction Inbound -LocalPort 5986 -Protocol TCP
}

# Create Self Signed certificate and store thumbprint
$thumbprint = (New-SelfSignedCertificate -DnsName $env:COMPUTERNAME -CertStoreLocation Cert:\LocalMachine\My).Thumbprint

# Run WinRM configuration on command line. DNS name set to computer hostname.
$cmd = "winrm create winrm/config/Listener?Address=*+Transport=HTTPS @{Hostname=""$env:computername""; CertificateThumbprint=""$thumbprint""}"
cmd.exe /C $cmd
