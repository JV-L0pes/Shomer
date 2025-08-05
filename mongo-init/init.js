// mongo-init/init.js

// Conecta como root (credenciais vindas das env vars)
db = db.getSiblingDB("admin");

// Cria seu database e um usuário de app com permissões restritas:
db = db.getSiblingDB("shomerdb");
db.createUser({
  user: "appuser",
  pwd: "appPass123",
  roles: [
    { role: "readWrite", db: "shomerdb" }
  ]
});

// Cria collections básicas (opcional, pois o Mongo é schema-less):
db.createCollection("users");
db.createCollection("logs");
