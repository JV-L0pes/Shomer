#!/bin/bash

# Configurar vm.max_map_count dentro do container
echo 262144 > /proc/sys/vm/max_map_count

# Configurar outras otimizações
echo 0 > /proc/sys/vm/swappiness
echo 1 > /proc/sys/vm/overcommit_memory

# Configurar limites de memória
ulimit -l unlimited

# Iniciar o MongoDB com configurações otimizadas e executar scripts de inicialização
exec docker-entrypoint.sh mongod \
  --wiredTigerCacheSizeGB 1 \
  --wiredTigerCollectionBlockCompressor snappy \
  --wiredTigerIndexPrefixCompression true \
  --logappend \
  --journal
