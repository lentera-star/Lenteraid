# 🔑 SSH Connection Fix Guide

> Quick fixes untuk SSH "Permission denied" error

---

## 🚨 Current Issue

```
root@84.247.150.83's password: 
Permission denied, please try again.
```

---

## 🔧 Solutions (Try in order)

### Solution 1: Clear SSH Known Hosts

```powershell
# Remove old SSH key
ssh-keygen -R 84.247.150.83

# Try again
ssh root@84.247.150.83
```

---

### Solution 2: Check Password dari Email Contabo

1. Cek email dari Contabo dengan subject "VPS Credentials"
2. Copy password PERSIS seperti di email (termasuk special chars)
3. Paste saat login (right-click di PowerShell)

**NOTE**: Password case-sensitive dan bisa ada special chars kayak `!@#$%`

---

### Solution 3: Reset Password via Contabo Panel

1. Login ke [Contabo Customer Panel](https://my.contabo.com)
2. Your Services → VPS → Select your VPS
3. Click "Reset Root Password"
4. Tunggu email dengan password baru (1-5 menit)
5. SSH dengan password baru

---

### Solution 4: Use SSH Key instead of Password

Generate SSH key:

```powershell
# Generate key (if not exist)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Copy public key
type ~\.ssh\id_ed25519.pub
```

Add ke VPS via Contabo panel:
1. Customer Panel → VPS Settings
2. SSH Keys → Add New Key
3. Paste public key
4. Save

Test:

```powershell
ssh -i ~\.ssh\id_ed25519 root@84.247.150.83
```

---

### Solution 5: Verify VPS is Running

```powershell
# Ping VPS
ping 84.247.150.83

# Check if SSH port open
Test-NetConnection -ComputerName 84.247.150.83 -Port 22
```

If ping fails:
1. VPS mungkin shutdown atau suspended
2. Check Contabo panel untuk status
3. Restart VPS jika perlu

---

### Solution 6: Try Different SSH Client

**Option A: PuTTY**
1. Download [PuTTY](https://www.putty.org/)
2. Host: `84.247.150.83`
3. Port: `22`
4. Connection Type: SSH
5. Click Open
6. Username: `root`
7. Password: dari email Contabo

**Option B: Windows Terminal**
```powershell
# Open Windows Terminal
wt
ssh root@84.247.150.83
```

---

## 🔍 Debug Information

Get more details about SSH error:

```powershell
# Verbose SSH
ssh -vvv root@84.247.150.83
```

Look for:
- `debug1: Authentications that can continue: publickey,password`
- `debug1: Next authentication method: password`
- Any errors about key exchange or ciphers

---

## 📞 Emergency Access

Jika semua gagal, contact Contabo support:

1. **Email**: support@contabo.com
2. **Support Ticket**: Via customer panel
3. Request:
   - Password reset assistance
   - Console access (KVM)

Biasanya respond dalam 1-2 jam.

---

## ✅ After SSH Works

Once connected, verify:

```bash
# Check Ollama
ollama --version

# Check backend
ls -la /opt/lentera-backend/

# Check if backend running
systemctl status lentera-backend
```

Then proceed with: **VPS_GGUF_DEPLOYMENT.md** ✅

---

## 💡 Pro Tips

1. **Save password** in secure password manager
2. **Setup SSH key** once connected (lebih aman)
3. **Keep backup access** via Contabo console (KVM)
4. **Screen recorder** saat reset password (bukti)

---

**Good luck!** 🚀
