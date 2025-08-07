// mongo-init/init.js

// Conecta como root (credenciais vindas das env vars)
db = db.getSiblingDB("admin");

// Cria seu database e um usuário de app com permissões restritas:
db = db.getSiblingDB("shomerdb");
db.createUser({
  user: process.env.MONGO_APP_USER || "shomer_app",
  pwd: process.env.MONGO_APP_PASSWORD,
  roles: [
    { role: "readWrite", db: "shomerdb" },
    { role: "dbAdmin", db: "shomerdb" }
  ]
});

// Cria collections básicas
db.createCollection("users");
db.createCollection("logs");
db.createCollection("detections");

// Cria índices para melhor performance
db.users.createIndex({ "username": 1 }, { unique: true });
db.users.createIndex({ "email": 1 }, { unique: true });
db.logs.createIndex({ "timestamp": -1 });
db.logs.createIndex({ "user": 1 });
db.detections.createIndex({ "timestamp": -1 });
db.detections.createIndex({ "user_id": 1 });

print("Database 'shomerdb' inicializado com sucesso!");
print("Usuário '" + (process.env.MONGO_APP_USER || "shomer_app") + "' criado com permissões restritas");
print("Collections 'users', 'logs' e 'detections' criadas");
