#!/bin/bash

# Wrapper di avvio Tomcat con hook per init
# Avvia Tomcat in background, poi fa le operazioni, poi blocca in foreground

# Avvia Tomcat in background
echo "Avvio Tomcat in background..."
catalina.sh start

# Attendi che RDF4J sia pronto
echo "Aspetto che RDF4J sia disponibile..."
until curl -s http://localhost:8080/rdf4j-server/ > /dev/null; do
  echo "⏳ RDF4J non è ancora pronto, attendo..."
  sleep 2
done

# Crea repository
echo "✅ RDF4J è attivo, creo repository..."
curl -X POST \
  -H "Content-Type: multipart/form-data" \
  -F "config=@/app/repo-config.ttl" \
  http://localhost:8080/rdf4j-server/repositories

# Carica dati nel repository
echo "📥 Carico dati nel repository..."
curl -X POST \
  -H "Content-Type: text/turtle" \
  --data-binary @/data/DSkg.ttl \
  http://localhost:8080/rdf4j-server/repositories/myrepo/statements

# Riavvio Tomcat in foreground per mantenere il container attivo
echo "♻️ Avvio Tomcat in foreground..."
exec catalina.sh run
