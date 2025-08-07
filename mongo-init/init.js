// mongo-init/init.js

// Conecta como root (credenciais vindas das env vars)
db = db.getSiblingDB("admin");

// Cria seu database e um usuário de app com permissões restritas:
db = db.getSiblingDB("shomerdb");

// Cria o usuário de aplicação
var appUser = process.env.MONGO_APP_USER || "shomer_user";
try {
  db.createUser({
    user: appUser,
    pwd: process.env.MONGO_APP_PASSWORD,
    roles: [
      { role: "readWrite", db: "shomerdb" },
      { role: "dbAdmin", db: "shomerdb" }
    ]
  });
  print("Usuário '" + appUser + "' criado com sucesso!");
} catch (e) {
  print("Usuário '" + appUser + "' já existe ou erro: " + e.message);
}

// Cria collections básicas
db.createCollection("users");
db.createCollection("logs");
db.createCollection("detections");
print("Collections criadas!");

// Cria índices para melhor performance
db.users.createIndex({ "username": 1 }, { unique: true });
db.users.createIndex({ "email": 1 }, { unique: true });
db.logs.createIndex({ "timestamp": -1 });
db.logs.createIndex({ "user": 1 });
print("Índices criados!");

print("Database 'shomerdb' inicializado com sucesso!");
print("Usuário '" + appUser + "' configurado com permissões restritas");
print("Collections e índices configurados!");
