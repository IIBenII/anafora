# Front

This is the web front end write in vuejs.

# How to launch

```bash
# Save the URI of database API and PBQ parser API
EXPORT DATABASE_URI=http://172.17.0.1:5000

EXPORT API_PARSER_URI=http://172.17.0.1:5000

#build
docker build \
-t anafora_front \
--build-arg VUE_APP_DATABASE_ADRESS=$DATABASE_URI \
--build-arg VUE_APP_WORKER_ADRESS=$API_PARSER_URI \*
.

#run
docker run -p 80:80 anafora_front
```

You can access at this adress http://localhost/