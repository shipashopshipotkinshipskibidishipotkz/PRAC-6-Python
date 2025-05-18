import asyncio
from spotify_client import get_spotify_token, search_track
from genius_client import search_lyrics_url, search_by_lyrics_snippet

async def main():
    token = await get_spotify_token()

    while True:
        print("\nЧто вы хотите сделать?")
        print("1. Найти трек по названию")
        print("2. Найти трек по тексту")
        print("3. Выйти")
        choice = input("Ваш выбор (1/2/3): ").strip()

        if choice == "1":
            track_name = input("Введите название песни: ")
            track_info = await search_track(track_name, token)

            if not track_info:
                print("❌ Не удалось найти трек.")
                continue

            print(f"\n🎵 Название: {track_info['name']}")
            print(f"👤 Исполнитель: {track_info['artist']}")
            print(f"🖼️ Обложка: {track_info['album_cover']}")
            print(f"🔗 Слушать в Spotify: {track_info['spotify_url']}")

            lyrics_url = await search_lyrics_url(track_info["name"], track_info["artist"])
            print(f"📜 Текст песни: {lyrics_url or 'Не найден'}")

        elif choice == "2":
            lyrics_snippet = input("Введите часть текста песни: ")
            title, artist = await search_by_lyrics_snippet(lyrics_snippet)

            if not title or not artist:
                print("❌ Песня не найдена.")
                continue

            lyrics_url = await search_lyrics_url(title, artist)
            print(f"\n🎵 Название: {title}")
            print(f"👤 Исполнитель: {artist}")
            print(f"📜 Ссылка на текст: {lyrics_url or 'Не найден'}")

        elif choice == "3" or choice.lower() in {"exit", "выход"}:
            print(" пока")
            break
        else:
            print("Неверный ввод. Попробуйте снова.")

if __name__ == "__main__":
    asyncio.run(main())
