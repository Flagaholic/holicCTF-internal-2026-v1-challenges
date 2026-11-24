FROM eclipse-temurin:8-jre-jammy

WORKDIR /minecraft

RUN useradd -u 10001 -m minecraft

COPY --chown=minecraft:minecraft . .

USER minecraft

EXPOSE 25565

CMD ["java", "-Xms256M", "-Xmx512M", "-jar", "server.jar", "nogui"]
