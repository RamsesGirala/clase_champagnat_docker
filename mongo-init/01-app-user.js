// Crea la base y el usuario de aplicación con permisos de lectura/escritura
const dbName = "tributaria";
const user = "appuser";
const pass = "apppass";

db = db.getSiblingDB(dbName);

// Fuerza la creación de la DB (Mongo la crea al primer write)
db.createCollection("keepalive_init");
db.keepalive_init.insertOne({ createdAt: new Date() });

// Crea usuario de aplicación con permisos mínimos necesarios
db.createUser({
  user: user,
  pwd:  pass,
  roles: [{ role: "readWrite", db: dbName }],
});
