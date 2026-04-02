# Ghost 模块平台支持矩阵

> 生成时间：2026-03-28T15:29:30
> 数据源：`python3 scripts/analyze_module_platforms.py`

## 覆盖统计（按显式 `@config` 声明）

| platform | module count |
|---|---:|
| windows | 46 |
| linux | 32 |
| darwin | 11 |
| android | 7 |
| posix | 5 |
| solaris | 3 |
| all | 1 |

- 模块总数：122
- 未显式声明平台：58
- 显式支持 darwin：11
- 显式支持 android：7

## 能力缺口速览

- Windows：显式模块最多，且包含 `privesc`/`exploit` 能力。
- Linux：覆盖面次之，包含少量 `privesc`/`exploit` 能力。
- macOS：显式模块较少，当前无显式 `privesc`/`exploit` 模块。
- Android：当前显式模块仅覆盖 `gather` 与 `troll`，没有显式 `creds`/`privesc`/`exploit` 模块。

## 各平台显式模块清单

### windows (46)

- 分类分布：admin=13, creds=4, exploit=6, gather=12, manage=6, network=1, privesc=3, troll=1
- `beroot.py`
- `bypassuac.py`
- `check_vm.py`
- `clear_logs.py`
- `credcap.py`
- `creddump.py`
- `drives.py`
- `duplicate.py`
- `exploit_suggester.py`
- `getdomain.py`
- `getprivs.py`
- `getsystem.py`
- `impersonate.py`
- `inveigh.py`
- `isearch.py`
- `keylogger.py`
- `last.py`
- `lazagne.py`
- `lock_screen.py`
- `logs.py`
- `loot_memory.py`
- `memory_exec.py`
- `memstrings.py`
- `migrate.py`
- `mimikatz.py`
- `mimishell.py`
- `mouselogger.py`
- `msgbox.py`
- `nbnsspoof.py`
- `outlook.py`
- `persistence.py`
- `pipecatcher.py`
- `powerview.py`
- `psh.py`
- `pywerview.py`
- `rdesktop.py`
- `rdp.py`
- `record_mic.py`
- `screenshot.py`
- `services.py`
- `shares.py`
- `shellcode_exec.py`
- `stat.py`
- `users.py`
- `webcamsnap.py`
- `wmic.py`

### linux (32)

- 分类分布：admin=9, creds=5, exploit=1, gather=8, manage=6, privesc=1, troll=1, unknown=1
- `become.py`
- `beroot.py`
- `check_vm.py`
- `credcap.py`
- `creddump.py`
- `duplicate.py`
- `exploit_suggester.py`
- `hashmon.py`
- `hide_process.py`
- `keylogger.py`
- `last.py`
- `lazagne.py`
- `linux_stealth.py`
- `loot_memory.py`
- `mapped.py`
- `memory_exec.py`
- `memstrings.py`
- `migrate.py`
- `mimipy.py`
- `msgbox.py`
- `persistence.py`
- `privesc_checker.py`
- `rdesktop.py`
- `rdp.py`
- `screenshot.py`
- `services.py`
- `shares.py`
- `stat.py`
- `sudo_alias.py`
- `ttyrec.py`
- `users.py`
- `usniper.py`

### darwin (11)

- 分类分布：admin=4, creds=1, gather=4, manage=1, troll=1
- `check_vm.py`
- `creddump.py`
- `drives.py`
- `keylogger.py`
- `lock_screen.py`
- `msgbox.py`
- `rdesktop.py`
- `rdp.py`
- `screenshot.py`
- `sudo_alias.py`
- `users.py`

### android (7)

- 分类分布：gather=5, troll=2
- `apps.py`
- `call.py`
- `contacts.py`
- `gpstracker.py`
- `text_to_speach.py`
- `vibrate.py`
- `webcamsnap.py`

## 未显式声明平台的模块

- 共 58 个。它们不等于“全平台支持”，只代表源码没有写清楚兼容边界。
- `ad.py`, `alive.py`, `cat.py`, `cd.py`, `cloudinfo.py`, `cp.py`, `date.py`, `dns.py`, `download.py`, `echo.py`, `edit.py`, `env.py`, `exit.py`, `forward.py`, `get_hwuuid.py`, `get_info.py`, `getpid.py`, `getppid.py`, `getuid.py`, `http.py`, `igd.py`, `interactive_shell.py`, `ip.py`, `ls.py`, `mkdir.py`, `mv.py`, `netcreds.py`, `netmon.py`, `netstat.py`, `odbc.py`, `pexec.py`, `port_scan.py`, `portfwd.py`, `process_kill.py`, `ps.py`, `psexec.py`, `pwd.py`, `pyexec.py`, `pyshell.py`, `reg.py`, `rfs.py`, `rm.py`, `rwmic.py`, `scapy_shell.py`, `search.py`, `shell_exec.py`, `smb.py`, `smbspider.py`, `socks5proxy.py`, `ssh.py`, `sshell.py`, `tasks.py`, `tcpdump.py`, `upload.py`, `w.py`, `write.py`, `x509.py`, `zip.py`

## 可复现命令

```bash
cd /Users/pangxingzhong/.openclaw/workspace/Ghost
python3 scripts/analyze_module_platforms.py
python3 scripts/identify_generic_modules.py
```
