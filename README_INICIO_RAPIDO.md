# 🚀 INICIALIZAÇÃO RÁPIDA - Sistema e-lib

## ⚡ COMANDOS RÁPIDOS

### **Abrir 2 Terminais:**

**Terminal 1 - Backend:**
```bash
cd /home/mostqi/EngSoft/TP1
./start_backend.sh
```

**Terminal 2 - Frontend:**
```bash
cd /home/mostqi/EngSoft/TP1
./start.sh
```

### **Aguardar Mensagens:**
- ✅ Backend: `Running on http://127.0.0.1:5000`
- ✅ Frontend: `Local: http://localhost:4200/`

### **Acessar:**
```
http://localhost:4200
```

---

## 🐛 PROBLEMA ATUAL

**Erro:** `ECONNREFUSED 127.0.0.1:5000`  
**Causa:** Backend não está rodando!  
**Solução:** Execute `./start_backend.sh`

---

## 📊 POPULAR BANCO DE DADOS

### **Opção 1: Durante inicialização do backend**
O script `start_backend.sh` pergunta automaticamente se deseja popular

### **Opção 2: Manualmente**
```bash
cd /home/mostqi/EngSoft/TP1/e-lib/backend
source venv/bin/activate
python seed_bibtex.py seed_data.bib
```

### **Opção 3: Via interface web**
```
1. http://localhost:4200/admin
2. Login: admin@e-lib.com
3. Gerenciar Artigos → Upload em Massa
4. Selecionar: /home/mostqi/EngSoft/TP1/e-lib/backend/seed_data.bib
```

---

## ✅ CHECKLIST

- [ ] MongoDB rodando: `sudo systemctl status mongod`
- [ ] Backend rodando: `./start_backend.sh`
- [ ] Frontend rodando: `./start.sh`
- [ ] Banco populado: 22 artigos + 2 eventos
- [ ] Acesso: http://localhost:4200

---

## 📁 ARQUIVOS IMPORTANTES

| Arquivo | Descrição |
|---------|-----------|
| `start_backend.sh` | 🆕 Inicia backend (Flask) |
| `start.sh` | Inicia frontend (Angular) |
| `e-lib/backend/seed_data.bib` | Dados de teste (22 artigos) |
| `COMO_INICIAR_SISTEMA.md` | Guia completo detalhado |

---

## 🔧 TROUBLESHOOTING RÁPIDO

### Backend não inicia:
```bash
cd /home/mostqi/EngSoft/TP1/e-lib/backend
pip install -r requirements.txt
python run.py
```

### MongoDB não está rodando:
```bash
sudo systemctl start mongod
sudo systemctl status mongod
```

### Porta 5000 ocupada:
```bash
lsof -ti:5000 | xargs kill -9
```

### Banco vazio após reiniciar:
```bash
cd /home/mostqi/EngSoft/TP1/e-lib/backend
python seed_bibtex.py seed_data.bib
```

---

**Versão:** 1.0 | **Data:** 13/10/2025
