# watchdogReg
Check if the TLS records are created on the Windows server. If the records don't exist, create them and generate a log with this information.

# Why?
Windows Server 2012 does not natively support TLS 1.2. Creating these records automatically resolves the issue.
