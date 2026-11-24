# app-policy: тек secret/redis-app жазбасын ОҚУҒА рұқсат (жазу, жою — жоқ)
# KV v2 қозғалтқышында деректер secret/data/<жол> астында сақталады
path "secret/data/redis-app" {
  capabilities = ["read"]
}
